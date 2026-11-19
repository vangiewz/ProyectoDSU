import {
  AlertOctagon,
  BarChart3,
  BellRing,
  DatabaseZap,
  FileSpreadsheet,
  Map as MapIcon,
  SlidersHorizontal,
  TrendingUp,
  Trees,
  Boxes,
  CalendarClock,
  ClipboardList,
  History,
  LogOut,
  MapPin,
  Menu,
  Recycle,
  ScrollText,
  ShieldCheck,
  Smartphone,
  Truck,
  Users,
  X,
  type LucideIcon,
} from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router'

import { useAuth } from '../lib/auth'
import { Resguardo } from './Resguardo'
import { cx } from './ui'

type Item = { a: string; texto: string; Icono: LucideIcon; permiso: string }
type Grupo = { titulo?: string; items: Item[] }

export const NAVEGACION: Grupo[] = [
  {
    items: [
      { a: '/campo', texto: 'Registro en campo', Icono: Smartphone, permiso: 'operations.ejecutar_jornada' },
      { a: '/jornadas', texto: 'Jornadas', Icono: CalendarClock, permiso: 'operations.view_jornada' },
      { a: '/historico', texto: 'Histórico de residuos', Icono: History, permiso: 'operations.view_registroresiduo' },
      { a: '/incidencias', texto: 'Incidencias', Icono: AlertOctagon, permiso: 'operations.view_incidencia' },
    ],
  },
  {
    titulo: 'Análisis',
    items: [
      { a: '/tablero', texto: 'Tablero', Icono: BarChart3, permiso: 'analytics.view_hechoresiduo' },
      { a: '/mapa', texto: 'Mapa del campus', Icono: MapIcon, permiso: 'analytics.view_hechoresiduo' },
      { a: '/predicciones', texto: 'Predicción', Icono: TrendingUp, permiso: 'prediction.view_prediccion' },
      { a: '/recomendaciones', texto: 'Alertas y recomendaciones', Icono: BellRing, permiso: 'prediction.view_recomendacion' },
      { a: '/reportes', texto: 'Reportes', Icono: FileSpreadsheet, permiso: 'analytics.generar_reporte' },
    ],
  },
  {
    titulo: 'Campus',
    items: [
      { a: '/sectores', texto: 'Sectores', Icono: ClipboardList, permiso: 'campus.view_sector' },
      { a: '/puntos', texto: 'Puntos de recolección', Icono: MapPin, permiso: 'campus.view_puntorecoleccion' },
      { a: '/contenedores', texto: 'Contenedores', Icono: Boxes, permiso: 'campus.view_contenedor' },
    ],
  },
  {
    titulo: 'Catálogos',
    items: [
      { a: '/tipos-residuo', texto: 'Tipos y unidades', Icono: Recycle, permiso: 'catalogs.view_tiporesiduo' },
      { a: '/vehiculos', texto: 'Vehículos', Icono: Truck, permiso: 'operations.view_vehiculo' },
    ],
  },
  {
    titulo: 'Administración',
    items: [
      { a: '/usuarios', texto: 'Usuarios', Icono: Users, permiso: 'accounts.view_user' },
      { a: '/roles', texto: 'Roles y permisos', Icono: ShieldCheck, permiso: 'auth.view_group' },
      { a: '/procesos', texto: 'Procesamiento ETL', Icono: DatabaseZap, permiso: 'analytics.view_ejecucionetl' },
      { a: '/modelo', texto: 'Modelo predictivo', Icono: Trees, permiso: 'prediction.view_modeloentrenado' },
      { a: '/parametros', texto: 'Parámetros', Icono: SlidersHorizontal, permiso: 'catalogs.view_parametrossistema' },
      { a: '/bitacora', texto: 'Bitácora', Icono: ScrollText, permiso: 'audit.view_auditlog' },
    ],
  },
]

function Monograma() {
  return (
    <div className="flex items-center gap-3">
      <span className="grid h-10 place-items-center rounded-[3px] bg-white px-2 text-xl font-extrabold tracking-tight text-dsu [font-stretch:80%]">
        DSU
      </span>
      <span className="text-[0.7rem] leading-tight font-semibold text-white/85 [font-stretch:85%]">
        Dirección de Servicios
        <br />
        Universitarios · UAGRM
      </span>
    </div>
  )
}

