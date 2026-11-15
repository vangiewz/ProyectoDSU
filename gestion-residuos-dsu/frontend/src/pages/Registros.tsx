import { Plus } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router'

import { opcionesDe, type Opcion } from '../components/Crud'
import { Sello } from '../components/Sello'
import { Area, Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Paginacion, Seleccion, Tabla, cx } from '../components/ui'
import { api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fechaHora, numero, useCarga } from '../lib/datos'

type Registro = {
  id: number
  fecha_hora: string
  punto_codigo: string
  sector: string
  tipo_residuo_nombre: string
  cantidad: string
  unidad_simbolo: string
  registrado_por_nombre: string
  jornada_detalle: string
  observaciones: string
}
type Total = { tipo_residuo__nombre: string; unidad__magnitud: 'PESO' | 'VOLUMEN'; total: string; registros: number }

function useOpciones(recurso: string, texto: (f: Record<string, unknown>) => string) {
  const [o, setO] = useState<Opcion[]>([])
  useEffect(() => {
    void opcionesDe(recurso, texto).then(setO)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [recurso])
  return o
}

function Filtro({ etiqueta, valor, cambiar, opciones }: { etiqueta: string; valor: string; cambiar: (v: string) => void; opciones: Opcion[] }) {
  return (
    <Campo etiqueta={etiqueta}>
      <Seleccion value={valor} onChange={(e) => cambiar(e.target.value)}>
        <option value="">Todos</option>
        {opciones.map((o) => (
          <option key={o.valor} value={o.valor}>
            {o.texto}
          </option>
        ))}
      </Seleccion>
    </Campo>
  )
}

export function Historico() {
  const sectores = useOpciones('sectores/', (f) => `${f.codigo} · ${f.nombre}`)
  const tipos = useOpciones('tipos-residuo/', (f) => String(f.nombre))
  const [pagina, setPagina] = useState(1)
  const [params] = useSearchParams()
  const [f, setF] = useState(() => ({
    sector: params.get('sector') ?? '',
    tipo_residuo: params.get('tipo_residuo') ?? '',
    desde: params.get('desde') ?? '',
    hasta: params.get('hasta') ?? '',
    search: params.get('search') ?? '',
  }))
  const { data, error, cargando } = useCarga(
    () => api<Pagina<Registro> & { totales: Total[] }>('registros/', { query: { page: pagina, ...f } }),
    [pagina, JSON.stringify(f)],
  )
  const set = (k: keyof typeof f, v: string) => {
    setF((p) => ({ ...p, [k]: v }))
    setPagina(1)
  }

  return (
    <>
      <Encabezado titulo="Histórico de residuos" detalle="Cada vaciado registrado en campo. Las cantidades en tinta azul son las que capturó el personal." />
      <div className="mb-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        <Filtro etiqueta="Sector" valor={f.sector} cambiar={(v) => set('sector', v)} opciones={sectores} />
        <Filtro etiqueta="Tipo de residuo" valor={f.tipo_residuo} cambiar={(v) => set('tipo_residuo', v)} opciones={tipos} />
        <Campo etiqueta="Desde">
          <Entrada type="date" value={f.desde} onChange={(e) => set('desde', e.target.value)} />
        </Campo>
        <Campo etiqueta="Hasta">
          <Entrada type="date" value={f.hasta} onChange={(e) => set('hasta', e.target.value)} />
        </Campo>
        <Campo etiqueta="Punto">
          <Entrada type="search" placeholder="Código o nombre" value={f.search} onChange={(e) => set('search', e.target.value)} />
        </Campo>
      </div>
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && !data ? (
        <Cargando />
      ) : (
        data && (
          <>
            {data.totales.length > 0 && (
              <dl className="mb-4 flex flex-wrap gap-x-8 gap-y-3 rounded-hoja border border-filete bg-hoja px-5 py-4">
                {data.totales.map((t) => (
                  <div key={t.tipo_residuo__nombre + t.unidad__magnitud}>
                    <dt className="rotulo">{t.tipo_residuo__nombre}</dt>
                    <dd className="tinta mt-0.5 text-xl font-bold">
                      {numero(t.total)} {t.unidad__magnitud === 'PESO' ? 'kg' : 'L'}
                      <span className="ml-1.5 text-xs font-medium text-grafito-2">{t.registros} reg.</span>
                    </dd>
                  </div>
                ))}
              </dl>
            )}
            <Tabla
              filas={data.results}
              vacio="No hay registros con estos filtros."
              columnas={[
                { titulo: 'Fecha y hora', celda: (r) => <span className="whitespace-nowrap">{fechaHora(r.fecha_hora)}</span> },
                { titulo: 'Punto', celda: (r) => <span className="font-semibold [font-stretch:85%]">{r.punto_codigo}</span> },
                { titulo: 'Sector', celda: (r) => r.sector },
                { titulo: 'Tipo', celda: (r) => r.tipo_residuo_nombre },
                {
                  titulo: 'Cantidad',
                  derecha: true,
                  celda: (r) => (
                    <span className="tinta font-semibold whitespace-nowrap">
                      {numero(r.cantidad)} {r.unidad_simbolo}
                    </span>
                  ),
                },
                { titulo: 'Registró', celda: (r) => r.registrado_por_nombre },
                { titulo: 'Observaciones', celda: (r) => <span className="line-clamp-1 text-grafito-2">{r.observaciones || '—'}</span> },
              ]}
            />
            <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
          </>
        )
      )}
    </>
  )
}

