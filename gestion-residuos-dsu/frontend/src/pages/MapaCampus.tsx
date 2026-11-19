import L from 'leaflet'
import 'leaflet.heat'
import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from 'react-leaflet'

import { Estimado } from '../components/Estimado'
import { FiltrosAnalisis, consulta, filtrosIniciales, type Filtros } from '../components/FiltrosAnalisis'
import { CENTRO_CAMPUS } from '../components/Mapa'
import { Aviso, Cargando, Encabezado, Tabla, cx } from '../components/ui'
import { api } from '../lib/api'
import { useAuth } from '../lib/auth'
import { aproximado, fecha, fechaHora, numero, useCarga } from '../lib/datos'

type Ubicado = { id: number; codigo: string; nombre: string; sector: string; latitud: string; longitud: string; peso: number; total_kg: string; promedio_dia_kg: string }
type PuntoMapa = Ubicado & { capacidad_kg: string; critico: boolean; ultima_atencion: string | null }
type DatosMapa = { alcance: { dias: number }; maximo_kg: string; umbral_critico_kg_dia: string; puntos: PuntoMapa[]; registros: number }
type PuntoProyectado = Ubicado & { margen_kg: string; desde: string; hasta: string; version: number }
type DatosProyectados = { maximo_kg: string; puntos: PuntoProyectado[] }

// Escala secuencial de un solo tono (rojo DSU, de claro a oscuro): intensidad de generación.
const ESCALA = ['#f6d5da', '#ec9aa6', '#d9485f', '#c4122f', '#7a0a1c']
const GRADIENTE = { 0.15: ESCALA[0], 0.4: ESCALA[1], 0.65: ESCALA[2], 0.85: ESCALA[3], 1: ESCALA[4] }
const colorPorPeso = (peso: number) => ESCALA[Math.min(ESCALA.length - 1, Math.floor(peso * ESCALA.length))]

function CapaCalor({ puntos }: { puntos: Ubicado[] }) {
  const mapa = useMap()
  useEffect(() => {
    const capa = L.heatLayer(
      puntos.filter((p) => p.peso > 0).map((p) => [Number(p.latitud), Number(p.longitud), p.peso]),
      { radius: 38, blur: 26, maxZoom: 18, max: 1, minOpacity: 0.25, gradient: GRADIENTE },
    ).addTo(mapa)
    return () => {
      capa.remove()
    }
  }, [mapa, puntos])
  return null
}

function Encuadre({ puntos }: { puntos: Ubicado[] }) {
  const mapa = useMap()
  useEffect(() => {
    if (puntos.length) mapa.fitBounds(L.latLngBounds(puntos.map((p) => [Number(p.latitud), Number(p.longitud)])), { padding: [40, 40], maxZoom: 18 })
  }, [mapa, puntos])
  return null
}

