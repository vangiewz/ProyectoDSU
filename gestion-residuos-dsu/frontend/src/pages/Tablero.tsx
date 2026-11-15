import { ArrowDownRight, ArrowUpRight, ExternalLink, TrendingUp } from 'lucide-react'
import { useState, type ReactNode } from 'react'
import { Link, useNavigate } from 'react-router'

import { FiltrosAnalisis, consulta, filtrosIniciales, type Filtros } from '../components/FiltrosAnalisis'
import { BarrasHorizontales, Columnas } from '../components/Graficos'
import { Aviso, Campo, Cargando, Encabezado, Entrada, Seleccion, Tabla, Vacio, cx } from '../components/ui'
import { api } from '../lib/api'
import { fecha, numero, useCarga } from '../lib/datos'

type KPIs = {
  alcance: { desde: string; hasta: string; dias: number }
  total_kg: string
  total_litros: string
  variacion_kg_pct: number | null
  periodo_anterior: { desde: string; hasta: string; total_kg: string }
  promedio_kg_por_punto: string
  promedio_kg_por_sector: string
  sector_mayor_generacion: { sector__nombre: string; total: string } | null
  tipo_predominante: { tipo_residuo__nombre: string; total: string; magnitud: string } | null
  recolecciones_realizadas: number
  frecuencia_semanal_por_punto: number
  cobertura_pct: number | null
  puntos_criticos: { punto_id: number; punto__codigo: string; punto__nombre: string; sector__nombre: string; total: string; promedio_dia: string }[]
  umbral_critico_kg_dia: string
  registros: number
  atipicos: number
  por_sector: { sector_id: number; sector__codigo: string; sector__nombre: string; total: string }[]
  por_punto: { punto_id: number; punto__codigo: string; punto__nombre: string; sector__nombre: string; total: string }[]
  por_tipo: { tipo_residuo_id: number; tipo_residuo__nombre: string; magnitud: string; total: string }[]
  serie: { etiqueta: string; total: string }[]
  serie_por: 'dia' | 'semana'
}

const corta = new Intl.DateTimeFormat('es-BO', { day: '2-digit', month: 'short' })

function Variacion({ pct }: { pct: number | null }) {
  if (pct === null) return <span className="text-grafito-2">sin datos del periodo anterior</span>
  const sube = pct > 0
  const Icono = sube ? ArrowUpRight : ArrowDownRight
  return (
    <span className="inline-flex items-center gap-1 font-semibold">
      <Icono className={cx('size-4', sube ? 'text-dsu' : 'text-sello-ok')} aria-hidden />
      {sube ? '+' : ''}
      {numero(pct)}% respecto del periodo anterior
    </span>
  )
}

/** Planilla de indicadores: un solo número protagonista y el resto como renglones asentados. */
function Indicadores({ k }: { k: KPIs }) {
  const renglones: [string, ReactNode][] = [
    ['Promedio por punto', `${numero(k.promedio_kg_por_punto)} kg`],
    ['Promedio por sector', `${numero(k.promedio_kg_por_sector)} kg`],
    ['Sector de mayor generación', k.sector_mayor_generacion ? `${k.sector_mayor_generacion.sector__nombre} · ${numero(k.sector_mayor_generacion.total)} kg` : '—'],
    ['Tipo predominante', k.tipo_predominante?.tipo_residuo__nombre ?? '—'],
    ['Jornadas cerradas', k.recolecciones_realizadas],
    ['Atenciones por punto', `${numero(k.frecuencia_semanal_por_punto)} por semana`],
    ['Cobertura de jornadas', k.cobertura_pct === null ? '—' : `${numero(k.cobertura_pct)}%`],
    ['Volumen registrado', `${numero(k.total_litros)} L`],
  ]
  return (
    <section className="grid gap-x-8 gap-y-5 rounded-hoja border border-filete bg-hoja p-5 lg:grid-cols-[minmax(0,18rem)_1fr]">
      <div>
        <p className="rotulo">Total recolectado · {k.alcance.dias} días</p>
        <p className="tinta mt-1 text-[3.25rem] leading-none font-extrabold tracking-tight [font-variant-numeric:proportional-nums]">
          {numero(k.total_kg)}
          <span className="ml-1.5 text-2xl font-bold">kg</span>
        </p>
        <p className="mt-2 text-sm">
          <Variacion pct={k.variacion_kg_pct} />
        </p>
        <p className="mt-3 text-xs text-grafito-2">
          {k.registros} registros depurados{k.atipicos ? ` · ${k.atipicos} marcados como atípicos` : ''}
        </p>
      </div>
      <dl className="grid content-start gap-x-8 sm:grid-cols-2">
        {renglones.map(([t, v]) => (
          <div key={t} className="flex items-baseline justify-between gap-4 border-b border-filete-suave py-2 text-sm">
            <dt className="text-grafito-2">{t}</dt>
            <dd className="text-right font-semibold">{v}</dd>
          </div>
        ))}
      </dl>
    </section>
  )
}

