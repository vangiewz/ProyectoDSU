import { Plus } from 'lucide-react'
import { useMemo, useState } from 'react'

import { CrudPage, opcionesDe, type CrudConfig, type Fila } from '../components/Crud'
import { Aviso, Boton, Campo, Cargando, Encabezado, Entrada, Paginacion, Seleccion, Tabla, cx } from '../components/ui'
import { api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fechaHora, useCarga } from '../lib/datos'

const ROLES = ['Administrador', 'Supervisor', 'Operativo', 'Directivo']

const cfgUsuarios: CrudConfig = {
  recurso: 'usuarios',
  titulo: 'Usuarios',
  detalle: 'Cuentas del personal. La desactivación impide el acceso y conserva el historial de operaciones.',
  modelo: 'accounts.user',
  columnas: [
    { titulo: 'Usuario', celda: (f) => <span className="font-semibold [font-stretch:85%]">{String(f.username)}</span> },
    { titulo: 'Nombre', celda: (f) => `${f.first_name} ${f.last_name}` },
    { titulo: 'Roles', celda: (f) => (f.roles as string[]).join(', ') || '—' },
    { titulo: 'Último acceso', celda: (f) => fechaHora(f.last_login as string | null) },
  ],
  campos: [
    { nombre: 'username', etiqueta: 'Nombre de usuario', requerido: true },
    { nombre: 'first_name', etiqueta: 'Nombres', requerido: true },
    { nombre: 'last_name', etiqueta: 'Apellidos', requerido: true },
    { nombre: 'ci', etiqueta: 'Carnet de identidad' },
    { nombre: 'email', etiqueta: 'Correo' },
    { nombre: 'telefono', etiqueta: 'Teléfono' },
    { nombre: 'roles', etiqueta: 'Roles', tipo: 'multiple', opciones: ROLES.map((r) => ({ valor: r, texto: r })) },
    {
      nombre: 'password',
      etiqueta: 'Contraseña',
      tipo: 'password',
      ayuda: 'Mínimo 8 caracteres, no solo números. Al editar, déjela vacía para conservar la actual.',
    },
  ],
  inicial: { roles: [] },
  filtros: [
    { nombre: 'groups__name', etiqueta: 'Rol', opciones: ROLES.map((r) => ({ valor: r, texto: r })) },
    { nombre: 'is_active', etiqueta: 'Estado', opciones: [{ valor: 'true', texto: 'Activos' }, { valor: 'false', texto: 'Inactivos' }] },
  ],
}

export function Usuarios() {
  const { puede } = useAuth()
  const veRoles = puede('auth.view_group')
  const { data } = useCarga(
    () => veRoles ? opcionesDe('roles/', (r) => String(r.name)).then((roles) => roles.map((r) => ({ valor: r.texto, texto: r.texto }))) : Promise.resolve(null),
    [veRoles],
  )
  const config = useMemo<CrudConfig>(() => ({
    ...cfgUsuarios,
    campos: cfgUsuarios.campos.map((c) => c.nombre === 'roles' ? { ...c, opciones: data ?? ROLES.map((r) => ({ valor: r, texto: r })) } : c),
    filtros: cfgUsuarios.filtros?.map((f) => f.nombre === 'groups__name' ? { ...f, opciones: data ?? f.opciones } : f),
  }), [data])
  return <CrudPage config={config} />
}

type Permiso = { id: number; codename: string; name: string; modulo: string; entidad: string }
type Rol = { id: number; name: string; permissions: number[]; usuarios: number }

const MODULOS: Record<string, string> = {
  accounts: 'Usuarios',
  auth: 'Roles',
  audit: 'Bitácora',
  catalogs: 'Catálogos',
  campus: 'Campus',
  operations: 'Operación',
  analytics: 'Análisis',
  prediction: 'Predicción',
}

