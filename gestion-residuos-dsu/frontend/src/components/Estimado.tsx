import { aproximado } from '../lib/datos'
import { cx } from './ui'

/** Cifra del modelo: a lápiz, aproximada y siempre con su margen de error (RNF13). */
export function Estimado({ valor, margen, unidad = 'kg', className }: { valor: string | number; margen: string | number; unidad?: string; className?: string }) {
  const v = Number(valor)
  const m = Number(margen)
  return (
    <span className={cx('whitespace-nowrap', className)} title={`Estimación: entre ${aproximado(Math.max(v - m, 0))} y ${aproximado(v + m)} ${unidad}`}>
      <span className="lapiz font-semibold">≈ {aproximado(v)}</span>
      <span className="text-[0.8em] text-lapiz">
        {' '}± {aproximado(m)} {unidad}
      </span>
    </span>
  )
}
