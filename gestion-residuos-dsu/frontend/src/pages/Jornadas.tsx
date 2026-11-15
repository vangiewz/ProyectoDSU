import { ArrowDown, ArrowUp, ChevronLeft, Plus, Smartphone, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router'

import { opcionesDe, type Opcion } from '../components/Crud'
import { EjeJornada } from '../components/EjeJornada'
import { Sello, selloDeJornada } from '../components/Sello'
import { Area, Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Paginacion, Seleccion, Tabla, Vacio, cx } from '../components/ui'
import { api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fecha, hora, hoyISO, numero, useCarga } from '../lib/datos'
import type { Jornada, Resumen } from '../lib/tipos'

const TURNOS = [
  { valor: 'MANANA', texto: 'Mañana' },
  { valor: 'TARDE', texto: 'Tarde' },
  { valor: 'NOCHE', texto: 'Noche' },
]
const ESTADOS = [
  { valor: 'PLANIFICADA', texto: 'Planificada' },
  { valor: 'CONFIRMADA', texto: 'Confirmada' },
  { valor: 'EN_EJECUCION', texto: 'En ejecución' },
  { valor: 'CERRADA', texto: 'Cerrada' },
]

function useSectores() {
  const [s, setS] = useState<Opcion[]>([])
  useEffect(() => {
    void opcionesDe('sectores/', (f) => `${f.codigo} · ${f.nombre}`, { is_active: 'true' }).then(setS)
  }, [])
  return s
}

const cobertura = (j: Jornada) => (j.puntos_planificados ? Math.round((j.puntos_atendidos * 100) / j.puntos_planificados) : 0)

export function Jornadas() {
  const { puede } = useAuth()
  const navegar = useNavigate()
  const sectores = useSectores()
  const [pagina, setPagina] = useState(1)
  const [f, setF] = useState({ estado: '', sector: '', desde: '', hasta: '' })
  const { data, error, cargando } = useCarga(() => api<Pagina<Jornada>>('jornadas/', { query: { page: pagina, ...f } }), [pagina, JSON.stringify(f)])
  const set = (k: keyof typeof f, v: string) => {
    setF((p) => ({ ...p, [k]: v }))
    setPagina(1)
  }

  return (
    <>
      <Encabezado
        titulo="Jornadas de recolección"
        detalle="Planificación, ejecución e historial de las rutas por sector."
        acciones={
          puede('operations.add_jornada') && (
            <Boton onClick={() => navegar('/jornadas/nueva')}>
              <Plus className="size-4" aria-hidden /> Planificar jornada
            </Boton>
          )
        }
      />
      <div className="mb-4 grid gap-3 sm:grid-cols-4">
        <Campo etiqueta="Estado">
          <Seleccion value={f.estado} onChange={(e) => set('estado', e.target.value)}>
            <option value="">Todos</option>
            {ESTADOS.map((o) => (
              <option key={o.valor} value={o.valor}>
                {o.texto}
              </option>
            ))}
          </Seleccion>
        </Campo>
        <Campo etiqueta="Sector">
          <Seleccion value={f.sector} onChange={(e) => set('sector', e.target.value)}>
            <option value="">Todos</option>
            {sectores.map((o) => (
              <option key={o.valor} value={o.valor}>
                {o.texto}
              </option>
            ))}
          </Seleccion>
        </Campo>
        <Campo etiqueta="Desde">
          <Entrada type="date" value={f.desde} onChange={(e) => set('desde', e.target.value)} />
        </Campo>
        <Campo etiqueta="Hasta">
          <Entrada type="date" value={f.hasta} onChange={(e) => set('hasta', e.target.value)} />
        </Campo>
      </div>
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && !data ? (
        <Cargando />
      ) : (
        data && (
          <>
            <Tabla
              filas={data.results}
              vacio="No hay jornadas con estos filtros."
              alSeleccionar={(j) => navegar(`/jornadas/${j.id}`)}
              columnas={[
                { titulo: 'Fecha', celda: (j) => <span className="font-semibold whitespace-nowrap">{fecha(j.fecha)}</span> },
                { titulo: 'Turno', celda: (j) => j.turno_display },
                { titulo: 'Sector', celda: (j) => j.sector_nombre },
                { titulo: 'Responsable', celda: (j) => j.responsable_nombre || <span className="text-grafito-2">Sin asignar</span> },
                {
                  titulo: 'Cobertura',
                  derecha: true,
                  celda: (j) => (
                    <span>
                      <span className="tinta font-semibold">{j.puntos_atendidos}</span>
                      <span className="text-grafito-2"> / {j.puntos_planificados} · {cobertura(j)}%</span>
                    </span>
                  ),
                },
                { titulo: 'Estado', celda: (j) => <Sello estado={selloDeJornada(j.estado)} /> },
              ]}
            />
            <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
          </>
        )
      )}
    </>
  )
}