type Incidencia = {
  id: number
  fecha_hora: string
  punto: number
  punto_codigo: string
  sector: string
  tipo_display: string
  gravedad: string
  gravedad_display: string
  descripcion: string
  estado: 'PENDIENTE' | 'ATENDIDA'
  reportada_por_nombre: string
  accion_adoptada: string
}

const GRAVEDADES = ['BAJA', 'MEDIA', 'ALTA', 'CRITICA']
const TIPOS = [
  { valor: 'CONTENEDOR_DANADO', texto: 'Contenedor dañado' },
  { valor: 'ACCESO_BLOQUEADO', texto: 'Acceso bloqueado' },
  { valor: 'MAL_SEGREGADO', texto: 'Residuos mal segregados' },
  { valor: 'RESIDUO_PELIGROSO', texto: 'Residuo peligroso' },
  { valor: 'DESBORDE', texto: 'Desborde' },
  { valor: 'OTRO', texto: 'Otro' },
]

function NuevaIncidencia({ listo }: { listo: () => void }) {
  const puntos = useOpciones('puntos/', (f) => `${f.codigo} · ${f.nombre}`)
  const [d, setD] = useState({ punto: '', tipo: '', gravedad: 'MEDIA', descripcion: '' })
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)
  async function enviar() {
    setEnviando(true)
    setError(null)
    try {
      await api('incidencias/', { body: d })
      listo()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setEnviando(false)
    }
  }
  return (
    <section className="mb-5 grid gap-3 rounded-hoja border border-filete bg-hoja p-5 sm:grid-cols-3">
      {error && (
        <div className="sm:col-span-3">
          <Aviso tono="error">{error}</Aviso>
        </div>
      )}
      <Filtro etiqueta="Punto" valor={d.punto} cambiar={(v) => setD({ ...d, punto: v })} opciones={puntos} />
      <Filtro etiqueta="Tipo" valor={d.tipo} cambiar={(v) => setD({ ...d, tipo: v })} opciones={TIPOS} />
      <Filtro etiqueta="Gravedad" valor={d.gravedad} cambiar={(v) => setD({ ...d, gravedad: v })} opciones={GRAVEDADES.map((g) => ({ valor: g, texto: g.toLowerCase() }))} />
      <div className="sm:col-span-3">
        <Campo etiqueta="Descripción">
          <Area value={d.descripcion} onChange={(e) => setD({ ...d, descripcion: e.target.value })} />
        </Campo>
      </div>
      <div>
        <Boton cargando={enviando} disabled={!d.punto || !d.tipo || !d.descripcion.trim()} onClick={() => void enviar()}>
          Registrar incidencia
        </Boton>
      </div>
    </section>
  )
}

