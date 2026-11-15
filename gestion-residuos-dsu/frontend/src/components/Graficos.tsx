import { useState, type ReactNode } from 'react'

import { aproximado, numero } from '../lib/datos'
import { cx } from './ui'

// Una sola serie por gráfico: un solo tono, sin leyenda. Bolígrafo = cantidades medidas;
// lápiz = estimaciones del modelo, que además llevan su margen de error.
const TINTA = '#1f3fa8'
export const LAPIZ = '#55606c'
const GRILLA = '#e3e7ec'

export type Dato = { etiqueta: string; valor: number; detalle?: string; margen?: number }

const conMargen = (d: Dato, unidad: string) =>
  d.margen === undefined ? `${numero(d.valor)} ${unidad}` : `≈ ${aproximado(d.valor)} ± ${aproximado(d.margen)} ${unidad}`

function niceMax(v: number) {
  if (v <= 0) return 1
  const p = 10 ** Math.floor(Math.log10(v))
  return ([1, 2, 5, 10].find((m) => m * p >= v) ?? 10) * p
}

/** Marco común: título, unidad, alternar a tabla (la tabla es la vista accesible de los datos). */
function Marco({ titulo, unidad, datos, children }: { titulo: string; unidad: string; datos: Dato[]; children: ReactNode }) {
  const [tabla, setTabla] = useState(false)
  return (
    <figure className="rounded-hoja border border-filete bg-hoja p-5">
      <figcaption className="mb-3 flex items-baseline justify-between gap-3">
        <span className="font-bold [font-stretch:90%]">
          {titulo} <span className="text-sm font-medium text-grafito-2">({unidad})</span>
        </span>
        <button onClick={() => setTabla(!tabla)} className="text-xs font-semibold text-grafito-2 underline hover:text-grafito">
          {tabla ? 'Ver gráfico' : 'Ver tabla'}
        </button>
      </figcaption>
      {!datos.length ? (
        <p className="py-8 text-center text-sm text-grafito-2">Sin datos para estos filtros.</p>
      ) : tabla ? (
        <table className="w-full text-sm">
          <tbody>
            {datos.map((d) => (
              <tr key={d.etiqueta} className="border-b border-filete-suave last:border-0">
                <td className="py-1.5">{d.etiqueta}</td>
                <td className={cx('py-1.5 text-right font-semibold', d.margen !== undefined ? 'text-lapiz' : 'tinta')}>{conMargen(d, unidad)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        children
      )}
    </figure>
  )
}

/** Magnitud por categoría: barras horizontales ordenadas, valor en la punta. */
export function BarrasHorizontales({
  titulo,
  unidad,
  datos,
  alElegir,
  tinta = TINTA,
}: {
  titulo: string
  unidad: string
  datos: Dato[]
  alElegir?: (d: Dato) => void
  tinta?: string
}) {
  const max = Math.max(...datos.map((d) => d.valor), 0) || 1
  return (
    <Marco titulo={titulo} unidad={unidad} datos={datos}>
      <ul className="flex flex-col gap-2.5">
        {datos.map((d) => (
          <li key={d.etiqueta}>
            <button
              onClick={alElegir ? () => alElegir(d) : undefined}
              className={cx('grid w-full grid-cols-[minmax(4.5rem,9rem)_minmax(0,1fr)] items-center gap-3 text-left text-sm', alElegir && 'cursor-pointer hover:bg-papel')}
              title={`${d.etiqueta}: ${conMargen(d, unidad)}${d.detalle ? ` · ${d.detalle}` : ''}`}
            >
              <span className="truncate">{d.etiqueta}</span>
              <span className="flex items-center gap-2">
                <span className="h-5 rounded-r-[4px]" style={{ width: `${Math.max((d.valor / max) * 78, 0.5)}%`, background: tinta }} />
                <span className="text-xs font-semibold whitespace-nowrap">
                  {d.margen === undefined ? numero(d.valor) : <span className="text-lapiz">≈ {aproximado(d.valor)} <span className="font-normal">± {aproximado(d.margen)}</span></span>}
                </span>
              </span>
            </button>
          </li>
        ))}
      </ul>
    </Marco>
  )
}

/** Cambio en el tiempo: columnas por día o semana con línea base única, tooltip al pasar. */
export function Columnas({ titulo, unidad, datos, tinta = TINTA }: { titulo: string; unidad: string; datos: Dato[]; tinta?: string }) {
  const [activo, setActivo] = useState<number | null>(null)
  const W = 720
  const H = 220
  const izq = 44
  const abajo = 24
  const arriba = 10 // aire para la etiqueta del tope del eje
  const top = niceMax(Math.max(...datos.map((d) => d.valor + (d.margen ?? 0)), 0))
  const ancho = (W - izq) / Math.max(datos.length, 1)
  const barra = Math.min(24, Math.max(ancho - 2, 2))
  const y = (v: number) => arriba + (H - abajo - arriba) * (1 - v / top)
  const ticks = [0, top / 2, top]
  const cadaEtiqueta = Math.ceil(datos.length / 8)
  const sel = activo !== null ? datos[activo] : null

  return (
    <Marco titulo={titulo} unidad={unidad} datos={datos}>
      <div className="relative">
        <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full" role="img" aria-label={`${titulo}, ${datos.length} periodos`} onMouseLeave={() => setActivo(null)}>
          {ticks.map((t) => (
            <g key={t}>
              <line x1={izq} x2={W} y1={y(t)} y2={y(t)} stroke={GRILLA} strokeWidth={1} />
              <text x={izq - 6} y={y(t) + 4} textAnchor="end" fontSize={11} fill="#4a5560">
                {numero(t)}
              </text>
            </g>
          ))}
          {datos.map((d, i) => {
            const x = izq + i * ancho + (ancho - barra) / 2
            const alto = Math.max((H - abajo) - y(d.valor), d.valor > 0 ? 1 : 0)
            const r = Math.min(4, barra / 2, alto)
            return (
              <g key={d.etiqueta} onMouseEnter={() => setActivo(i)} onFocus={() => setActivo(i)} tabIndex={0} aria-label={`${d.etiqueta}: ${conMargen(d, unidad)}`}>
                <rect x={izq + i * ancho} y={0} width={ancho} height={H - abajo} fill="transparent" />
                <path
                  d={`M${x},${H - abajo} v${-(alto - r)} q0,${-r} ${r},${-r} h${barra - 2 * r} q${r},0 ${r},${r} v${alto - r} z`}
                  fill={tinta}
                  opacity={activo === null || activo === i ? 1 : 0.45}
                />
                {d.margen !== undefined && d.margen > 0 && (
                  // Bigote del margen de error: de valor − margen a valor + margen.
                  <path
                    d={`M${x + barra / 2},${y(Math.max(d.valor - d.margen, 0))} V${y(d.valor + d.margen)} M${x + barra / 2 - 3},${y(d.valor + d.margen)} h6`}
                    stroke="#1e2328"
                    strokeWidth={1.25}
                    fill="none"
                  />
                )}
                {i % cadaEtiqueta === 0 && (
                  <text x={x + barra / 2} y={H - 6} textAnchor="middle" fontSize={11} fill="#4a5560">
                    {d.etiqueta}
                  </text>
                )}
              </g>
            )
          })}
        </svg>
        {sel && (
          <div className="pointer-events-none absolute top-0 right-0 rounded-hoja border border-filete bg-hoja px-3 py-2 text-xs shadow-[0_2px_8px_rgb(0_0_0/0.08)]">
            <p className="font-semibold">{sel.etiqueta}</p>
            <p className={cx('font-bold', sel.margen !== undefined ? 'text-lapiz' : 'tinta')}>{conMargen(sel, unidad)}</p>
          </div>
        )}
      </div>
    </Marco>
  )
}
