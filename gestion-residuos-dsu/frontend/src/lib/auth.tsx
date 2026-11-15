import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react'

import { api, sesion } from './api'

export type Yo = {
  id: number
  username: string
  first_name: string
  last_name: string
  email: string
  is_superuser: boolean
  roles: string[]
  permisos: string[]
}

type Auth = {
  yo: Yo | null
  cargando: boolean
  entrar: (username: string, password: string) => Promise<void>
  salir: () => Promise<void>
  puede: (...permisos: string[]) => boolean
}

const Ctx = createContext<Auth | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [yo, setYo] = useState<Yo | null>(null)
  const [cargando, setCargando] = useState(() => sesion.get() !== null)

  const cargarYo = useCallback(async () => {
    try {
      setYo(await api<Yo>('auth/me/'))
    } catch {
      sesion.set(null)
      setYo(null)
    } finally {
      setCargando(false)
    }
  }, [])

  useEffect(() => {
    if (sesion.get()) void cargarYo()
    const expirada = () => setYo(null)
    window.addEventListener('dsu:sesion-expirada', expirada)
    return () => window.removeEventListener('dsu:sesion-expirada', expirada)
  }, [cargarYo])

  const entrar = async (username: string, password: string) => {
    const t = await api<{ access: string; refresh: string }>('auth/login/', { body: { username, password } })
    sesion.set(t)
    await cargarYo()
  }

  const salir = async () => {
    const t = sesion.get()
    if (t) await api('auth/logout/', { body: { refresh: t.refresh } }).catch(() => undefined)
    sesion.set(null)
    setYo(null)
  }

  const puede = (...permisos: string[]) => !!yo && (yo.is_superuser || permisos.every((p) => yo.permisos.includes(p)))

  return <Ctx.Provider value={{ yo, cargando, entrar, salir, puede }}>{children}</Ctx.Provider>
}

export function useAuth() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useAuth fuera de AuthProvider')
  return ctx
}