export function Incidencias() {
  const { puede } = useAuth()
  const [pagina, setPagina] = useState(1)
  const [f, setF] = useState({ estado: 'PENDIENTE', gravedad: '' })
  const [version, setVersion] = useState(0)
  const [nueva, setNueva] = useState(false)
  const [atendiendo, setAtendiendo] = useState<number | null>(null)
  const [accion, setAccion] = useState('')
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const { data, error, cargando } = useCarga(() => api<Pagina<Incidencia>>('incidencias/', { query: { page: pagina, ...f } }), [pagina, JSON.stringify(f), version])

  async function atender(id: number) {
    try {
      await api(`incidencias/${id}/atender/`, { body: { accion_adoptada: accion } })
      setAviso({ tono: 'ok', texto: 'Incidencia atendida y asentada.' })
      setAtendiendo(null)
      setAccion('')
      setVersion((v) => v + 1)
    } catch (e) {
      setAviso({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    }
  }

  return (
    <>
      <Encabezado
        titulo="Incidencias operativas"
        detalle="Situaciones que afectan la recolección. Las pendientes esperan la acción del supervisor del sector."
        acciones={
          puede('operations.add_incidencia') && (
            <Boton variante="secundario" onClick={() => setNueva(!nueva)}>
              <Plus className="size-4" aria-hidden /> Reportar incidencia
            </Boton>
          )
        }
      />
      {aviso && (
        <div className="mb-4">
          <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>
        </div>
      )}
      {nueva && (
        <NuevaIncidencia
          listo={() => {
            setNueva(false)
            setAviso({ tono: 'ok', texto: 'Incidencia registrada.' })
            setVersion((v) => v + 1)
          }}
        />
      )}
      <div className="mb-4 grid max-w-md grid-cols-2 gap-3">
        <Filtro
          etiqueta="Estado"
          valor={f.estado}
          cambiar={(v) => setF({ ...f, estado: v })}
          opciones={[
            { valor: 'PENDIENTE', texto: 'Pendientes' },
            { valor: 'ATENDIDA', texto: 'Atendidas' },
          ]}
        />
        <Filtro etiqueta="Gravedad" valor={f.gravedad} cambiar={(v) => setF({ ...f, gravedad: v })} opciones={GRAVEDADES.map((g) => ({ valor: g, texto: g.toLowerCase() }))} />
      </div>
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && !data ? (
        <Cargando />
      ) : (
        data && (
          <>
            <Tabla
              filas={data.results}
              vacio={f.estado === 'PENDIENTE' ? 'No hay incidencias pendientes.' : 'No hay incidencias con estos filtros.'}
              columnas={[
                { titulo: 'Reportada', celda: (i) => <span className="whitespace-nowrap">{fechaHora(i.fecha_hora)}</span> },
                { titulo: 'Punto', celda: (i) => <span className="font-semibold [font-stretch:85%]">{i.punto_codigo}</span> },
                { titulo: 'Tipo', celda: (i) => i.tipo_display },
                {
                  titulo: 'Gravedad',
                  celda: (i) => <span className={cx('font-semibold', (i.gravedad === 'ALTA' || i.gravedad === 'CRITICA') && 'text-dsu')}>{i.gravedad_display}</span>,
                },
                {
                  titulo: 'Descripción',
                  celda: (i) => (
                    <div className="max-w-sm">
                      <p className="tinta">{i.descripcion}</p>
                      {i.accion_adoptada && <p className="mt-1 text-xs text-grafito-2">Acción: {i.accion_adoptada}</p>}
                    </div>
                  ),
                },
                { titulo: 'Reportó', celda: (i) => i.reportada_por_nombre },
                {
                  titulo: 'Estado',
                  celda: (i) =>
                    i.estado === 'ATENDIDA' ? (
                      <Sello estado="ATENDIDA" />
                    ) : atendiendo === i.id ? (
                      <div className="flex min-w-56 flex-col gap-2">
                        <Entrada autoFocus placeholder="Acción adoptada" value={accion} onChange={(e) => setAccion(e.target.value)} />
                        <div className="flex gap-1">
                          <Boton disabled={!accion.trim()} onClick={() => void atender(i.id)}>
                            Asentar
                          </Boton>
                          <Boton variante="fantasma" onClick={() => setAtendiendo(null)}>
                            Cancelar
                          </Boton>
                        </div>
                      </div>
                    ) : puede('operations.atender_incidencia') ? (
                      <Boton variante="secundario" onClick={() => setAtendiendo(i.id)}>
                        Atender
                      </Boton>
                    ) : (
                      <Sello estado="PENDIENTE" />
                    ),
                },
              ]}
            />
            <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
          </>
        )
      )}
    </>
  )
}
