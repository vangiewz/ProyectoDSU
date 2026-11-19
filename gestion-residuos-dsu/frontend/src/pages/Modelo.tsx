import { Trees, Undo2 } from 'lucide-react'
import { useEffect, useState, type FormEvent } from 'react'

import { BarrasHorizontales, LAPIZ } from '../components/Graficos'
import { Sello, type EstadoSello } from '../components/Sello'
import { Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Paginacion, Tabla, cx } from '../components/ui'
import { ApiError, api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fecha, fechaHora, numero, useCarga } from '../lib/datos'

type Hiper = { n_estimators: number; max_depth: number; min_samples_leaf: number }

export type Version = {
  id: number
  version: number
  estado: 'EN_CURSO' | 'APROBADO' | 'RECHAZADO' | 'FALLIDO'
  estado_display: string
  vigente: boolean
  inicio: string
  fin: string | null
  entrenado_por_nombre: string
  hiperparametros: Hiper
  variables: string[]
  registros: number
  observaciones_entrenamiento: number
  observaciones_prueba: number
  corte: string | null
  mae: number | null
  mse: number | null
  rmse: number | null
  r2: number | null
  umbral_r2: string | null
  importancias: Record<string, number>
  mensaje: string
}

const SELLO: Record<Version['estado'], EstadoSello> = { EN_CURSO: 'EN CURSO', APROBADO: 'APROBADO', RECHAZADO: 'RECHAZADO', FALLIDO: 'FALLIDO' }

// Nombre de cada variable predictora tal como la entiende la dirección (RF22).
const VARIABLE: Record<string, string> = {
  promedio_28d: 'Cantidad histórica',
  frecuencia_semanal: 'Frecuencia',
  en_periodo: 'Periodo académico',
  dia_semana: 'Día de la semana',
  semana_anio: 'Semana del año',
  dia_mes: 'Día del mes',
  mes: 'Mes',
  tipo_residuo_id: 'Tipo de residuo',
  punto_id: 'Punto de recolección',
  sector_id: 'Sector',
}

const HIPER: { nombre: keyof Hiper; etiqueta: string }[] = [
  { nombre: 'n_estimators', etiqueta: 'Número de árboles' },
  { nombre: 'max_depth', etiqueta: 'Profundidad máxima' },
  { nombre: 'min_samples_leaf', etiqueta: 'Observaciones mínimas por hoja' },
]

const metrica = (v: number | null, d = 3) => (v === null ? '—' : v.toLocaleString('es-BO', { minimumFractionDigits: d, maximumFractionDigits: d }))

function Ficha({ v }: { v: Version }) {
  const alcanza = v.r2 !== null && v.umbral_r2 !== null && v.r2 >= Number(v.umbral_r2)
  return (
    <section className="rounded-hoja border border-filete bg-hoja">
      <header className="flex flex-wrap items-center gap-x-4 gap-y-2 border-b border-filete px-5 py-4">
        <h2 className="text-lg font-bold [font-stretch:88%]">Versión {v.version}</h2>
        {v.vigente ? <Sello estado="VIGENTE" /> : <Sello estado={SELLO[v.estado]} />}
        <p className="text-sm text-grafito-2">
          Entrenada el {fechaHora(v.inicio)} · {v.entrenado_por_nombre}
        </p>
      </header>
      <dl className="grid grid-cols-2 gap-x-6 gap-y-4 px-5 py-5 sm:grid-cols-4">
        <div>
          <dt className="rotulo">Coef. de determinación R²</dt>
          <dd className={cx('mt-1 text-[1.75rem] leading-none font-bold [font-stretch:88%]', alcanza ? 'text-sello-ok' : 'text-sello-omit')}>{metrica(v.r2)}</dd>
          <dd className="mt-1 text-xs text-grafito-2">Umbral para publicar: {metrica(Number(v.umbral_r2), 2)}</dd>
        </div>
        <div>
          <dt className="rotulo">Raíz del error cuadrático (RMSE)</dt>
          <dd className="mt-1 text-[1.75rem] leading-none font-bold [font-stretch:88%]">{metrica(v.rmse, 2)} kg</dd>
          <dd className="mt-1 text-xs text-grafito-2">Margen de cada estimación diaria</dd>
        </div>
        <div>
          <dt className="rotulo">Error absoluto medio (MAE)</dt>
          <dd className="mt-1 text-[1.75rem] leading-none font-bold [font-stretch:88%]">{metrica(v.mae, 2)} kg</dd>
        </div>
        <div>
          <dt className="rotulo">Error cuadrático medio (MSE)</dt>
          <dd className="mt-1 text-[1.75rem] leading-none font-bold [font-stretch:88%]">{metrica(v.mse, 2)}</dd>
        </div>
      </dl>
      <p className="border-t border-filete-suave px-5 py-3 text-sm text-grafito-2">
        {numero(v.registros)} registros depurados · {numero(v.observaciones_entrenamiento)} observaciones de entrenamiento y{' '}
        {numero(v.observaciones_prueba)} de prueba{v.corte && <> (desde el {fecha(v.corte)}, en orden cronológico)</>} ·{' '}
        {v.hiperparametros.n_estimators} árboles, profundidad {v.hiperparametros.max_depth}, {v.hiperparametros.min_samples_leaf} obs. por hoja
      </p>
      {v.mensaje && (
        <div className="px-5 pb-4">
          <Aviso tono={v.estado === 'APROBADO' ? 'ok' : v.estado === 'EN_CURSO' ? 'info' : 'error'}>{v.mensaje}</Aviso>
        </div>
      )}
    </section>
  )
}

