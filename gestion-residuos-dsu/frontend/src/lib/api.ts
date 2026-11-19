// Cliente HTTP del API Django (/api). Maneja JWT: adjunta el access y renueva con el refresh una vez ante 401.

const CLAVE = 'dsu.sesion'

type Tokens = { access: string; refresh: string }

export class ApiError extends Error {
  status: number
  data: unknown
  constructor(status: number, data: unknown, message: string) {
    super(message)
    this.status = status
    this.data = data
  }
}

export class SinConexion extends Error {
  constructor() {
    super('Sin conexión con el servidor. Revise la red e intente de nuevo; el dato no se guardó.')
  }
}

export type Pagina<T> = { count: number; next: string | null; previous: string | null; results: T[] }

// ponytail: tokens en localStorage; pasar a cookie httpOnly si se agrega CSP estricta o terceros con JS.
export const sesion = {
  get(): Tokens | null {
    try {
      return JSON.parse(localStorage.getItem(CLAVE) ?? 'null')
    } catch {
      return null
    }
  },
  set(t: Tokens | null) {
    if (t) localStorage.setItem(CLAVE, JSON.stringify(t))
    else localStorage.removeItem(CLAVE)
  },
}

/** Convierte la respuesta de error de DRF en un texto legible. */
export function mensajeDeError(data: unknown): string {
  if (!data) return 'Ocurrió un error inesperado.'
  if (typeof data === 'string') return data
  if (Array.isArray(data)) return data.map(mensajeDeError).join(' ')
  if (typeof data === 'object') {
    const d = data as Record<string, unknown>
    if (typeof d.detail === 'string') return d.detail
    return Object.entries(d)
      .map(([campo, v]) => (campo === 'non_field_errors' ? mensajeDeError(v) : `${campo}: ${mensajeDeError(v)}`))
      .join(' ')
  }
  return String(data)
}

// URL del backend en producción (frontend aparte); vacío = mismo origen (proxy de Vite en desarrollo).
const BASE = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')

let renovando: Promise<boolean> | null = null

async function renovar(): Promise<boolean> {
  const t = sesion.get()
  if (!t) return false
  renovando ??= fetch(`${BASE}/api/auth/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: t.refresh }),
  })
    .then(async (r) => {
      if (!r.ok) return false
      const nuevo = await r.json()
      sesion.set({ access: nuevo.access, refresh: nuevo.refresh ?? t.refresh })
      return true
    })
    .catch(() => false)
    .finally(() => {
      renovando = null
    })
  return renovando
}

type Opciones = {
  method?: string
  body?: unknown
  query?: Record<string, string | number | boolean | undefined | null>
  archivo?: boolean // devuelve un Blob (descargas de reportes)
}

export async function api<T = unknown>(ruta: string, opciones: Opciones = {}, reintento = true): Promise<T> {
  const url = new URL(`${BASE}/api/${ruta.replace(/^\//, '')}`, window.location.origin)
  for (const [k, v] of Object.entries(opciones.query ?? {})) {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, String(v))
  }
  const t = sesion.get()
  let r: Response
  try {
    r = await fetch(url, {
      cache: 'no-store', // datos vivos: nunca una respuesta guardada de otra versión o de otro usuario
      method: opciones.method ?? (opciones.body ? 'POST' : 'GET'),
      headers: {
        ...(opciones.body !== undefined ? { 'Content-Type': 'application/json' } : {}),
        ...(t ? { Authorization: `Bearer ${t.access}` } : {}),
      },
      body: opciones.body !== undefined ? JSON.stringify(opciones.body) : undefined,
    })
  } catch {
    throw new SinConexion()
  }
  if (r.status === 401 && reintento && t && (await renovar())) return api<T>(ruta, opciones, false)
  if (r.status === 401 && t) {
    sesion.set(null)
    window.dispatchEvent(new Event('dsu:sesion-expirada'))
  }
  if (r.status === 204 || r.status === 205) return undefined as T
  if (opciones.archivo && r.ok) return (await r.blob()) as T
  const data = await r.json().catch(() => null)
  if (!r.ok) throw new ApiError(r.status, data, mensajeDeError(data))
  return data as T
}
