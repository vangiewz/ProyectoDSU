import { Plus, Search } from 'lucide-react'
import { useEffect, useState, type FormEvent, type ReactNode } from 'react'

import { api, ApiError, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { useCarga } from '../lib/datos'
import { Activo, Area, Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Paginacion, Seleccion, Tabla, type Columna } from './ui'
import { SelectorCoordenadas } from './Mapa'

export type Opcion = { valor: string | number; texto: string }

export type CampoDef = {
  nombre: string
  etiqueta: string
  tipo?: 'texto' | 'numero' | 'fecha' | 'area' | 'seleccion' | 'casilla' | 'multiple' | 'password' | 'coordenadas'
  opciones?: Opcion[] | (() => Promise<Opcion[]>)
  requerido?: boolean
  ayuda?: string
  paso?: string
  soloAlCrear?: boolean
}

export type Filtro = { nombre: string; etiqueta: string; opciones: Opcion[] }

export type Fila = { id: number; is_active?: boolean } & Record<string, unknown>

export type CrudConfig = {
  recurso: string
  titulo: string
  detalle?: ReactNode
  modelo: string // app.modelo para permisos, p. ej. "campus.sector"
  columnas: Columna<Fila>[]
  campos: CampoDef[]
  filtros?: Filtro[]
  inicial?: Record<string, unknown>
  pideMotivo?: boolean
  arriba?: (filas: Fila[]) => ReactNode
  sinBusqueda?: boolean
}

function useOpciones(campos: CampoDef[]) {
  const [remotas, setRemotas] = useState<Record<string, Opcion[]>>({})
  useEffect(() => {
    for (const c of campos) {
      if (typeof c.opciones === 'function') {
        void c.opciones().then((o) => setRemotas((prev) => ({ ...prev, [c.nombre]: o })))
      }
    }
  }, [campos])
  const fijas = Object.fromEntries(campos.filter((c) => Array.isArray(c.opciones)).map((c) => [c.nombre, c.opciones as Opcion[]]))
  return { ...fijas, ...remotas }
}

/** Lista todas las páginas de un recurso para alimentar selects. */
export async function opcionesDe(recurso: string, texto: (f: Fila) => string, query: Record<string, string> = {}): Promise<Opcion[]> {
  const r = await api<Pagina<Fila>>(recurso, { query: { page_size: 500, ...query } })
  return r.results.map((f) => ({ valor: f.id, texto: texto(f) }))
}

function Formulario({ config, fila, alGuardar, alCancelar }: { config: CrudConfig; fila: Fila | null; alGuardar: () => void; alCancelar: () => void }) {
  const opciones = useOpciones(config.campos)
  const [valores, setValores] = useState<Record<string, unknown>>(() => ({ ...config.inicial, ...fila }))
  const [errores, setErrores] = useState<Record<string, string>>({})
  const [general, setGeneral] = useState<string | null>(null)
  const [guardando, setGuardando] = useState(false)
  const set = (k: string, v: unknown) => setValores((p) => ({ ...p, [k]: v }))

  async function enviar(e: FormEvent) {
    e.preventDefault()
    setGuardando(true)
    setErrores({})
    setGeneral(null)
    const cuerpo: Record<string, unknown> = {}
    for (const c of config.campos) {
      if (c.tipo === 'coordenadas') {
        cuerpo.latitud = valores.latitud
        cuerpo.longitud = valores.longitud
      } else if (!(c.tipo === 'password' && !valores[c.nombre])) {
        const v = valores[c.nombre]
        cuerpo[c.nombre] = v === '' && (c.tipo === 'seleccion' || c.tipo === 'numero') ? null : v
      }
    }
    try {
      await api(fila ? `${config.recurso}/${fila.id}/` : `${config.recurso}/`, { method: fila ? 'PATCH' : 'POST', body: cuerpo })
      alGuardar()
    } catch (err) {
      if (err instanceof ApiError && err.data && typeof err.data === 'object' && !Array.isArray(err.data)) {
        const porCampo: Record<string, string> = {}
        const resto: string[] = []
        for (const [k, v] of Object.entries(err.data as Record<string, unknown>)) {
          const msg = Array.isArray(v) ? v.join(' ') : String(v)
          if (config.campos.some((c) => c.nombre === k || (c.tipo === 'coordenadas' && (k === 'latitud' || k === 'longitud')))) {
            porCampo[k === 'longitud' ? 'latitud' : k] = msg
          } else resto.push(msg)
        }
        setErrores(porCampo)
        setGeneral(resto.join(' ') || (Object.keys(porCampo).length ? null : err.message))
      } else setGeneral(err instanceof Error ? err.message : String(err))
    } finally {
      setGuardando(false)
    }
  }

  return (
    <form onSubmit={enviar} className="flex flex-col gap-4 rounded-hoja border border-filete bg-hoja p-5" noValidate>
      <h2 className="text-lg font-bold [font-stretch:90%]">{fila ? `Editar ${String(fila.codigo ?? fila.nombre ?? fila.username ?? fila.placa ?? '')}` : 'Nuevo registro'}</h2>
      {general && <Aviso tono="error">{general}</Aviso>}
      {config.campos
        .filter((c) => !(c.soloAlCrear && fila))
        .map((c) => {
          const v = valores[c.nombre]
          const err = errores[c.nombre]
          if (c.tipo === 'casilla')
            return (
              <label key={c.nombre} className="flex min-h-10 items-center gap-3 text-sm">
                <input type="checkbox" className="size-5" checked={!!v} onChange={(e) => set(c.nombre, e.target.checked)} />
                {c.etiqueta}
              </label>
            )
          if (c.tipo === 'coordenadas')
            return (
              <Campo key={c.nombre} etiqueta={c.etiqueta} error={errores.latitud} ayuda="Toque el mapa para ubicar el punto o escriba las coordenadas.">
                <SelectorCoordenadas
                  latitud={valores.latitud as string}
                  longitud={valores.longitud as string}
                  cambiar={(lat, lon) => setValores((p) => ({ ...p, latitud: lat, longitud: lon }))}
                />
              </Campo>
            )
          return (
            <Campo key={c.nombre} etiqueta={c.etiqueta + (c.requerido ? ' *' : '')} error={err} ayuda={c.ayuda}>
              {c.tipo === 'seleccion' ? (
                <Seleccion value={(v as string | number | null) ?? ''} onChange={(e) => set(c.nombre, e.target.value)} required={c.requerido}>
                  <option value="">— Seleccione —</option>
                  {(opciones[c.nombre] ?? []).map((o) => (
                    <option key={o.valor} value={o.valor}>
                      {o.texto}
                    </option>
                  ))}
                </Seleccion>
              ) : c.tipo === 'multiple' ? (
                <div className="flex flex-wrap gap-2">
                  {(opciones[c.nombre] ?? []).map((o) => {
                    const lista = (v as (string | number)[]) ?? []
                    const marcado = lista.includes(o.valor)
                    return (
                      <label key={o.valor} className="flex min-h-10 items-center gap-2 rounded-hoja border border-filete px-3 text-sm has-[:checked]:border-boligrafo has-[:checked]:text-boligrafo">
                        <input
                          type="checkbox"
                          checked={marcado}
                          onChange={() => set(c.nombre, marcado ? lista.filter((x) => x !== o.valor) : [...lista, o.valor])}
                        />
                        {o.texto}
                      </label>
                    )
                  })}
                </div>
              ) : c.tipo === 'area' ? (
                <Area value={(v as string) ?? ''} onChange={(e) => set(c.nombre, e.target.value)} />
              ) : (
                <Entrada
                  type={c.tipo === 'numero' ? 'number' : c.tipo === 'fecha' ? 'date' : c.tipo === 'password' ? 'password' : 'text'}
                  step={c.paso}
                  inputMode={c.tipo === 'numero' ? 'decimal' : undefined}
                  autoComplete={c.tipo === 'password' ? 'new-password' : undefined}
                  value={(v as string | number | null) ?? ''}
                  onChange={(e) => set(c.nombre, e.target.value)}
                  required={c.requerido}
                />
              )}
            </Campo>
          )
        })}
      <div className="flex gap-2 pt-1">
        <Boton type="submit" cargando={guardando}>
          Guardar
        </Boton>
        <Boton type="button" variante="fantasma" onClick={alCancelar}>
          Cancelar
        </Boton>
      </div>
    </form>
  )
}

export function CrudPage({ config }: { config: CrudConfig }) {
  const { puede } = useAuth()
  const [app, modelo] = config.modelo.split('.')
  const puedeCrear = puede(`${app}.add_${modelo}`)
  const puedeEditar = puede(`${app}.change_${modelo}`)

  const [pagina, setPagina] = useState(1)
  const [busqueda, setBusqueda] = useState('')
  const [filtros, setFiltros] = useState<Record<string, string>>({})
  const [editando, setEditando] = useState<Fila | 'nuevo' | null>(null)
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)

  const { data, error, cargando, recargar } = useCarga(
    () => api<Pagina<Fila>>(`${config.recurso}/`, { query: { page: pagina, search: busqueda, ...filtros } }),
    [config.recurso, pagina, busqueda, JSON.stringify(filtros)],
  )

  async function alternar(fila: Fila) {
    let motivo = ''
    if (fila.is_active && config.pideMotivo) {
      motivo = window.prompt('Motivo de la desactivación') ?? ''
      if (!motivo.trim()) return
    }
    try {
      await api(`${config.recurso}/${fila.id}/${fila.is_active ? 'desactivar' : 'activar'}/`, { body: { motivo } })
      setAviso({ tono: 'ok', texto: fila.is_active ? 'Registro desactivado. Su historial se conserva.' : 'Registro reactivado.' })
      void recargar()
    } catch (e) {
      setAviso({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    }
  }

  const columnas: Columna<Fila>[] = [
    ...config.columnas,
    ...('is_active' in (data?.results[0] ?? {}) ? [{ titulo: 'Estado', celda: (f: Fila) => <Activo activo={!!f.is_active} /> }] : []),
    ...(puedeEditar
      ? [
          {
            titulo: 'Acciones',
            derecha: true,
            celda: (f: Fila) => (
              <div className="flex justify-end gap-1" onClick={(e) => e.stopPropagation()}>
                <Boton variante="fantasma" onClick={() => setEditando(f)}>
                  Editar
                </Boton>
                {'is_active' in f && (
                  <Boton variante={f.is_active ? 'peligro' : 'secundario'} onClick={() => void alternar(f)}>
                    {f.is_active ? 'Desactivar' : 'Activar'}
                  </Boton>
                )}
              </div>
            ),
          },
        ]
      : []),
  ]

  return (
    <>
      <Encabezado
        titulo={config.titulo}
        detalle={config.detalle}
        acciones={
          puedeCrear && (
            <Boton onClick={() => setEditando('nuevo')}>
              <Plus className="size-4" aria-hidden /> Nuevo
            </Boton>
          )
        }
      />
      {aviso && (
        <div className="mb-4">
          <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>
        </div>
      )}
      {config.arriba && data && <div className="mb-5">{config.arriba(data.results)}</div>}
      <div className={editando ? 'grid items-start gap-5 xl:grid-cols-[minmax(0,1fr)_400px]' : ''}>
        <section className={editando ? 'hidden xl:block' : ''}>
          <div className="mb-3 flex flex-wrap gap-2">
            {!config.sinBusqueda && (
              <div className="relative min-w-56 flex-1">
                <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-grafito-2" aria-hidden />
                <Entrada
                  type="search"
                  placeholder="Buscar…"
                  aria-label="Buscar"
                  className="pl-9"
                  value={busqueda}
                  onChange={(e) => {
                    setBusqueda(e.target.value)
                    setPagina(1)
                  }}
                />
              </div>
            )}
            {config.filtros?.map((f) => (
              <Seleccion
                key={f.nombre}
                aria-label={f.etiqueta}
                className="w-auto"
                value={filtros[f.nombre] ?? ''}
                onChange={(e) => {
                  setFiltros((p) => ({ ...p, [f.nombre]: e.target.value }))
                  setPagina(1)
                }}
              >
                <option value="">{f.etiqueta}: todos</option>
                {f.opciones.map((o) => (
                  <option key={o.valor} value={o.valor}>
                    {o.texto}
                  </option>
                ))}
              </Seleccion>
            ))}
          </div>
          {error && <Aviso tono="error">{error}</Aviso>}
          {cargando && !data ? (
            <Cargando />
          ) : (
            data && (
              <>
                <Tabla columnas={columnas} filas={data.results} alSeleccionar={puedeEditar ? (f) => setEditando(f) : undefined} />
                <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
              </>
            )
          )}
        </section>
        {editando && (
          <aside className="xl:sticky xl:top-6">
            <Formulario
              key={editando === 'nuevo' ? 'nuevo' : editando.id}
              config={config}
              fila={editando === 'nuevo' ? null : editando}
              alCancelar={() => setEditando(null)}
              alGuardar={() => {
                setAviso({ tono: 'ok', texto: 'Cambios guardados y registrados en la bitácora.' })
                setEditando(null)
                void recargar()
              }}
            />
          </aside>
        )}
      </div>
    </>
  )
}
