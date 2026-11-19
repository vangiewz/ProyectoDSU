import { useCallback, useEffect, useRef, useState } from 'react'

import { ApiError } from './api'

/** Carga asíncrona con estado de carga/error y función para recargar. */
export function useCarga<T>(cargar: () => Promise<T>, deps: unknown[]) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [cargando, setCargando] = useState(true)
  const ultimaCarga = useRef(0)

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fn = useCallback(cargar, deps)

  const recargar = useCallback(async () => {
    const carga = ++ultimaCarga.current
    setCargando(true)
    setError(null)
    try {
      const nuevo = await fn()
      if (carga === ultimaCarga.current) setData(nuevo)
    } catch (e) {
      if (carga === ultimaCarga.current) setError(e instanceof Error ? e.message : String(e))
    } finally {
      if (carga === ultimaCarga.current) setCargando(false)
    }
  }, [fn])

  useEffect(() => {
    void recargar()
    return () => { ultimaCarga.current += 1 }
  }, [recargar])

  return { data, error, cargando, recargar, setData }
}

export const esError403 = (e: unknown) => e instanceof ApiError && e.status === 403

const fmtFecha = new Intl.DateTimeFormat('es-BO', { day: '2-digit', month: 'short', year: 'numeric' })
const fmtHora = new Intl.DateTimeFormat('es-BO', { hour: '2-digit', minute: '2-digit', hour12: false })
const fmtNum = new Intl.NumberFormat('es-BO', { maximumFractionDigits: 2 })

export const fecha = (iso?: string | null) => (iso ? fmtFecha.format(new Date(iso.length === 10 ? `${iso}T12:00` : iso)) : '—')
export const hora = (iso?: string | null) => (iso ? fmtHora.format(new Date(iso)) : '—')
export const fechaHora = (iso?: string | null) => (iso ? `${fecha(iso)} · ${hora(iso)}` : '—')
// Las estimaciones no son exactas: enteros desde 100 kg, un decimal por debajo (RNF13).
export const aproximado = (v: number) => new Intl.NumberFormat('es-BO', { maximumFractionDigits: Math.abs(v) >= 100 ? 0 : 1 }).format(v)
export const numero = (v?: string | number | null) => (v === null || v === undefined || v === '' ? '—' : fmtNum.format(Number(v)))
export const hoyISO = () => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