function Riel({ cerrar }: { cerrar?: () => void }) {
  const { yo, puede, salir } = useAuth()
  const grupos = NAVEGACION.map((g) => ({ ...g, items: g.items.filter((i) => puede(i.permiso)) })).filter((g) => g.items.length)

  return (
    <div className="flex h-full flex-col bg-dsu text-white">
      <div className="flex items-center justify-between px-5 pt-5 pb-6">
        <Monograma />
        {cerrar && (
          <button onClick={cerrar} className="rounded p-2 hover:bg-white/10" aria-label="Cerrar menú">
            <X className="size-5" />
          </button>
        )}
      </div>
      <nav className="flex-1 overflow-y-auto pb-4" aria-label="Principal">
        {grupos.map((g, i) => (
          <div key={g.titulo ?? i} className="mb-4">
            {g.titulo && <p className="px-5 pb-1.5 text-[0.68rem] font-semibold tracking-[0.08em] text-white/65 uppercase [font-stretch:80%]">{g.titulo}</p>}
            <ul>
              {g.items.map(({ a, texto, Icono }) => (
                <li key={a}>
                  <NavLink
                    to={a}
                    onClick={cerrar}
                    className={({ isActive }) =>
                      cx(
                        'ml-3 flex min-h-10 items-center gap-3 rounded-l-[4px] py-2 pr-4 pl-3 text-[0.92rem] font-medium transition-colors duration-100',
                        isActive ? 'bg-papel text-grafito' : 'text-white/90 hover:bg-white/10 hover:text-white',
                      )
                    }
                  >
                    <Icono className="size-[18px] shrink-0" aria-hidden />
                    {texto}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
      <div className="border-t border-white/20 px-5 py-4">
        <p className="truncate text-sm font-semibold">{yo?.first_name ? `${yo.first_name} ${yo.last_name}` : yo?.username}</p>
        <p className="truncate text-xs text-white/75">{yo?.is_superuser ? 'Administrador' : yo?.roles.join(', ')}</p>
        <button onClick={() => void salir()} className="mt-3 inline-flex items-center gap-2 rounded px-2 py-1.5 -ml-2 text-sm text-white/90 hover:bg-white/10">
          <LogOut className="size-4" aria-hidden /> Cerrar sesión
        </button>
      </div>
    </div>
  )
}

export function Shell() {
  const [abierto, setAbierto] = useState(false)
  const { pathname } = useLocation()
  return (
    <div className="min-h-dvh lg:grid lg:grid-cols-[248px_1fr]">
      <aside className="sticky top-0 hidden h-dvh lg:block">
        <Riel />
      </aside>

      <header className="sticky top-0 z-[1000] flex h-14 items-center justify-between bg-dsu px-4 text-white lg:hidden">
        <span className="grid h-8 place-items-center rounded-[3px] bg-white px-1.5 text-base font-extrabold text-dsu [font-stretch:80%]">DSU</span>
        <button onClick={() => setAbierto(true)} className="rounded p-2 hover:bg-white/10" aria-label="Abrir menú" aria-expanded={abierto}>
          <Menu className="size-6" />
        </button>
      </header>
      {abierto && (
        <div className="fixed inset-0 z-[1100] lg:hidden" role="dialog" aria-modal="true" aria-label="Menú">
          <div className="absolute inset-0 bg-grafito/40" onClick={() => setAbierto(false)} />
          <div className="absolute inset-y-0 left-0 w-[min(300px,85vw)] shadow-[4px_0_24px_rgb(0_0_0/0.25)]">
            <Riel cerrar={() => setAbierto(false)} />
          </div>
        </div>
      )}

      <main className="min-w-0 px-4 py-6 sm:px-8 lg:py-8">
        <div className="mx-auto max-w-6xl">
          {/* Al cambiar de pantalla se reinicia: un error en una no bloquea las demás. */}
          <Resguardo key={pathname}>
            <Outlet />
          </Resguardo>
        </div>
      </main>
    </div>
  )
}
