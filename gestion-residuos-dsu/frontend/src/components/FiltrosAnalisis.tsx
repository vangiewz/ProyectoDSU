import { RotateCcw } from 'lucide-react'
import { useEffect, useState } from 'react'

import { hoyISO } from '../lib/datos'
import { opcionesDe, type Opcion } from './Crud'
import { Boton, Campo, Entrada, Seleccion } from './ui'

export type Filtros = { desde: string; hasta: string; periodo: string; sector: string; punto: string; tipo_residuo: string }

export function filtrosIniciales(dias = 30): Filtros {
  const d = new Date()
  d.setDate(d.getDate() - (dias - 1))
  const desde = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  return { desde, hasta: hoyISO(), periodo: '', sector: '', punto: '', tipo_residuo: '' }
}

/** Parámetros de consulta: el periodo académico reemplaza al rango de fechas cuando se elige. */
export const consulta = (f: Filtros) => (f.periodo ? { ...f, desde: '', hasta: '' } : { ...f, periodo: '' })

function useListas(sector: string) {
  const [l, setL] = useState<{ sectores: Opcion[]; tipos: Opcion[]; periodos: Opcion[]; puntos: Opcion[] }>({ sectores: [], tipos: [], periodos: [], puntos: [] })
  useEffect(() => {
    void Promise.all([
      opcionesDe('sectores/', (f) => `${f.codigo} · ${f.nombre}`),
      opcionesDe('tipos-residuo/', (f) => String(f.nombre)),
      opcionesDe('periodos/', (f) => String(f.nombre)),
    ]).then(([sectores, tipos, periodos]) => setL((p) => ({ ...p, sectores, tipos, periodos })))
  }, [])
  useEffect(() => {
    void opcionesDe('puntos/', (f) => `${f.codigo} · ${f.nombre}`, sector ? { sector } : {}).then((puntos) => setL((p) => ({ ...p, puntos })))
  }, [sector])
  return l
}

function Lista({ etiqueta, valor, opciones, cambiar }: { etiqueta: string; valor: string; opciones: Opcion[]; cambiar: (v: string) => void }) {
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

/** Fila única de filtros sobre lo que acotan (RF17, RF21). */
export function FiltrosAnalisis({ valor, cambiar, sinPunto }: { valor: Filtros; cambiar: (f: Filtros) => void; sinPunto?: boolean }) {
  const l = useListas(valor.sector)
  const set = (k: keyof Filtros, v: string) => cambiar({ ...valor, [k]: v, ...(k === 'sector' ? { punto: '' } : {}) })
  return (
    <div className="mb-5 grid items-end gap-3 sm:grid-cols-3 xl:grid-cols-[repeat(6,minmax(0,1fr))_auto]">
      <Campo etiqueta="Desde">
        <Entrada type="date" value={valor.desde} disabled={!!valor.periodo} onChange={(e) => set('desde', e.target.value)} />
      </Campo>
      <Campo etiqueta="Hasta">
        <Entrada type="date" value={valor.hasta} disabled={!!valor.periodo} onChange={(e) => set('hasta', e.target.value)} />
      </Campo>
      <Lista etiqueta="Periodo académico" valor={valor.periodo} opciones={l.periodos} cambiar={(v) => set('periodo', v)} />
      <Lista etiqueta="Sector" valor={valor.sector} opciones={l.sectores} cambiar={(v) => set('sector', v)} />
      {!sinPunto && <Lista etiqueta="Punto" valor={valor.punto} opciones={l.puntos} cambiar={(v) => set('punto', v)} />}
      <Lista etiqueta="Tipo de residuo" valor={valor.tipo_residuo} opciones={l.tipos} cambiar={(v) => set('tipo_residuo', v)} />
      <Boton variante="fantasma" onClick={() => cambiar(filtrosIniciales())} aria-label="Restablecer filtros" title="Restablecer filtros">
        <RotateCcw className="size-4" aria-hidden /> Restablecer
      </Boton>
    </div>
  )
}
