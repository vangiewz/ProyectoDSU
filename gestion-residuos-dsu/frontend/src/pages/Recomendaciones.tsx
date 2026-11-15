import { Check, X } from 'lucide-react'
import { useState, type ReactNode } from 'react'
import { Link } from 'react-router'

import { Estimado } from '../components/Estimado'
import { Sello, type EstadoSello } from '../components/Sello'
import { Area, Aviso, Boton, Cargando, Encabezado, Paginacion, Vacio, cx } from '../components/ui'
import { api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fecha, fechaHora, numero, useCarga } from '../lib/datos'

type Evidencia = {
  capacidad_kg: number
  proxima_atencion: string | null
  dias_hasta_atencion: number
  acumulado_proyectado_kg: number
  margen_kg: number
  ocupacion_proyectada_pct: number
  promedio_reciente_dia_kg: number | null
  crecimiento_pct: number | null
  no_aprovechable_pct: number
  incidencias_mal_segregado_90d: number
  modelo_version: number
  horizonte: { desde: string; hasta: string }
}

type Recomendacion = {
  id: number
  punto: number
  punto_codigo: string
  punto_nombre: string
  sector_nombre: string
  tipo: string
  tipo_display: string
  urgencia: 'ALTA' | 'MEDIA' | 'BAJA'
  es_alerta: boolean
  mensaje: string
  evidencia: Evidencia
  estado: 'PENDIENTE' | 'ACEPTADA' | 'DESCARTADA' | 'REEMPLAZADA'
  estado_display: string
  creada_en: string
  resuelta_por_nombre: string | null
  resuelta_en: string | null
  motivo_decision: string
  jornada: number | null
  jornada_fecha: string | null
}

const URGENCIA: Record<Recomendacion['urgencia'], EstadoSello> = { ALTA: 'URGENCIA ALTA', MEDIA: 'URGENCIA MEDIA', BAJA: 'URGENCIA BAJA' }
const pct = (v: number | null) => (v === null ? '—' : `${v > 0 ? '+' : ''}${numero(v)} %`)

function Dato({ rotulo, children }: { rotulo: string; children: ReactNode }) {
  return (
    <div className="min-w-0">
      <dt className="rotulo">{rotulo}</dt>
      <dd className="mt-0.5 text-sm">{children}</dd>
    </div>
  )
}

/** La evidencia histórica y predictiva que sustenta la recomendación (RF24 paso 3.2). */
function Evidencias({ e }: { e: Evidencia }) {
  return (
    <dl className="mt-3 grid grid-cols-2 gap-x-5 gap-y-3 sm:grid-cols-4">
      <Dato rotulo="Capacidad instalada">{numero(e.capacidad_kg)} kg</Dato>
      <Dato rotulo={e.proxima_atencion ? `Hasta el ${fecha(e.proxima_atencion)}` : 'Próximo día de recolección'}>
        <Estimado valor={e.acumulado_proyectado_kg} margen={e.margen_kg} />
      </Dato>
      <Dato rotulo="Ocupación proyectada">
        <span className="lapiz font-semibold">≈ {numero(e.ocupacion_proyectada_pct)} %</span>
      </Dato>
      <Dato rotulo="Promedio de los últimos 28 días">
        {e.promedio_reciente_dia_kg === null ? '—' : <span className="tinta font-semibold">{numero(e.promedio_reciente_dia_kg)} kg/día</span>}
      </Dato>
      <Dato rotulo="Variación proyectada">{pct(e.crecimiento_pct)}</Dato>
      <Dato rotulo="Residuo no aprovechable">{numero(e.no_aprovechable_pct)} %</Dato>
      <Dato rotulo="Incid. de segregación (90 días)">{e.incidencias_mal_segregado_90d}</Dato>
      <Dato rotulo="Fuente">
        Modelo v{e.modelo_version}, {fecha(e.horizonte.desde)} – {fecha(e.horizonte.hasta)}
      </Dato>
    </dl>
  )
}