function Resumen({ filtros, cambiar }: { filtros: Filtros; cambiar: (f: Filtros) => void }) {
  const navegar = useNavigate()
  const { data: k, error, cargando } = useCarga(() => api<KPIs>('analitica/indicadores/', { query: consulta(filtros) }), [JSON.stringify(filtros)])
  if (cargando && !k) return <Cargando texto="Calculando indicadores…" />
  if (error) return <Aviso tono="error">{error}</Aviso>
  if (!k) return null
  const enlace = (extra: Record<string, string>) =>
    `/historico?${new URLSearchParams({ desde: k.alcance.desde, hasta: k.alcance.hasta, ...extra }).toString()}`

  return (
    <div className="flex flex-col gap-5">
      <Indicadores k={k} />
      <Columnas
        titulo={k.serie_por === 'dia' ? 'Generación diaria' : 'Generación semanal'}
        unidad="kg"
        datos={k.serie.map((s) => ({ etiqueta: k.serie_por === 'dia' ? corta.format(new Date(`${s.etiqueta}T12:00`)) : s.etiqueta, valor: Number(s.total) }))}
      />
      <div className="grid gap-5 lg:grid-cols-2">
        {/* RF17: elegir una barra filtra todo el tablero por ese elemento; el punto abre su detalle. */}
        <BarrasHorizontales
          titulo="Por sector"
          unidad="kg"
          datos={k.por_sector.map((s) => ({ etiqueta: s.sector__codigo, detalle: s.sector__nombre, valor: Number(s.total) }))}
          alElegir={(d) => {
            const s = k.por_sector.find((x) => x.sector__codigo === d.etiqueta)
            if (s) cambiar({ ...filtros, sector: String(s.sector_id), punto: '' })
          }}
        />
        <BarrasHorizontales
          titulo="Por tipo de residuo"
          unidad="kg"
          datos={k.por_tipo.filter((t) => t.magnitud === 'PESO').map((t) => ({ etiqueta: t.tipo_residuo__nombre, valor: Number(t.total) }))}
          alElegir={(d) => {
            const t = k.por_tipo.find((x) => x.tipo_residuo__nombre === d.etiqueta)
            if (t) cambiar({ ...filtros, tipo_residuo: String(t.tipo_residuo_id) })
          }}
        />
      </div>
      <BarrasHorizontales
        titulo="Puntos de mayor generación"
        unidad="kg"
        datos={k.por_punto.map((p) => ({ etiqueta: p.punto__codigo, detalle: `${p.punto__nombre} · ${p.sector__nombre}`, valor: Number(p.total) }))}
        alElegir={(d) => navegar(enlace({ search: d.etiqueta }))}
      />
      <p className="-mt-2 text-xs text-grafito-2">Elija un sector o un tipo para filtrar todo el tablero; elija un punto para ver sus registros.</p>
      <section>
        <h2 className="mb-2 font-bold [font-stretch:90%]">
          Puntos críticos <span className="text-sm font-medium text-grafito-2">(más de {numero(k.umbral_critico_kg_dia)} kg por día)</span>
        </h2>
        <Tabla
          filas={k.puntos_criticos.map((p) => ({ ...p, id: p.punto_id }))}
          vacio="Ningún punto supera el umbral en este periodo."
          columnas={[
            { titulo: 'Punto', celda: (p) => <Link className="font-semibold underline [font-stretch:85%]" to={enlace({ search: p.punto__codigo })}>{p.punto__codigo}</Link> },
            { titulo: 'Nombre', celda: (p) => p.punto__nombre },
            { titulo: 'Sector', celda: (p) => p.sector__nombre },
            { titulo: 'Promedio diario', derecha: true, celda: (p) => <span className="tinta font-semibold">{numero(p.promedio_dia)} kg</span> },
            { titulo: 'Total', derecha: true, celda: (p) => `${numero(p.total)} kg` },
          ]}
        />
      </section>
    </div>
  )
}

