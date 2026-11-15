import { BellRing, TrendingUp } from 'lucide-react'
import { useEffect, useState, type FormEvent } from 'react'
import { Link } from 'react-router'

import { opcionesDe, type Opcion } from '../components/Crud'
import { Estimado } from '../components/Estimado'
import { BarrasHorizontales, Columnas, LAPIZ } from '../components/Graficos'
import { Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Seleccion, Tabla, Vacio } from '../components/ui'
import { api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fecha, fechaHora, numero, useCarga } from '../lib/datos'

type Lote = {
  id: number
  version: number
  creado_en: string
  desde: string
  hasta: string
  sector_nombre: string | null
  punto_codigo: string | null
  solicitado_por_nombre: string
  puntos_omitidos: string[]
}

type Fila = { cantidad_kg: string; margen_kg: string }
type Detalle = Lote & {
  por_punto: (Fila & { punto_id: number; punto__codigo: string; punto__nombre: string; sector__nombre: string; punto__capacidad_kg: string })[]
  por_sector: (Fila & { sector_id: number; sector__codigo: string; sector__nombre: string })[]
  por_tipo: (Fila & { tipo_residuo_id: number; tipo_residuo__nombre: string })[]
  serie: (Fila & { fecha: string })[]
}

const fmtDia = new Intl.DateTimeFormat('es-BO', { day: '2-digit', month: 'short' })
const dia = (iso: string) => fmtDia.format(new Date(`${iso}T12:00`))
const alcance = (l: Lote) => l.punto_codigo ?? l.sector_nombre ?? 'Todos los puntos a su cargo'

function Solicitud({ alGenerar }: { alGenerar: (id: number) => void }) {
  const [horizonte, setHorizonte] = useState('7')
  const [sector, setSector] = useState('')
  const [punto, setPunto] = useState('')
  const [sectores, setSectores] = useState<Opcion[]>([])
  const [puntos, setPuntos] = useState<Opcion[]>([])
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    void opcionesDe('sectores/', (f) => `${f.codigo} · ${f.nombre}`).then(setSectores)
  }, [])
  useEffect(() => {
    void opcionesDe('puntos/', (f) => `${f.codigo} · ${f.nombre}`, sector ? { sector, is_active: 'true' } : { is_active: 'true' }).then(setPuntos)
  }, [sector])

  async function enviar(e: FormEvent) {
    e.preventDefault()
    setEnviando(true)
    setError(null)
    try {
      const lote = await api<Detalle>('predicciones/', { body: { horizonte: Number(horizonte), sector: sector || null, punto: punto || null } })
      alGenerar(lote.id)
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={enviar} className="mb-6 rounded-hoja border border-filete bg-hoja p-5">
      <div className="grid items-end gap-4 sm:grid-cols-2 lg:grid-cols-[10rem_minmax(0,1fr)_minmax(0,1fr)_auto]">
        <Campo etiqueta="Horizonte (días)">
          <Entrada type="number" inputMode="numeric" min={1} max={30} required value={horizonte} onChange={(e) => setHorizonte(e.target.value)} />
        </Campo>
        <Campo etiqueta="Sector">
          <Seleccion
            value={sector}
            onChange={(e) => {
              setSector(e.target.value)
              setPunto('')
            }}
          >
            <option value="">Todos</option>
            {sectores.map((o) => (
              <option key={o.valor} value={o.valor}>
                {o.texto}
              </option>
            ))}
          </Seleccion>
        </Campo>
        <Campo etiqueta="Punto">
          <Seleccion value={punto} onChange={(e) => setPunto(e.target.value)}>
            <option value="">Todos</option>
            {puntos.map((o) => (
              <option key={o.valor} value={o.valor}>
                {o.texto}
              </option>
            ))}
          </Seleccion>
        </Campo>
        <Boton type="submit" cargando={enviando}>
          <TrendingUp className="size-4" aria-hidden /> Generar predicción
        </Boton>
      </div>
      {error && (
        <div className="mt-4">
          <Aviso tono="error">{error}</Aviso>
        </div>
      )}
    </form>
  )
}