function Decision({ r, puedeResolver, alResolver }: { r: Recomendacion; puedeResolver: boolean; alResolver: (r: Recomendacion) => void }) {
  const [motivo, setMotivo] = useState('')
  const [enviando, setEnviando] = useState<'aceptar' | 'descartar' | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function resolver(accion: 'aceptar' | 'descartar') {
    if (!motivo.trim()) {
      setError('Indique el motivo de la decisión.')
      return
    }
    setEnviando(accion)
    setError(null)
    try {
      alResolver(await api<Recomendacion>(`recomendaciones/${r.id}/${accion}/`, { body: { motivo } }))
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setEnviando(null)
    }
  }

  if (r.estado !== 'PENDIENTE') return null
  if (!puedeResolver) return <p className="text-sm text-grafito-2">Pendiente de decisión del supervisor.</p>
  return (
    <div className="flex flex-col gap-2">
      <label className="flex flex-col gap-1.5">
        <span className="rotulo">Motivo de la decisión</span>
        <Area value={motivo} onChange={(e) => setMotivo(e.target.value)} placeholder="Qué observó o por qué decide así" rows={2} />
      </label>
      {error && <p className="text-xs font-medium text-dsu">{error}</p>}
      <div className="flex gap-2">
        <Boton className="flex-1" cargando={enviando === 'aceptar'} disabled={!!enviando} onClick={() => void resolver('aceptar')}>
          <Check className="size-4" aria-hidden /> Aceptar
        </Boton>
        <Boton className="flex-1" variante="secundario" cargando={enviando === 'descartar'} disabled={!!enviando} onClick={() => void resolver('descartar')}>
          <X className="size-4" aria-hidden /> Descartar
        </Boton>
      </div>
    </div>
  )
}

function Resuelta({ r, recien }: { r: Recomendacion; recien: boolean }) {
  if (r.estado === 'PENDIENTE') return null
  const incorporable = r.tipo === 'PRIORIZAR' || r.tipo === 'INCREMENTAR_FRECUENCIA'
  return (
    <div className="flex flex-col items-start gap-2 text-sm">
      <Sello estado={r.estado as EstadoSello} recien={recien} />
      {r.motivo_decision && <p className="tinta">“{r.motivo_decision}”</p>}
      {r.resuelta_por_nombre && (
        <p className="text-xs text-grafito-2">
          {r.resuelta_por_nombre} · {fechaHora(r.resuelta_en)}
        </p>
      )}
      {r.estado === 'ACEPTADA' &&
        incorporable &&
        (r.jornada ? (
          <Link to={`/jornadas/${r.jornada}`} className="font-semibold underline">
            Incorporada a la jornada del {fecha(r.jornada_fecha)}
          </Link>
        ) : (
          <p className="text-xs text-sello-omit">No hay jornada planificada para el sector: considérela al planificar la próxima.</p>
        ))}
    </div>
  )
}

