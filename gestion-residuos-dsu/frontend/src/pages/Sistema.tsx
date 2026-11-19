import { Play } from 'lucide-react'
import { useEffect, useState, type FormEvent } from 'react'
import { Link } from 'react-router'

import { Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Paginacion, Tabla, cx } from '../components/ui'
import { ApiError, api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fechaHora, useCarga } from '../lib/datos'

type Ejecucion = {
  id: number
  inicio: string
  fin: string | null
  estado: 'EN_CURSO' | 'EXITOSA' | 'CON_ALERTA' | 'SIN_CAMBIOS' | 'FALLIDA'
  estado_display: string
  disparada_por_nombre: string
  procesados: number
  aceptados: number
  observados: number
  duplicados: number
  atipicos: number
  mensaje: string
  duracion_segundos: number | null
}

const TINTA_ESTADO: Record<Ejecucion['estado'], string> = {
  EN_CURSO: 'text-boligrafo',
  EXITOSA: 'text-sello-ok',
  CON_ALERTA: 'text-sello-omit',
  SIN_CAMBIOS: 'text-grafito-2',
  FALLIDA: 'text-dsu',
}

export function ProcesoETL() {
  const { puede } = useAuth()
  const [pagina, setPagina] = useState(1)
  const [version, setVersion] = useState(0)
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [lanzando, setLanzando] = useState(false)
  const { data, error, cargando } = useCarga(() => api<Pagina<Ejecucion>>('etl/', { query: { page: pagina } }), [pagina, version])
  const enCurso = data?.results.some((e) => e.estado === 'EN_CURSO')

  // Mientras haya una ejecución en curso, se consulta su avance cada 3 s.
  useEffect(() => {
    if (!enCurso) return
    const t = setInterval(() => setVersion((v) => v + 1), 3000)
    return () => clearInterval(t)
  }, [enCurso])

  async function ejecutar() {
    setLanzando(true)
    setAviso(null)
    try {
      await api('etl/ejecutar/', { body: {} })
      setAviso({ tono: 'ok', texto: 'Proceso iniciado en segundo plano. La captura en campo sigue disponible.' })
      setVersion((v) => v + 1)
    } catch (e) {
      setAviso({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    } finally {
      setLanzando(false)
    }
  }

  return (
    <>
      <Encabezado
        titulo="Procesamiento de datos (ETL)"
        detalle="Depura los registros de campo, estandariza unidades, deriva variables del calendario y marca atípicos. Corre de forma programada y también a pedido."
        acciones={
          puede('analytics.ejecutar_etl') && (
            <Boton onClick={() => void ejecutar()} cargando={lanzando} disabled={enCurso}>
              <Play className="size-4" aria-hidden /> {enCurso ? 'En curso…' : 'Ejecutar ahora'}
            </Boton>
          )
        }
      />
      {aviso && (
        <div className="mb-4">
          <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>
        </div>
      )}
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && !data ? (
        <Cargando />
      ) : (
        data && (
          <>
            <Tabla
              filas={data.results}
              vacio="El proceso aún no se ha ejecutado."
              columnas={[
                { titulo: 'Inicio', celda: (e) => <span className="whitespace-nowrap">{fechaHora(e.inicio)}</span> },
                { titulo: 'Estado', celda: (e) => <span className={cx('font-semibold', TINTA_ESTADO[e.estado])}>{e.estado_display}</span> },
                { titulo: 'Procesados', derecha: true, celda: (e) => e.procesados },
                { titulo: 'Aceptados', derecha: true, celda: (e) => e.aceptados },
                {
                  titulo: 'Observados',
                  derecha: true,
                  celda: (e) => (
                    <span title={`${e.duplicados} duplicados · ${e.atipicos} atípicos`}>
                      {e.observados}
                      {e.observados > 0 && <span className="ml-1 text-xs text-grafito-2">({e.duplicados} dup. · {e.atipicos} atíp.)</span>}
                    </span>
                  ),
                },
                { titulo: 'Duración', derecha: true, celda: (e) => (e.duracion_segundos === null ? '—' : `${e.duracion_segundos} s`) },
                { titulo: 'Origen', celda: (e) => e.disparada_por_nombre },
                { titulo: 'Resultado', celda: (e) => <span className="text-grafito-2">{e.mensaje}</span> },
              ]}
            />
            <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
          </>
        )
      )}
    </>
  )
}

type Parametros = {
  umbral_critico_kg_dia: string
  tolerancia_capacidad: string
  etl_periodicidad_horas: number
  etl_umbral_observados_pct: string
  min_registros_entrenamiento: number
  umbral_r2_modelo: string
  horizonte_max_dias: number
  alerta_capacidad_pct: string
  crecimiento_alerta_pct: string
  no_aprovechable_max_pct: string
  url_powerbi: string
  actualizado_en: string
}

const CAMPOS: { nombre: keyof Parametros; etiqueta: string; ayuda: string; paso: string; grupo: string; tipo?: 'url' }[] = [
  { nombre: 'umbral_critico_kg_dia', etiqueta: 'Umbral de punto crítico (kg por día)', ayuda: 'Un punto es crítico si su promedio diario lo supera.', paso: '0.1', grupo: 'Operación' },
  { nombre: 'tolerancia_capacidad', etiqueta: 'Tolerancia sobre la capacidad del punto', ayuda: 'Entre 1 y 5. Un vaciado mayor a capacidad × tolerancia se rechaza.', paso: '0.1', grupo: 'Operación' },
  { nombre: 'etl_periodicidad_horas', etiqueta: 'Periodicidad del ETL (horas)', ayuda: 'Entre 1 y 168. La ejecución programada respeta este intervalo.', paso: '1', grupo: 'Procesamiento' },
  { nombre: 'etl_umbral_observados_pct', etiqueta: 'Umbral de registros observados (%)', ayuda: 'Por encima, la ejecución queda con alerta para revisión.', paso: '0.5', grupo: 'Procesamiento' },
  { nombre: 'min_registros_entrenamiento', etiqueta: 'Registros mínimos para entrenar', ayuda: 'Volumen necesario antes de entrenar el modelo predictivo.', paso: '1', grupo: 'Modelo predictivo' },
  { nombre: 'umbral_r2_modelo', etiqueta: 'R² mínimo para publicar', ayuda: 'Entre 0 y 1. Un modelo por debajo no se publica.', paso: '0.01', grupo: 'Modelo predictivo' },
  { nombre: 'horizonte_max_dias', etiqueta: 'Horizonte máximo de predicción (días)', ayuda: 'Entre 1 y 30.', paso: '1', grupo: 'Modelo predictivo' },
  { nombre: 'alerta_capacidad_pct', etiqueta: 'Ocupación que activa una alerta (%)', ayuda: 'Entre 10 y 100. Desde este porcentaje de la capacidad se emite una alerta de urgencia baja.', paso: '1', grupo: 'Alertas y recomendaciones' },
  { nombre: 'crecimiento_alerta_pct', etiqueta: 'Crecimiento que sugiere más frecuencia (%)', ayuda: 'Respecto del promedio de los últimos 28 días.', paso: '1', grupo: 'Alertas y recomendaciones' },
  { nombre: 'no_aprovechable_max_pct', etiqueta: 'Residuo no aprovechable tolerado (%)', ayuda: 'Por encima se recomienda reforzar la separación en origen.', paso: '1', grupo: 'Alertas y recomendaciones' },
  { nombre: 'url_powerbi', etiqueta: 'Enlace del informe de Power BI', ayuda: 'En Power BI: Archivo → Insertar informe → Sitio web o portal. Se muestra en el Tablero; vacío si aún no se publicó.', paso: '', grupo: 'Power BI', tipo: 'url' },
]

export function ParametrosPage() {
  const { puede } = useAuth()
  const editable = puede('catalogs.change_parametrossistema')
  const { data, error, cargando, setData } = useCarga(() => api<Parametros>('parametros/'), [])
  const [valores, setValores] = useState<Partial<Parametros>>({})
  const [errores, setErrores] = useState<Record<string, string>>({})
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [guardando, setGuardando] = useState(false)

  async function guardar(e: FormEvent) {
    e.preventDefault()
    setGuardando(true)
    setErrores({})
    setAviso(null)
    try {
      const nuevo = await api<Parametros>('parametros/', { method: 'PATCH', body: valores })
      setData(nuevo)
      setValores({})
      setAviso({ tono: 'ok', texto: 'Parámetros guardados. Se aplican desde la próxima operación y quedaron en la bitácora.' })
    } catch (err) {
      if (err instanceof ApiError && err.data && typeof err.data === 'object') {
        setErrores(Object.fromEntries(Object.entries(err.data as Record<string, string[]>).map(([k, v]) => [k, [v].flat().join(' ')])))
      }
      setAviso({ tono: 'error', texto: 'Revise los valores marcados: alguno está fuera del rango admitido.' })
    } finally {
      setGuardando(false)
    }
  }

  if (cargando && !data) return <Cargando />
  if (error || !data) return <Aviso tono="error">{error ?? 'No se pudieron cargar los parámetros.'}</Aviso>

  const grupos = [...new Set(CAMPOS.map((c) => c.grupo))]
  return (
    <>
      <Encabezado
        titulo="Parámetros del sistema"
        detalle={`Umbrales y configuración que gobiernan el análisis y la predicción. Última modificación: ${fechaHora(data.actualizado_en)}.`}
      />
      {aviso && (
        <div className="mb-4">
          <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>
        </div>
      )}
      <form onSubmit={guardar} className="flex max-w-3xl flex-col gap-5">
        {grupos.map((g) => (
          <fieldset key={g} className="grid gap-4 rounded-hoja border border-filete bg-hoja p-5 sm:grid-cols-2">
            <legend className="px-1 font-bold">{g}</legend>
            {CAMPOS.filter((c) => c.grupo === g).map((c) => (
              <Campo key={c.nombre} etiqueta={c.etiqueta} ayuda={c.ayuda} error={errores[c.nombre]}>
                <Entrada
                  type={c.tipo ?? 'number'}
                  inputMode={c.tipo ? 'url' : 'decimal'}
                  placeholder={c.tipo ? 'https://app.powerbi.com/reportEmbed?…' : undefined}
                  step={c.paso || undefined}
                  disabled={!editable}
                  value={String(valores[c.nombre] ?? data[c.nombre])}
                  onChange={(e) => setValores({ ...valores, [c.nombre]: e.target.value })}
                />
              </Campo>
            ))}
          </fieldset>
        ))}
        <p className="text-sm text-grafito-2">
          Los periodos académicos se administran en <Link to="/tipos-residuo" className="font-semibold underline">Catálogos</Link>.
        </p>
        {editable && (
          <div>
            <Boton type="submit" cargando={guardando} disabled={!Object.keys(valores).length}>
              Guardar parámetros
            </Boton>
          </div>
        )}
      </form>
    </>
  )
}