type FilaComp = { id: number; nombre: string; base_kg: string; comparacion_kg: string; variacion_kg: string; variacion_pct: number | null; tendencia_creciente: boolean }
type Comparacion = { sector: FilaComp[]; punto: FilaComp[]; tipo: FilaComp[] }

function Comparar() {
  const [p, setP] = useState({ base_desde: '', base_hasta: '', comp_desde: '', comp_hasta: '' })
  const [vista, setVista] = useState<'sector' | 'punto' | 'tipo'>('sector')
  const listo = Object.values(p).every(Boolean)
  const { data, error, cargando } = useCarga(
    () => (listo ? api<Comparacion>('analitica/comparacion/', { query: p }) : Promise.resolve(null)),
    [JSON.stringify(p)],
  )
  const set = (k: keyof typeof p, v: string) => setP({ ...p, [k]: v })

  return (
    <div className="flex flex-col gap-5">
      <div className="grid gap-5 rounded-hoja border border-filete bg-hoja p-5 md:grid-cols-2">
        <fieldset className="grid grid-cols-2 gap-3">
          <legend className="mb-2 font-bold">Periodo base</legend>
          <Campo etiqueta="Desde">
            <Entrada type="date" value={p.base_desde} onChange={(e) => set('base_desde', e.target.value)} />
          </Campo>
          <Campo etiqueta="Hasta">
            <Entrada type="date" value={p.base_hasta} onChange={(e) => set('base_hasta', e.target.value)} />
          </Campo>
        </fieldset>
        <fieldset className="grid grid-cols-2 gap-3">
          <legend className="mb-2 font-bold">Periodo a comparar</legend>
          <Campo etiqueta="Desde">
            <Entrada type="date" value={p.comp_desde} onChange={(e) => set('comp_desde', e.target.value)} />
          </Campo>
          <Campo etiqueta="Hasta">
            <Entrada type="date" value={p.comp_hasta} onChange={(e) => set('comp_hasta', e.target.value)} />
          </Campo>
        </fieldset>
      </div>
      {!listo && <Aviso>Elija los dos periodos para ver la variación por sector, punto y tipo de residuo.</Aviso>}
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && listo && !data && <Cargando />}
      {data && (
        <>
          <div className="flex items-end justify-between gap-3">
            <Campo etiqueta="Comparar por">
              <Seleccion value={vista} onChange={(e) => setVista(e.target.value as typeof vista)} className="w-48">
                <option value="sector">Sector</option>
                <option value="punto">Punto</option>
                <option value="tipo">Tipo de residuo</option>
              </Seleccion>
            </Campo>
            <p className="flex items-center gap-1.5 text-xs text-grafito-2">
              <TrendingUp className="size-4 text-dsu" aria-hidden /> crecimiento sostenido 4 meses seguidos
            </p>
          </div>
          <Tabla
            filas={data[vista]}
            columnas={[
              {
                titulo: vista === 'punto' ? 'Punto' : vista === 'tipo' ? 'Tipo' : 'Sector',
                celda: (f) => (
                  <span className="inline-flex items-center gap-1.5 font-semibold">
                    {f.nombre}
                    {f.tendencia_creciente && <TrendingUp className="size-4 text-dsu" aria-label="Tendencia creciente sostenida" />}
                  </span>
                ),
              },
              { titulo: `Base (${fecha(p.base_desde)} – ${fecha(p.base_hasta)})`, derecha: true, celda: (f) => `${numero(f.base_kg)} kg` },
              { titulo: 'Comparado', derecha: true, celda: (f) => <span className="tinta font-semibold">{numero(f.comparacion_kg)} kg</span> },
              { titulo: 'Variación', derecha: true, celda: (f) => `${Number(f.variacion_kg) > 0 ? '+' : ''}${numero(f.variacion_kg)} kg` },
              { titulo: '%', derecha: true, celda: (f) => (f.variacion_pct === null ? 'nuevo' : `${f.variacion_pct > 0 ? '+' : ''}${numero(f.variacion_pct)}%`) },
            ]}
          />
        </>
      )}
    </div>
  )
}