function Lista({ titulo, detalle, filas, recientes, puedeResolver, alResolver }: {
  titulo: string
  detalle: string
  filas: Recomendacion[]
  recientes: Set<number>
  puedeResolver: boolean
  alResolver: (r: Recomendacion) => void
}) {
  if (!filas.length) return null
  return (
    <section className="rounded-hoja border border-filete bg-hoja">
      <header className="border-b border-filete px-5 py-3">
        <h2 className="font-bold [font-stretch:90%]">
          {titulo} <span className="font-medium text-grafito-2">({filas.length})</span>
        </h2>
        <p className="text-sm text-grafito-2">{detalle}</p>
      </header>
      <ul>
        {filas.map((r) => (
          <li key={r.id} className="grid gap-4 border-b border-filete-suave px-5 py-5 last:border-0 lg:grid-cols-[9.5rem_minmax(0,1fr)_17rem]">
            <div className="flex flex-row items-start gap-3 lg:flex-col">
              <Sello estado={URGENCIA[r.urgencia]} />
              <div>
                <p className="text-xl leading-tight font-bold [font-stretch:80%]">{r.punto_codigo}</p>
                <p className="text-xs text-grafito-2">{r.sector_nombre}</p>
              </div>
            </div>
            <div className="min-w-0">
              <p className={cx('font-bold', r.es_alerta && 'text-dsu-hondo')}>{r.tipo_display}</p>
              <p className="mt-1 max-w-[70ch] text-sm text-grafito">{r.mensaje}</p>
              <Evidencias e={r.evidencia} />
            </div>
            <div>
              <Decision r={r} puedeResolver={puedeResolver} alResolver={alResolver} />
              <Resuelta r={r} recien={recientes.has(r.id)} />
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}

export function Recomendaciones() {
  const { puede } = useAuth()
  const [vista, setVista] = useState<'pendientes' | 'todas'>('pendientes')
  const [pagina, setPagina] = useState(1)
  const [recientes, setRecientes] = useState<Set<number>>(new Set())
  const { data, error, cargando, setData } = useCarga(
    () => api<Pagina<Recomendacion>>('recomendaciones/', { query: { page: pagina, page_size: 50, estado: vista === 'pendientes' ? 'PENDIENTE' : undefined } }),
    [vista, pagina],
  )

  // La recomendación resuelta queda en su lugar con el sello recién estampado.
  const alResolver = (r: Recomendacion) => {
    setRecientes((s) => new Set(s).add(r.id))
    setData((d) => (d ? { ...d, results: d.results.map((x) => (x.id === r.id ? r : x)) } : d))
  }
  const filas = data?.results ?? []
  const comun = { recientes, puedeResolver: puede('prediction.resolver_recomendacion'), alResolver }

  return (
    <>
      <Encabezado
        titulo="Alertas y recomendaciones"
        detalle="Se emiten a partir de cada predicción. Son de apoyo: el supervisor decide, indica el motivo y su decisión queda registrada."
        acciones={
          <div role="radiogroup" aria-label="Recomendaciones mostradas" className="inline-flex rounded-hoja border border-filete bg-hoja p-0.5">
            {(
              [
                ['pendientes', 'Por resolver'],
                ['todas', 'Todas'],
              ] as const
            ).map(([id, texto]) => (
              <button
                key={id}
                role="radio"
                aria-checked={vista === id}
                onClick={() => {
                  setVista(id)
                  setPagina(1)
                }}
                className={cx('min-h-9 rounded-[3px] px-3 text-sm font-semibold', vista === id ? 'bg-grafito text-white' : 'text-grafito-2 hover:text-grafito')}
              >
                {texto}
              </button>
            ))}
          </div>
        }
      />
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && !data && <Cargando />}
      {data && !filas.length && (
        <Vacio titulo={vista === 'pendientes' ? 'No hay recomendaciones por resolver' : 'Aún no se emitieron recomendaciones'}>
          Se generan al solicitar una <Link to="/predicciones" className="font-semibold underline">predicción</Link>.
        </Vacio>
      )}
      {data && filas.length > 0 && (
        <div className="flex flex-col gap-6">
          <Lista
            titulo="Alertas tempranas de desborde"
            detalle="Puntos cuya generación proyectada se acerca o supera su capacidad antes de la próxima atención. Al aceptarla, el punto pasa al primer lugar de la siguiente jornada de su sector."
            filas={filas.filter((r) => r.es_alerta)}
            {...comun}
          />
          <Lista
            titulo="Recomendaciones logísticas"
            detalle="Acciones sobre la frecuencia, los contenedores y la separación en origen, según el patrón detectado."
            filas={filas.filter((r) => !r.es_alerta)}
            {...comun}
          />
          <Paginacion pagina={pagina} total={data.count} porPagina={50} cambiar={setPagina} />
        </div>
      )}
    </>
  )
}