function Entrenar({ enCurso, alIniciar }: { enCurso: boolean; alIniciar: () => void }) {
  const { data: propuestos } = useCarga(() => api<{ valores: Hiper; limites: Record<keyof Hiper, [number, number]> }>('modelos/propuestos/'), [])
  const [valores, setValores] = useState<Partial<Record<keyof Hiper, string>>>({})
  const [errores, setErrores] = useState<Record<string, string>>({})
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [enviando, setEnviando] = useState(false)

  async function enviar(e: FormEvent) {
    e.preventDefault()
    if (!propuestos) return
    setEnviando(true)
    setErrores({})
    setAviso(null)
    try {
      await api('modelos/entrenar/', { body: { ...propuestos.valores, ...valores } })
      setAviso({ tono: 'ok', texto: 'Entrenamiento iniciado en segundo plano. La operación en campo no se ve afectada.' })
      alIniciar()
    } catch (err) {
      if (err instanceof ApiError && err.status === 400 && err.data && typeof err.data === 'object') {
        setErrores(Object.fromEntries(Object.entries(err.data as Record<string, string[]>).map(([k, v]) => [k, [v].flat().join(' ')])))
      }
      setAviso({ tono: 'error', texto: err instanceof Error ? err.message : String(err) })
    } finally {
      setEnviando(false)
    }
  }

  if (!propuestos) return null
  return (
    <form onSubmit={enviar} className="rounded-hoja border border-filete bg-hoja p-5">
      <h2 className="font-bold [font-stretch:90%]">Nuevo entrenamiento</h2>
      <p className="mt-1 mb-4 text-sm text-grafito-2">
        Se proponen los valores por defecto; ajústelos solo si conoce su efecto. Si el R² no alcanza el umbral, la versión vigente se conserva.
      </p>
      <div className="grid items-end gap-4 sm:grid-cols-[repeat(3,minmax(0,1fr))_auto]">
        {HIPER.map(({ nombre, etiqueta }) => {
          const [min, max] = propuestos.limites[nombre]
          return (
            <Campo key={nombre} etiqueta={etiqueta} ayuda={`Entre ${min} y ${max}.`} error={errores[nombre]}>
              <Entrada
                type="number"
                inputMode="numeric"
                min={min}
                max={max}
                value={valores[nombre] ?? String(propuestos.valores[nombre])}
                onChange={(e) => setValores({ ...valores, [nombre]: e.target.value })}
              />
            </Campo>
          )
        })}
        <Boton type="submit" cargando={enviando} disabled={enCurso} className="mb-5 sm:mb-6">
          <Trees className="size-4" aria-hidden /> {enCurso ? 'Entrenando…' : 'Entrenar'}
        </Boton>
      </div>
      {aviso && <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>}
    </form>
  )
}