function Lienzo({
  puntos,
  capa,
  maximo,
  leyenda,
  marcador,
  popup,
}: {
  puntos: Ubicado[]
  capa: 'calor' | 'marcadores'
  maximo: string
  leyenda: string
  marcador: (p: Ubicado) => { radius: number; pathOptions: L.PathOptions }
  popup: (p: Ubicado) => ReactNode
}) {
  return (
    <div className="relative h-[min(62vh,560px)] overflow-hidden rounded-hoja border border-filete">
      <MapContainer center={CENTRO_CAMPUS} zoom={17} className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          maxZoom={19}
        />
        <Encuadre puntos={puntos} />
        {capa === 'calor' && <CapaCalor puntos={puntos} />}
        {puntos.map((p) => (
          <CircleMarker key={p.id} center={[Number(p.latitud), Number(p.longitud)]} {...marcador(p)}>
            <Popup>
              <div className="min-w-48 text-sm">
                <p className="text-base font-bold">{p.codigo}</p>
                <p className="mb-2 text-grafito-2">
                  {p.nombre} · {p.sector}
                </p>
                {popup(p)}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      <div className="pointer-events-none absolute bottom-3 left-3 z-[500] rounded-hoja border border-filete bg-hoja px-3 py-2 text-xs shadow-[0_2px_8px_rgb(0_0_0/0.1)]">
        <p className="rotulo mb-1">{leyenda}</p>
        <div className="h-2.5 w-48 rounded-sm" style={{ background: `linear-gradient(to right, ${ESCALA.join(',')})` }} />
        <div className="mt-1 flex justify-between text-grafito-2">
          <span>0</span>
          <span>{maximo}</span>
        </div>
      </div>
    </div>
  )
}

function Observada({ filtros, capa }: { filtros: Filtros; capa: 'calor' | 'marcadores' }) {
  const { data, error, cargando } = useCarga(() => api<DatosMapa>('analitica/mapa/', { query: consulta(filtros) }), [JSON.stringify(filtros)])
  const puntos = useMemo(() => data?.puntos ?? [], [data])
  if (error) return <Aviso tono="error">{error}</Aviso>
  if (cargando && !data) return <Cargando texto="Calculando la intensidad por punto…" />
  if (!data) return null
  const criticos = puntos.filter((p) => p.critico)
  return (
    <div className="flex flex-col gap-5">
      {!data.registros && <Aviso>No hay registros depurados para estos filtros; el mapa muestra los puntos sin intensidad.</Aviso>}
      <Lienzo
        puntos={puntos}
        capa={capa}
        maximo={numero(data.maximo_kg)}
        leyenda={capa === 'calor' ? 'Generación en el periodo (kg) · anillo oscuro = crítico' : 'Generación en el periodo (kg)'}
        marcador={(u) => {
          const p = u as PuntoMapa
          return {
            radius: capa === 'marcadores' ? 9 : p.critico ? 7 : 4,
            pathOptions:
              capa === 'marcadores'
                ? { color: '#ffffff', weight: 2, fillColor: colorPorPeso(p.peso), fillOpacity: 1 }
                : { color: p.critico ? '#1e2328' : '#ffffff', weight: p.critico ? 2.5 : 1.5, fillColor: '#ffffff', fillOpacity: p.critico ? 0 : 0.9 },
          }
        }}
        popup={(u) => {
          const p = u as PuntoMapa
          return (
            <>
              <p>
                Generado: <strong className="tinta">{numero(p.total_kg)} kg</strong> ({numero(p.promedio_dia_kg)} kg/día)
              </p>
              <p>Capacidad: {numero(p.capacidad_kg)} kg</p>
              <p>Última atención: {fechaHora(p.ultima_atencion)}</p>
              {p.critico && <p className="mt-1 font-semibold text-dsu">Zona crítica: supera el umbral diario</p>}
            </>
          )
        }}
      />
      <section>
        <h2 className="mb-2 font-bold [font-stretch:90%]">
          Zonas críticas <span className="text-sm font-medium text-grafito-2">(más de {numero(data.umbral_critico_kg_dia)} kg por día)</span>
        </h2>
        <Tabla
          filas={criticos}
          vacio="Ningún punto supera el umbral en este periodo."
          columnas={[
            { titulo: 'Punto', celda: (p) => <span className="font-semibold [font-stretch:85%]">{p.codigo}</span> },
            { titulo: 'Sector', celda: (p) => p.sector },
            { titulo: 'Promedio diario', derecha: true, celda: (p) => <span className="tinta font-semibold">{numero(p.promedio_dia_kg)} kg</span> },
            { titulo: 'Capacidad', derecha: true, celda: (p) => `${numero(p.capacidad_kg)} kg` },
            { titulo: 'Última atención', celda: (p) => fechaHora(p.ultima_atencion) },
          ]}
        />
      </section>
    </div>
  )
}

/** RF20: capa proyectada con la predicción vigente de cada punto; las cifras van a lápiz y con margen. */
function Proyectada({ sector, capa }: { sector: string; capa: 'calor' | 'marcadores' }) {
  const { data, error, cargando } = useCarga(() => api<DatosProyectados>('predicciones/mapa/', { query: { sector } }), [sector])
  const puntos = useMemo(() => data?.puntos ?? [], [data])
  if (error) return <Aviso tono="error">{error}</Aviso>
  if (cargando && !data) return <Cargando texto="Cargando la generación proyectada…" />
  if (!data) return null
  if (!puntos.length) return <Aviso>No hay predicciones vigentes para este alcance. Genere una en el módulo de Predicción.</Aviso>
  const ordenados = [...puntos].sort((a, b) => Number(b.total_kg) - Number(a.total_kg))
  return (
    <div className="flex flex-col gap-5">
      <Lienzo
        puntos={puntos}
        capa={capa}
        maximo={`≈ ${aproximado(Number(data.maximo_kg))}`}
        leyenda="Generación proyectada en el horizonte (kg)"
        marcador={(p) => ({
          radius: capa === 'marcadores' ? 9 : 4,
          pathOptions:
            capa === 'marcadores'
              ? { color: '#ffffff', weight: 2, fillColor: colorPorPeso(p.peso), fillOpacity: 1, dashArray: '3 3' }
              : { color: '#ffffff', weight: 1.5, fillColor: '#ffffff', fillOpacity: 0.9 },
        })}
        popup={(u) => {
          const p = u as PuntoProyectado
          return (
            <>
              <p>
                Proyectado: <Estimado valor={p.total_kg} margen={p.margen_kg} />
              </p>
              <p>
                Del {fecha(p.desde)} al {fecha(p.hasta)} · modelo v{p.version}
              </p>
            </>
          )
        }}
      />
      <section>
        <h2 className="mb-2 font-bold [font-stretch:90%]">Generación proyectada por punto</h2>
        <Tabla
          filas={ordenados}
          columnas={[
            { titulo: 'Punto', celda: (p) => <span className="font-semibold [font-stretch:85%]">{p.codigo}</span> },
            { titulo: 'Sector', celda: (p) => p.sector },
            { titulo: 'Horizonte', celda: (p) => `${fecha(p.desde)} – ${fecha(p.hasta)}` },
            { titulo: 'Generación proyectada', derecha: true, celda: (p) => <Estimado valor={p.total_kg} margen={p.margen_kg} /> },
            { titulo: 'Modelo', derecha: true, celda: (p) => `v${p.version}` },
          ]}
        />
      </section>
    </div>
  )
}

export function MapaCampus() {
  const { puede } = useAuth()
  const [filtros, setFiltros] = useState<Filtros>(() => filtrosIniciales())
  const [capa, setCapa] = useState<'calor' | 'marcadores'>('calor')
  const [proyectada, setProyectada] = useState(false)

  return (
    <>
      <Encabezado
        titulo="Mapa del campus"
        detalle={
          proyectada
            ? 'Generación estimada por el modelo para el horizonte vigente de cada punto. Es una proyección de apoyo, con margen de error.'
            : 'Generación observada por punto de recolección. Las zonas más oscuras concentran más residuos en el periodo.'
        }
      />
      {proyectada ? (
        <div className="mb-4">
          <Aviso>La capa proyectada usa la predicción vigente de cada punto; de los filtros solo se aplica el sector.</Aviso>
        </div>
      ) : null}
      <FiltrosAnalisis valor={filtros} cambiar={setFiltros} />
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <div role="radiogroup" aria-label="Capa del mapa" className="inline-flex rounded-hoja border border-filete bg-hoja p-0.5">
          {(
            [
              ['calor', 'Mapa de calor'],
              ['marcadores', 'Marcadores'],
            ] as const
          ).map(([id, texto]) => (
            <button
              key={id}
              role="radio"
              aria-checked={capa === id}
              onClick={() => setCapa(id)}
              className={cx('min-h-9 rounded-[3px] px-3 text-sm font-semibold', capa === id ? 'bg-grafito text-white' : 'text-grafito-2 hover:text-grafito')}
            >
              {texto}
            </button>
          ))}
        </div>
        {puede('prediction.view_prediccion') && (
          <div role="radiogroup" aria-label="Generación mostrada" className="inline-flex rounded-hoja border border-filete bg-hoja p-0.5">
            {(
              [
                [false, 'Observada'],
                [true, 'Proyectada'],
              ] as const
            ).map(([id, texto]) => (
              <button
                key={texto}
                role="radio"
                aria-checked={proyectada === id}
                onClick={() => setProyectada(id)}
                className={cx('min-h-9 rounded-[3px] px-3 text-sm font-semibold', proyectada === id ? 'bg-grafito text-white' : 'text-grafito-2 hover:text-grafito')}
              >
                {texto}
              </button>
            ))}
          </div>
        )}
      </div>
      {proyectada ? <Proyectada sector={filtros.sector} capa={capa} /> : <Observada filtros={filtros} capa={capa} />}
    </>
  )
}