/** RD8: el informe publicado en Power BI, insertado; cada usuario entra con su cuenta de Power BI. */
function PowerBI() {
  const { data, error, cargando } = useCarga(() => api<{ url: string }>('analitica/powerbi/'), [])
  if (cargando && !data) return <Cargando />
  if (error) return <Aviso tono="error">{error}</Aviso>
  if (!data?.url)
    return (
      <Vacio titulo="El informe de Power BI aún no está publicado">
        Cuando se publique, el administrador pega su enlace en Parámetros → Power BI y aparecerá aquí.
      </Vacio>
    )
  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-grafito-2">Requiere iniciar sesión con una cuenta de Power BI de la institución. Si no carga, ábralo en una pestaña aparte.</p>
        <a href={data.url} target="_blank" rel="noreferrer" className="inline-flex min-h-10 items-center gap-2 rounded-hoja border border-filete bg-hoja px-4 text-sm font-semibold hover:border-grafito-2">
          <ExternalLink className="size-4" aria-hidden /> Abrir en Power BI
        </a>
      </div>
      <iframe title="Tablero en Power BI" src={data.url} className="h-[min(78vh,760px)] w-full rounded-hoja border border-filete bg-hoja" allowFullScreen />
    </div>
  )
}

export function Tablero() {
  const [pestana, setPestana] = useState<'resumen' | 'comparar' | 'powerbi'>('resumen')
  const [filtros, setFiltros] = useState<Filtros>(() => filtrosIniciales())
  return (
    <>
      <Encabezado titulo="Tablero de gestión" detalle="Indicadores calculados sobre los registros depurados por el proceso ETL." />
      <div role="tablist" aria-label="Vistas del tablero" className="mb-5 flex gap-1 border-b border-filete">
        {(
          [
            ['resumen', 'Indicadores del periodo'],
            ['comparar', 'Comparar periodos'],
            ['powerbi', 'Power BI'],
          ] as const
        ).map(([id, texto]) => (
          <button
            key={id}
            role="tab"
            aria-selected={pestana === id}
            onClick={() => setPestana(id)}
            className={cx('-mb-px min-h-11 border-b-2 px-4 text-sm font-semibold', pestana === id ? 'border-dsu text-grafito' : 'border-transparent text-grafito-2 hover:text-grafito')}
          >
            {texto}
          </button>
        ))}
      </div>
      {pestana === 'resumen' ? (
        <>
          <FiltrosAnalisis valor={filtros} cambiar={setFiltros} />
          <Resumen filtros={filtros} cambiar={setFiltros} />
        </>
      ) : pestana === 'comparar' ? (
        <Comparar />
      ) : (
        <PowerBI />
      )}
    </>
  )
}