export function ModeloPredictivo() {
  const { puede } = useAuth()
  const [pagina, setPagina] = useState(1)
  const [version, setVersion] = useState(0)
  const [elegida, setElegida] = useState<number | null>(null)
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [publicando, setPublicando] = useState<number | null>(null)
  const { data, error, cargando } = useCarga(() => api<Pagina<Version>>('modelos/', { query: { page: pagina } }), [pagina, version])
  const { data: vigentes } = useCarga(() => api<Pagina<Version>>('modelos/', { query: { vigente: true } }), [version])
  const enCurso = !!data?.results.some((v) => v.estado === 'EN_CURSO')
  const vigente = vigentes?.results[0] ?? null
  const detalle = data?.results.find((v) => v.id === elegida) ?? vigente

  // Mientras haya un entrenamiento en curso, se consulta su avance cada 3 s.
  useEffect(() => {
    if (!enCurso) return
    const t = setInterval(() => setVersion((v) => v + 1), 3000)
    return () => clearInterval(t)
  }, [enCurso])

  async function publicar(v: Version) {
    setPublicando(v.id)
    setAviso(null)
    try {
      await api(`modelos/${v.id}/publicar/`, { body: {} })
      setAviso({ tono: 'ok', texto: `La versión ${v.version} es ahora la vigente. Las próximas predicciones la usarán; el cambio quedó en la bitácora.` })
      setElegida(v.id)
      setVersion((x) => x + 1)
    } catch (e) {
      setAviso({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    } finally {
      setPublicando(null)
    }
  }

  // PostgreSQL (jsonb) no conserva el orden de las claves: se ordena aquí de mayor a menor.
  const importancias = Object.entries(detalle?.importancias ?? {})
    .sort((a, b) => b[1] - a[1])
    .map(([k, v]) => ({ etiqueta: VARIABLE[k] ?? k, valor: Math.round(v * 1000) / 10 }))

  return (
    <>
      <Encabezado
        titulo="Modelo predictivo"
        detalle="Random Forest Regressor entrenado sobre el histórico depurado. Una versión se publica solo si su R² alcanza el umbral; cualquier versión aprobada puede volver a publicarse."
      />
      <div className="flex flex-col gap-6">
        {puede('prediction.entrenar_modelo') && <Entrenar enCurso={enCurso} alIniciar={() => setVersion((v) => v + 1)} />}
        {aviso && <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>}
        {error && <Aviso tono="error">{error}</Aviso>}
        {cargando && !data ? (
          <Cargando />
        ) : (
          <>
            {detalle ? (
              <div className="grid gap-6 xl:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)]">
                <Ficha v={detalle} />
                <BarrasHorizontales titulo="Importancia de cada variable" unidad="%" datos={importancias} tinta={LAPIZ} />
              </div>
            ) : (
              <Aviso>Aún no hay un modelo publicado. Las predicciones y recomendaciones estarán disponibles cuando una versión alcance el umbral de R².</Aviso>
            )}
            {data && (
              <section>
                <h2 className="mb-2 font-bold [font-stretch:90%]">Versiones</h2>
                <Tabla
                  filas={data.results}
                  vacio="El modelo aún no se ha entrenado."
                  alSeleccionar={(v) => setElegida(v.id)}
                  columnas={[
                    {
                      titulo: 'Versión',
                      celda: (v) => <span className={cx('font-bold [font-stretch:85%]', v.id === detalle?.id && 'underline decoration-2 underline-offset-4')}>v{v.version}</span>,
                    },
                    { titulo: 'Estado', celda: (v) => (v.vigente ? <Sello estado="VIGENTE" /> : <Sello estado={SELLO[v.estado]} />) },
                    { titulo: 'R²', derecha: true, celda: (v) => metrica(v.r2) },
                    { titulo: 'RMSE', derecha: true, celda: (v) => (v.rmse === null ? '—' : `${metrica(v.rmse, 2)} kg`) },
                    { titulo: 'Entrenada', celda: (v) => <span className="whitespace-nowrap">{fechaHora(v.inicio)}</span> },
                    { titulo: 'Por', celda: (v) => v.entrenado_por_nombre },
                    {
                      titulo: '',
                      derecha: true,
                      celda: (v) =>
                        v.estado === 'APROBADO' &&
                        !v.vigente &&
                        puede('prediction.publicar_modelo') && (
                          <Boton
                            variante="secundario"
                            cargando={publicando === v.id}
                            onClick={(e) => {
                              e.stopPropagation()
                              void publicar(v)
                            }}
                          >
                            <Undo2 className="size-4" aria-hidden /> Publicar esta versión
                          </Boton>
                        ),
                    },
                  ]}
                />
                <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
              </section>
            )}
          </>
        )}
      </div>
    </>
  )
}