export function Roles() {
  const { puede } = useAuth()
  const editable = puede('auth.change_group')
  const roles = useCarga(() => api<Pagina<Rol>>('roles/', { query: { page_size: 100 } }), [])
  const permisos = useCarga(() => api<Permiso[]>('permisos/'), [])
  const [sel, setSel] = useState<Rol | null>(null)
  const [nombre, setNombre] = useState('')
  const [marcados, setMarcados] = useState<Set<number>>(new Set())
  const [estado, setEstado] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [guardando, setGuardando] = useState(false)

  const porModulo = useMemo(() => {
    const g: Record<string, Permiso[]> = {}
    for (const p of permisos.data ?? []) (g[p.modulo] ??= []).push(p)
    return g
  }, [permisos.data])

  const abrir = (r: Rol | null) => {
    setSel(r ?? { id: 0, name: '', permissions: [], usuarios: 0 })
    setNombre(r?.name ?? '')
    setMarcados(new Set(r?.permissions ?? []))
    setEstado(null)
  }

  async function guardar() {
    if (!sel) return
    setGuardando(true)
    try {
      const body = { name: nombre, permissions: [...marcados] }
      await api(sel.id ? `roles/${sel.id}/` : 'roles/', { method: sel.id ? 'PATCH' : 'POST', body })
      setEstado({ tono: 'ok', texto: 'Rol guardado. Los usuarios con este rol ya operan con los nuevos permisos.' })
      setSel(null)
      void roles.recargar()
    } catch (e) {
      setEstado({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    } finally {
      setGuardando(false)
    }
  }

  return (
    <>
      <Encabezado
        titulo="Roles y permisos"
        detalle="Cada rol define qué módulos y operaciones ve su personal. Los cambios quedan en la bitácora."
        acciones={
          editable && (
            <Boton onClick={() => abrir(null)}>
              <Plus className="size-4" aria-hidden /> Nuevo rol
            </Boton>
          )
        }
      />
      {estado && (
        <div className="mb-4">
          <Aviso tono={estado.tono}>{estado.texto}</Aviso>
        </div>
      )}
      <div className={cx('grid items-start gap-5', sel && 'xl:grid-cols-[320px_1fr]')}>
        <section>
          {roles.cargando && !roles.data ? (
            <Cargando />
          ) : (
            <Tabla
              columnas={[
                { titulo: 'Rol', celda: (r: Rol) => <span className="font-semibold">{r.name}</span> },
                { titulo: 'Permisos', celda: (r: Rol) => r.permissions.length, derecha: true },
                { titulo: 'Usuarios', celda: (r: Rol) => r.usuarios, derecha: true },
              ]}
              filas={roles.data?.results ?? []}
              alSeleccionar={editable ? abrir : undefined}
            />
          )}
        </section>
        {sel && (
          <section className="rounded-hoja border border-filete bg-hoja p-5">
            <div className="mb-4 flex flex-wrap items-end gap-3">
              <div className="min-w-60 flex-1">
                <Campo etiqueta="Nombre del rol">
                  <Entrada value={nombre} onChange={(e) => setNombre(e.target.value)} />
                </Campo>
              </div>
              <Boton onClick={() => void guardar()} cargando={guardando}>
                Guardar rol
              </Boton>
              <Boton variante="fantasma" onClick={() => setSel(null)}>
                Cancelar
              </Boton>
            </div>
            <div className="grid gap-5 md:grid-cols-2">
              {Object.entries(porModulo).map(([modulo, lista]) => (
                <fieldset key={modulo}>
                  <legend className="rotulo mb-2">{MODULOS[modulo] ?? modulo}</legend>
                  <ul className="flex flex-col gap-1">
                    {lista.map((p) => (
                      <li key={p.id}>
                        <label className="flex min-h-8 items-start gap-2 text-sm">
                          <input
                            type="checkbox"
                            className="mt-0.5 size-4"
                            checked={marcados.has(p.id)}
                            onChange={() =>
                              setMarcados((s) => {
                                const n = new Set(s)
                                if (n.has(p.id)) n.delete(p.id)
                                else n.add(p.id)
                                return n
                              })
                            }
                          />
                          <span>{p.name}</span>
                        </label>
                      </li>
                    ))}
                  </ul>
                </fieldset>
              ))}
            </div>
          </section>
        )}
      </div>
    </>
  )
}

type RegistroBitacora = Fila & {
  fecha: string
  usuario: string | null
  modulo: string
  operacion: string
  operacion_display: string
  entidad: string
  entidad_id: string
  detalle: string
  datos_anteriores: unknown
  datos_nuevos: unknown
  ip: string | null
}

const OPERACIONES = ['CREAR', 'ACTUALIZAR', 'DESACTIVAR', 'ACTIVAR', 'TRANSICION', 'LOGIN', 'LOGIN_FALLIDO', 'LOGOUT', 'ACCESO_DENEGADO']

export function Bitacora() {
  const [pagina, setPagina] = useState(1)
  const [f, setF] = useState({ operacion: '', modulo: '', desde: '', hasta: '' })
  const [abierta, setAbierta] = useState<RegistroBitacora | null>(null)
  const { data, error, cargando } = useCarga(() => api<Pagina<RegistroBitacora>>('bitacora/', { query: { page: pagina, ...f } }), [pagina, JSON.stringify(f)])
  const set = (k: keyof typeof f, v: string) => {
    setF((p) => ({ ...p, [k]: v }))
    setPagina(1)
  }

  return (
    <>
      <Encabezado titulo="Bitácora de auditoría" detalle="Registro inalterable de las operaciones críticas: nadie puede editarlo ni borrarlo." />
      <div className="mb-4 grid gap-3 sm:grid-cols-4">
        <Campo etiqueta="Operación">
          <Seleccion value={f.operacion} onChange={(e) => set('operacion', e.target.value)}>
            <option value="">Todas</option>
            {OPERACIONES.map((o) => (
              <option key={o} value={o}>
                {o.replace('_', ' ').toLowerCase()}
              </option>
            ))}
          </Seleccion>
        </Campo>
        <Campo etiqueta="Módulo">
          <Seleccion value={f.modulo} onChange={(e) => set('modulo', e.target.value)}>
            <option value="">Todos</option>
            {Object.entries(MODULOS).map(([k, v]) => (
              <option key={k} value={k}>
                {v}
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
              alSeleccionar={(e) => setAbierta(abierta?.id === e.id ? null : e)}
              columnas={[
                { titulo: 'Fecha y hora', celda: (e) => <span className="whitespace-nowrap">{fechaHora(e.fecha)}</span> },
                { titulo: 'Usuario', celda: (e) => e.usuario ?? 'Anónimo' },
                {
                  titulo: 'Operación',
                  celda: (e) => (
                    <span className={cx('font-semibold [font-stretch:85%]', (e.operacion === 'ACCESO_DENEGADO' || e.operacion === 'LOGIN_FALLIDO') && 'text-dsu')}>
                      {e.operacion_display}
                    </span>
                  ),
                },
                { titulo: 'Entidad', celda: (e) => `${MODULOS[e.modulo] ?? e.modulo} · ${e.entidad}${e.entidad_id ? ` #${e.entidad_id}` : ''}` },
                { titulo: 'Detalle', celda: (e) => <span className="line-clamp-1 text-grafito-2">{e.detalle || '—'}</span> },
              ]}
            />
            {abierta && (
              <div className="mt-3 grid gap-3 rounded-hoja border border-filete bg-hoja p-4 text-xs md:grid-cols-2">
                <div>
                  <p className="rotulo mb-1">Valores anteriores</p>
                  <pre className="overflow-x-auto whitespace-pre-wrap text-grafito-2">{JSON.stringify(abierta.datos_anteriores, null, 2) ?? '—'}</pre>
                </div>
                <div>
                  <p className="rotulo mb-1">Valores nuevos</p>
                  <pre className="tinta overflow-x-auto whitespace-pre-wrap">{JSON.stringify(abierta.datos_nuevos, null, 2) ?? '—'}</pre>
                </div>
                <p className="text-grafito-2 md:col-span-2">IP de origen: {abierta.ip ?? '—'}</p>
              </div>
            )}
            <Paginacion pagina={pagina} total={data.count} cambiar={setPagina} />
          </>
        )
      )}
    </>
  )
}