type PuntoSector = { id: number; codigo: string; nombre: string; is_active: boolean }

export function NuevaJornada() {
  const navegar = useNavigate()
  const sectores = useSectores()
  const [datos, setDatos] = useState({ fecha: hoyISO(), turno: 'MANANA', sector: '', descripcion: '' })
  const [ruta, setRuta] = useState<PuntoSector[]>([])
  const [error, setError] = useState<string | null>(null)
  const [guardando, setGuardando] = useState(false)
  const puntos = useCarga(
    () => (datos.sector ? api<Pagina<PuntoSector>>('puntos/', { query: { sector: datos.sector, is_active: 'true', page_size: 500 } }) : Promise.resolve(null)),
    [datos.sector],
  )

  const mover = (i: number, d: -1 | 1) =>
    setRuta((r) => {
      const n = [...r]
      ;[n[i], n[i + d]] = [n[i + d], n[i]]
      return n
    })

  async function guardar() {
    setGuardando(true)
    setError(null)
    try {
      const j = await api<Jornada>('jornadas/', { body: { ...datos, puntos: ruta.map((p) => p.id) } })
      navegar(`/jornadas/${j.id}`)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setGuardando(false)
    }
  }

  const disponibles = (puntos.data?.results ?? []).filter((p) => !ruta.some((r) => r.id === p.id))

  return (
    <>
      <Link to="/jornadas" className="mb-3 inline-flex items-center gap-1 text-sm text-grafito-2 hover:text-grafito">
        <ChevronLeft className="size-4" aria-hidden /> Jornadas
      </Link>
      <Encabezado titulo="Planificar jornada" detalle="Defina fecha, turno y sector, y arme la ruta en el orden en que se atenderá." />
      {error && (
        <div className="mb-4">
          <Aviso tono="error">{error}</Aviso>
        </div>
      )}
      <div className="grid items-start gap-5 lg:grid-cols-[340px_1fr]">
        <section className="flex flex-col gap-4 rounded-hoja border border-filete bg-hoja p-5">
          <Campo etiqueta="Fecha">
            <Entrada type="date" value={datos.fecha} onChange={(e) => setDatos({ ...datos, fecha: e.target.value })} />
          </Campo>
          <Campo etiqueta="Turno">
            <Seleccion value={datos.turno} onChange={(e) => setDatos({ ...datos, turno: e.target.value })}>
              {TURNOS.map((t) => (
                <option key={t.valor} value={t.valor}>
                  {t.texto}
                </option>
              ))}
            </Seleccion>
          </Campo>
          <Campo etiqueta="Sector">
            <Seleccion
              value={datos.sector}
              onChange={(e) => {
                setDatos({ ...datos, sector: e.target.value })
                setRuta([])
              }}
            >
              <option value="">— Seleccione —</option>
              {sectores.map((o) => (
                <option key={o.valor} value={o.valor}>
                  {o.texto}
                </option>
              ))}
            </Seleccion>
          </Campo>
          <Campo etiqueta="Indicaciones">
            <Area value={datos.descripcion} onChange={(e) => setDatos({ ...datos, descripcion: e.target.value })} />
          </Campo>
          <Boton onClick={() => void guardar()} cargando={guardando} disabled={!datos.sector || !ruta.length}>
            Guardar planificación
          </Boton>
        </section>

        <section className="grid gap-5 md:grid-cols-2">
          <div>
            <h2 className="rotulo mb-2">Puntos del sector</h2>
            {!datos.sector ? (
              <Vacio titulo="Elija un sector">Sus puntos activos aparecerán aquí.</Vacio>
            ) : puntos.cargando ? (
              <Cargando />
            ) : disponibles.length ? (
              <ul className="divide-y divide-filete-suave rounded-hoja border border-filete bg-hoja">
                {disponibles.map((p) => (
                  <li key={p.id}>
                    <button onClick={() => setRuta((r) => [...r, p])} className="flex min-h-12 w-full items-center gap-3 px-3 text-left text-sm hover:bg-papel">
                      <Plus className="size-4 text-grafito-2" aria-hidden />
                      <span className="font-semibold [font-stretch:85%]">{p.codigo}</span>
                      <span className="truncate text-grafito-2">{p.nombre}</span>
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <Vacio titulo="Todos los puntos están en la ruta" />
            )}
          </div>
          <div>
            <h2 className="rotulo mb-2">Ruta · {ruta.length} punto(s)</h2>
            {ruta.length ? (
              <ol className="divide-y divide-filete-suave rounded-hoja border border-filete bg-hoja">
                {ruta.map((p, i) => (
                  <li key={p.id} className="flex min-h-12 items-center gap-2 px-3 text-sm">
                    <span className="w-6 text-right font-bold text-grafito-2">{i + 1}.</span>
                    <span className="font-semibold [font-stretch:85%]">{p.codigo}</span>
                    <span className="flex-1 truncate text-grafito-2">{p.nombre}</span>
                    <button disabled={i === 0} onClick={() => mover(i, -1)} className="rounded p-1.5 hover:bg-papel disabled:opacity-30" aria-label={`Subir ${p.codigo}`}>
                      <ArrowUp className="size-4" />
                    </button>
                    <button disabled={i === ruta.length - 1} onClick={() => mover(i, 1)} className="rounded p-1.5 hover:bg-papel disabled:opacity-30" aria-label={`Bajar ${p.codigo}`}>
                      <ArrowDown className="size-4" />
                    </button>
                    <button onClick={() => setRuta((r) => r.filter((x) => x.id !== p.id))} className="rounded p-1.5 text-dsu hover:bg-dsu/5" aria-label={`Quitar ${p.codigo}`}>
                      <X className="size-4" />
                    </button>
                  </li>
                ))}
              </ol>
            ) : (
              <Vacio titulo="Ruta vacía">Toque los puntos del sector para agregarlos en orden.</Vacio>
            )}
          </div>
        </section>
      </div>
    </>
  )
}

function Asignacion({ jornada, alGuardar }: { jornada: Jornada; alGuardar: () => void }) {
  const [operarios, setOperarios] = useState<Opcion[]>([])
  const [vehiculos, setVehiculos] = useState<Opcion[]>([])
  const [personal, setPersonal] = useState<number[]>(jornada.personal)
  const [flota, setFlota] = useState<number[]>(jornada.vehiculos)
  const [responsable, setResponsable] = useState<string>(jornada.responsable ? String(jornada.responsable) : '')
  const [error, setError] = useState<string | null>(null)
  const [guardando, setGuardando] = useState(false)

  useEffect(() => {
    void opcionesDe('usuarios/', (f) => `${f.first_name} ${f.last_name}`, { groups__name: 'Operativo', is_active: 'true' }).then(setOperarios)
    void opcionesDe('vehiculos/', (f) => `${f.placa} · ${f.descripcion}`, { is_active: 'true', estado: 'OPERATIVO' }).then(setVehiculos)
  }, [])

  const alternar = (lista: number[], set: (l: number[]) => void, id: number) => set(lista.includes(id) ? lista.filter((x) => x !== id) : [...lista, id])

  async function guardar() {
    setGuardando(true)
    setError(null)
    try {
      await api(`jornadas/${jornada.id}/asignar/`, { body: { personal, vehiculos: flota, responsable: responsable ? Number(responsable) : null } })
      alGuardar()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setGuardando(false)
    }
  }

  const casilla = (o: Opcion, marcado: boolean, cambiar: () => void) => (
    <label key={o.valor} className="flex min-h-11 items-center gap-3 rounded-hoja border border-filete px-3 text-sm has-[:checked]:border-boligrafo has-[:checked]:text-boligrafo">
      <input type="checkbox" checked={marcado} onChange={cambiar} className="size-4" />
      {o.texto}
    </label>
  )

  return (
    <section className="flex flex-col gap-4 rounded-hoja border border-filete bg-hoja p-5">
      <h2 className="text-lg font-bold [font-stretch:90%]">Asignar cuadrilla y vehículos</h2>
      {error && <Aviso tono="error">{error}</Aviso>}
      <fieldset>
        <legend className="rotulo mb-2">Personal operativo</legend>
        <div className="grid gap-2 sm:grid-cols-2">{operarios.map((o) => casilla(o, personal.includes(Number(o.valor)), () => alternar(personal, setPersonal, Number(o.valor))))}</div>
      </fieldset>
      <Campo etiqueta="Responsable de la jornada">
        <Seleccion value={responsable} onChange={(e) => setResponsable(e.target.value)}>
          <option value="">— Seleccione del personal —</option>
          {operarios
            .filter((o) => personal.includes(Number(o.valor)))
            .map((o) => (
              <option key={o.valor} value={o.valor}>
                {o.texto}
              </option>
            ))}
        </Seleccion>
      </Campo>
      <fieldset>
        <legend className="rotulo mb-2">Vehículos</legend>
        <div className="grid gap-2 sm:grid-cols-2">{vehiculos.map((o) => casilla(o, flota.includes(Number(o.valor)), () => alternar(flota, setFlota, Number(o.valor))))}</div>
      </fieldset>
      <div>
        <Boton onClick={() => void guardar()} cargando={guardando}>
          Guardar asignación
        </Boton>
      </div>
    </section>
  )
}

function ResumenJornada({ id, version }: { id: number; version: number }) {
  const { data } = useCarga(() => api<Resumen>(`jornadas/${id}/resumen/`), [id, version])
  if (!data) return null
  const cifra = (valor: string | number, unidad: string, rotulo: string) => (
    <div>
      <p className="rotulo">{rotulo}</p>
      <p className="tinta mt-1 text-[1.75rem] leading-none font-bold">
        {numero(valor)} <span className="text-base font-semibold">{unidad}</span>
      </p>
    </div>
  )
  return (
    <section className="rounded-hoja border border-filete bg-hoja p-5">
      <h2 className="mb-4 text-lg font-bold [font-stretch:90%]">Consolidado</h2>
      <div className="grid grid-cols-2 gap-5 sm:grid-cols-4">
        {cifra(data.total_kg, 'kg', 'Recolectado (peso)')}
        {cifra(data.total_litros, 'L', 'Recolectado (volumen)')}
        {cifra(data.cobertura, '%', `Cobertura · ${data.atendidos} de ${data.planificados}`)}
        {cifra(data.incidencias, '', `Incidencias · ${data.incidencias_pendientes} pendientes`)}
      </div>
      {data.por_tipo.length > 0 && (
        <table className="mt-5 w-full text-sm">
          <thead>
            <tr className="border-b border-filete">
              <th className="rotulo py-2 text-left">Tipo de residuo</th>
              <th className="rotulo py-2 text-right">Total</th>
            </tr>
          </thead>
          <tbody>
            {data.por_tipo.map((t) => (
              <tr key={t.tipo_residuo__nombre + t.unidad__magnitud} className="border-b border-filete-suave last:border-0">
                <td className="py-2">{t.tipo_residuo__nombre}</td>
                <td className="tinta py-2 text-right font-semibold">
                  {numero(t.total)} {t.unidad__magnitud === 'PESO' ? 'kg' : 'L'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export function DetalleJornada() {
  const { id } = useParams()
  const { puede } = useAuth()
  const [version, setVersion] = useState(0)
  const { data: j, error, cargando } = useCarga(() => api<Jornada>(`jornadas/${id}/`), [id, version])
  const [panel, setPanel] = useState<'asignar' | 'cerrar' | null>(null)
  const [observaciones, setObservaciones] = useState('')
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [ocupado, setOcupado] = useState(false)

  const refrescar = () => setVersion((v) => v + 1)

  async function accion(ruta: string, ok: string, body?: unknown) {
    setOcupado(true)
    setAviso(null)
    try {
      await api(`jornadas/${id}/${ruta}/`, { body: body ?? {} })
      setAviso({ tono: 'ok', texto: ok })
      setPanel(null)
      refrescar()
    } catch (e) {
      setAviso({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    } finally {
      setOcupado(false)
    }
  }

  if (cargando && !j) return <Cargando />
  if (error || !j) return <Aviso tono="error">{error ?? 'Jornada no encontrada.'}</Aviso>

  const e = j.estado
  return (
    <>
      <Link to="/jornadas" className="mb-3 inline-flex items-center gap-1 text-sm text-grafito-2 hover:text-grafito">
        <ChevronLeft className="size-4" aria-hidden /> Jornadas
      </Link>
      <Encabezado
        titulo={
          <span className="flex flex-wrap items-center gap-4">
            {fecha(j.fecha)} · {j.turno_display}
            <Sello estado={selloDeJornada(e)} recien={version > 0} />
          </span>
        }
        detalle={`${j.sector_nombre}${j.descripcion ? ` — ${j.descripcion}` : ''}`}
        acciones={
          <>
            {(e === 'PLANIFICADA' || e === 'CONFIRMADA') && puede('operations.asignar_jornada') && (
              <Boton variante="secundario" onClick={() => setPanel(panel === 'asignar' ? null : 'asignar')}>
                Asignar cuadrilla
              </Boton>
            )}
            {e === 'PLANIFICADA' && puede('operations.change_jornada') && (
              <Boton cargando={ocupado} onClick={() => void accion('confirmar', 'Jornada confirmada: ya es visible para la cuadrilla asignada.')}>
                Confirmar y publicar
              </Boton>
            )}
            {e === 'CONFIRMADA' && puede('operations.ejecutar_jornada') && (
              <Boton cargando={ocupado} onClick={() => void accion('abrir', 'Jornada abierta: la captura en campo está habilitada.')}>
                Abrir jornada
              </Boton>
            )}
            {e === 'EN_EJECUCION' && puede('operations.add_registroresiduo') && (
              <Link to={`/campo?jornada=${j.id}`} className="inline-flex min-h-10 items-center gap-2 rounded-hoja border border-filete bg-hoja px-4 text-sm font-semibold hover:border-grafito-2">
                <Smartphone className="size-4" aria-hidden /> Registro en campo
              </Link>
            )}
            {e === 'EN_EJECUCION' && puede('operations.cerrar_jornada') && (
              <Boton onClick={() => setPanel(panel === 'cerrar' ? null : 'cerrar')}>Cerrar jornada</Boton>
            )}
          </>
        }
      />
      {aviso && (
        <div className="mb-4">
          <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>
        </div>
      )}

      <div className="flex flex-col gap-5">
        {panel === 'asignar' && (
          <Asignacion
            jornada={j}
            alGuardar={() => {
              setAviso({ tono: 'ok', texto: 'Cuadrilla y vehículos asignados.' })
              setPanel(null)
              refrescar()
            }}
          />
        )}
        {panel === 'cerrar' && (
          <section className="flex flex-col gap-3 rounded-hoja border border-filete bg-hoja p-5">
            <h2 className="text-lg font-bold [font-stretch:90%]">Cerrar jornada</h2>
            <p className="text-sm text-grafito-2">Al cerrar, la jornada queda asentada y ya no admite registros ni cambios.</p>
            <Campo etiqueta="Observaciones finales">
              <Area value={observaciones} onChange={(ev) => setObservaciones(ev.target.value)} />
            </Campo>
            <div>
              <Boton cargando={ocupado} onClick={() => void accion('cerrar', 'Jornada cerrada.', { observaciones })}>
                Cerrar definitivamente
              </Boton>
            </div>
          </section>
        )}

        {(e === 'EN_EJECUCION' || e === 'CERRADA') && <EjeJornada ruta={j.ruta} inicio={j.hora_inicio} fin={j.hora_fin} />}

        <div className="grid items-start gap-5 lg:grid-cols-[1fr_300px]">
          <section>
            <h2 className="rotulo mb-2">Ruta · {j.ruta.length} punto(s)</h2>
            <ol className="divide-y divide-filete-suave rounded-hoja border border-filete bg-hoja">
              {j.ruta.map((p) => (
                <li key={p.id} className="flex flex-wrap items-center gap-x-4 gap-y-1 px-4 py-3 text-sm">
                  <span className="w-6 text-right font-bold text-grafito-2">{p.orden}.</span>
                  <span className="font-semibold [font-stretch:85%]">{p.codigo}</span>
                  <span className="min-w-0 flex-1 truncate text-grafito-2">{p.nombre}</span>
                  {p.atendido === true && <Sello estado={p.sin_generacion ? 'SIN RESIDUOS' : 'ATENDIDO'} nota={hora(p.atendido_en)} />}
                  {p.atendido === false && <Sello estado="OMITIDO" nota={hora(p.atendido_en)} />}
                  {p.atendido === null && <span className="text-xs font-medium text-grafito-2">Pendiente</span>}
                  {p.atendido === false && <p className="w-full pl-10 text-xs text-sello-omit">Motivo: {p.motivo_omision}</p>}
                </li>
              ))}
            </ol>
          </section>
          <aside className="flex flex-col gap-4 rounded-hoja border border-filete bg-hoja p-5 text-sm">
            <div>
              <p className="rotulo mb-1">Responsable</p>
              <p className={cx(!j.responsable_nombre && 'text-grafito-2')}>{j.responsable_nombre || 'Sin asignar'}</p>
            </div>
            <div>
              <p className="rotulo mb-1">Cuadrilla</p>
              {j.personal_detalle.length ? (
                <ul>
                  {j.personal_detalle.map((u) => (
                    <li key={u.id}>{u.nombre}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-grafito-2">Sin personal asignado</p>
              )}
            </div>
            {j.observaciones_cierre && (
              <div>
                <p className="rotulo mb-1">Observaciones de cierre</p>
                <p className="tinta">{j.observaciones_cierre}</p>
              </div>
            )}
          </aside>
        </div>

        {(e === 'EN_EJECUCION' || e === 'CERRADA') && <ResumenJornada id={j.id} version={version} />}
      </div>
    </>
  )
}