function Resultado({ id }: { id: number }) {
  const { data, error, cargando } = useCarga(() => api<Detalle>(`predicciones/${id}/`), [id])
  const { data: recs } = useCarga(() => api<Pagina<unknown>>('recomendaciones/', { query: { lote: id, estado: 'PENDIENTE', page_size: 1 } }), [id])
  if (cargando && !data) return <Cargando texto="Cargando la predicción…" />
  if (error || !data) return <Aviso tono="error">{error ?? 'No se pudo cargar la predicción.'}</Aviso>

  const total = data.por_sector.reduce((s, f) => s + Number(f.cantidad_kg), 0)
  const margenTotal = Math.sqrt(data.por_sector.reduce((s, f) => s + Number(f.margen_kg) ** 2, 0))
  return (
    <div className="flex flex-col gap-6">
      <section className="flex flex-wrap items-end justify-between gap-4 rounded-hoja border border-filete bg-hoja px-5 py-4">
        <div>
          <p className="text-sm text-grafito-2">
            {alcance(data)} · del {fecha(data.desde)} al {fecha(data.hasta)}
          </p>
          <p className="mt-1 text-[1.9rem] leading-tight font-bold [font-stretch:88%]">
            <Estimado valor={total} margen={margenTotal} />
          </p>
          <p className="mt-1 text-xs text-grafito-2">
            Modelo v{data.version} · solicitada por {data.solicitado_por_nombre} el {fechaHora(data.creado_en)}
          </p>
        </div>
        {recs && recs.count > 0 && (
          <Link to="/recomendaciones" className="inline-flex min-h-10 items-center gap-2 rounded-hoja border border-dsu/50 px-4 text-sm font-semibold text-dsu hover:bg-dsu hover:text-white">
            <BellRing className="size-4" aria-hidden /> {recs.count} recomendación(es) por resolver
          </Link>
        )}
      </section>
      {data.puntos_omitidos.length > 0 && (
        <Aviso>Sin historial reciente suficiente, no se estimaron: {data.puntos_omitidos.join(', ')}.</Aviso>
      )}
      <Columnas
        titulo="Generación proyectada por día de recolección"
        unidad="kg"
        tinta={LAPIZ}
        datos={data.serie.map((f) => ({ etiqueta: dia(f.fecha), valor: Number(f.cantidad_kg), margen: Number(f.margen_kg) }))}
      />
      <div className="grid gap-6 lg:grid-cols-2">
        <BarrasHorizontales
          titulo="Por sector"
          unidad="kg"
          tinta={LAPIZ}
          datos={[...data.por_sector]
            .sort((a, b) => Number(b.cantidad_kg) - Number(a.cantidad_kg))
            .map((f) => ({ etiqueta: f.sector__codigo, detalle: f.sector__nombre, valor: Number(f.cantidad_kg), margen: Number(f.margen_kg) }))}
        />
        <BarrasHorizontales
          titulo="Por tipo de residuo"
          unidad="kg"
          tinta={LAPIZ}
          datos={[...data.por_tipo]
            .sort((a, b) => Number(b.cantidad_kg) - Number(a.cantidad_kg))
            .map((f) => ({ etiqueta: f.tipo_residuo__nombre, valor: Number(f.cantidad_kg), margen: Number(f.margen_kg) }))}
        />
      </div>
      <section>
        <h2 className="mb-2 font-bold [font-stretch:90%]">Por punto de recolección</h2>
        <Tabla
          filas={data.por_punto.map((f) => ({ ...f, id: f.punto_id }))}
          columnas={[
            { titulo: 'Punto', celda: (f) => <span className="font-semibold [font-stretch:85%]">{f.punto__codigo}</span> },
            { titulo: 'Nombre', celda: (f) => f.punto__nombre },
            { titulo: 'Sector', celda: (f) => f.sector__nombre },
            { titulo: 'Generación en el horizonte', derecha: true, celda: (f) => <Estimado valor={f.cantidad_kg} margen={f.margen_kg} /> },
            { titulo: 'Capacidad del punto', derecha: true, celda: (f) => `${numero(f.punto__capacidad_kg)} kg` },
          ]}
        />
      </section>
    </div>
  )
}

export function Predicciones() {
  const { puede } = useAuth()
  const [version, setVersion] = useState(0)
  const [elegido, setElegido] = useState<number | null>(null)
  const { data, error, cargando } = useCarga(() => api<Pagina<Lote>>('predicciones/', { query: { page_size: 20 } }), [version])
  const id = elegido ?? data?.results[0]?.id ?? null

  return (
    <>
      <Encabezado
        titulo="Predicción de generación"
        detalle="Estimaciones de apoyo a la planificación: cada cifra va a lápiz, con su margen de error y la versión del modelo que la produjo. No reemplazan el criterio del supervisor."
      />
      {puede('prediction.generar_prediccion') && (
        <Solicitud
          alGenerar={(nuevo) => {
            setElegido(nuevo)
            setVersion((v) => v + 1)
          }}
        />
      )}
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && !data && <Cargando />}
      {data && !data.results.length && (
        <Vacio titulo="Aún no se generaron predicciones">Defina el horizonte y el alcance, y genere la primera.</Vacio>
      )}
      {data && id !== null && (
        <>
          {data.results.length > 1 && (
            <div className="mb-4 max-w-xl">
              <Campo etiqueta="Predicción consultada">
                <Seleccion value={id} onChange={(e) => setElegido(Number(e.target.value))}>
                  {data.results.map((l) => (
                    <option key={l.id} value={l.id}>
                      {fechaHora(l.creado_en)} · {alcance(l)} · {dia(l.desde)}–{dia(l.hasta)} · v{l.version}
                    </option>
                  ))}
                </Seleccion>
              </Campo>
            </div>
          )}
          <Resultado key={id} id={id} />
        </>
      )}
    </>
  )
}
