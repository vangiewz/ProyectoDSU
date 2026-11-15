import { AlertTriangle, CheckCircle2, ChevronLeft, ChevronRight, Info, Loader2 } from 'lucide-react'
import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode, SelectHTMLAttributes, TextareaHTMLAttributes } from 'react'

const cx = (...c: (string | false | null | undefined)[]) => c.filter(Boolean).join(' ')

type Variante = 'primario' | 'secundario' | 'peligro' | 'fantasma'

const variantes: Record<Variante, string> = {
  primario: 'bg-grafito text-white hover:bg-black disabled:bg-grafito-2',
  secundario: 'bg-hoja text-grafito border border-filete hover:border-grafito-2',
  peligro: 'bg-hoja text-dsu border border-dsu/50 hover:bg-dsu hover:text-white',
  fantasma: 'text-grafito-2 hover:text-grafito hover:bg-filete-suave',
}

export function Boton({
  variante = 'primario',
  cargando,
  grande,
  className,
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variante?: Variante; cargando?: boolean; grande?: boolean }) {
  return (
    <button
      {...props}
      disabled={props.disabled || cargando}
      className={cx(
        'inline-flex items-center justify-center gap-2 rounded-hoja font-semibold transition-colors duration-100 disabled:cursor-not-allowed disabled:opacity-60',
        grande ? 'min-h-14 px-6 text-lg' : 'min-h-10 px-4 text-sm',
        variantes[variante],
        className,
      )}
    >
      {cargando && <Loader2 className="size-4 animate-spin" aria-hidden />}
      {children}
    </button>
  )
}

export function Campo({ etiqueta, error, ayuda, children }: { etiqueta: string; error?: string; ayuda?: string; children: ReactNode }) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="rotulo">{etiqueta}</span>
      {children}
      {ayuda && !error && <span className="text-xs text-grafito-2">{ayuda}</span>}
      {error && <span className="text-xs font-medium text-dsu">{error}</span>}
    </label>
  )
}

const control =
  'min-h-10 w-full rounded-hoja border border-filete bg-hoja px-3 text-[0.95rem] text-boligrafo placeholder:text-grafito-2/70 hover:border-grafito-2 focus:border-boligrafo focus:outline-none disabled:bg-papel disabled:text-grafito-2'

export const Entrada = ({ className, ...p }: InputHTMLAttributes<HTMLInputElement>) => (
  <input {...p} className={cx(control, className)} />
)

export const Seleccion = ({ className, children, ...p }: SelectHTMLAttributes<HTMLSelectElement>) => (
  <select {...p} className={cx(control, 'pr-8', className)}>
    {children}
  </select>
)

export const Area = ({ className, ...p }: TextareaHTMLAttributes<HTMLTextAreaElement>) => (
  <textarea {...p} className={cx(control, 'min-h-20 py-2', className)} />
)

export function Encabezado({ titulo, detalle, acciones }: { titulo: ReactNode; detalle?: ReactNode; acciones?: ReactNode }) {
  return (
    <header className="mb-6 flex flex-wrap items-end justify-between gap-4 border-b border-filete pb-4">
      <div className="min-w-0">
        <h1 className="text-2xl font-bold tracking-tight [font-stretch:88%] sm:text-[1.75rem]">{titulo}</h1>
        {detalle && <p className="mt-1 text-sm text-grafito-2">{detalle}</p>}
      </div>
      {acciones && <div className="flex flex-wrap gap-2">{acciones}</div>}
    </header>
  )
}

type Tono = 'error' | 'ok' | 'info'
const tonos: Record<Tono, { clase: string; Icono: typeof Info }> = {
  error: { clase: 'border-dsu/40 bg-dsu/5 text-dsu-hondo', Icono: AlertTriangle },
  ok: { clase: 'border-sello-ok/40 bg-sello-ok/5 text-sello-ok', Icono: CheckCircle2 },
  info: { clase: 'border-filete bg-hoja text-grafito-2', Icono: Info },
}

export function Aviso({ tono = 'info', children }: { tono?: Tono; children: ReactNode }) {
  const { clase, Icono } = tonos[tono]
  return (
    <div role={tono === 'error' ? 'alert' : 'status'} className={cx('flex items-start gap-2 rounded-hoja border px-3 py-2.5 text-sm', clase)}>
      <Icono className="mt-0.5 size-4 shrink-0" aria-hidden />
      <div>{children}</div>
    </div>
  )
}

export function Vacio({ titulo, children }: { titulo: string; children?: ReactNode }) {
  return (
    <div className="rounded-hoja border border-dashed border-filete bg-hoja px-6 py-10 text-center">
      <p className="font-semibold">{titulo}</p>
      {children && <div className="mt-1 text-sm text-grafito-2">{children}</div>}
    </div>
  )
}

export function Cargando({ texto = 'Cargando…' }: { texto?: string }) {
  return (
    <div className="flex items-center gap-2 py-8 text-sm text-grafito-2" role="status">
      <Loader2 className="size-4 animate-spin" aria-hidden /> {texto}
    </div>
  )
}

export type Columna<T> = { titulo: string; celda: (fila: T) => ReactNode; derecha?: boolean; className?: string }

export function Tabla<T extends { id: number | string }>({
  columnas,
  filas,
  alSeleccionar,
  vacio = 'No hay registros que coincidan.',
}: {
  columnas: Columna<T>[]
  filas: T[]
  alSeleccionar?: (fila: T) => void
  vacio?: string
}) {
  if (!filas.length) return <Vacio titulo={vacio} />
  return (
    <div className="overflow-x-auto rounded-hoja border border-filete bg-hoja">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-filete">
            {columnas.map((c) => (
              <th key={c.titulo} scope="col" className={cx('rotulo whitespace-nowrap px-3 py-2.5', c.derecha ? 'text-right' : 'text-left')}>
                {c.titulo}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filas.map((f) => (
            <tr
              key={f.id}
              onClick={alSeleccionar ? () => alSeleccionar(f) : undefined}
              className={cx('border-b border-filete-suave last:border-0', alSeleccionar && 'cursor-pointer hover:bg-papel')}
            >
              {columnas.map((c) => (
                <td key={c.titulo} className={cx('px-3 py-2.5 align-middle', c.derecha && 'text-right', c.className)}>
                  {c.celda(f)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function Paginacion({ pagina, total, porPagina = 25, cambiar }: { pagina: number; total: number; porPagina?: number; cambiar: (p: number) => void }) {
  const paginas = Math.max(1, Math.ceil(total / porPagina))
  if (paginas === 1) return <p className="mt-3 text-xs text-grafito-2">{total} registro(s)</p>
  return (
    <nav className="mt-3 flex items-center justify-between text-sm" aria-label="Paginación">
      <span className="text-xs text-grafito-2">
        {total} registros · página {pagina} de {paginas}
      </span>
      <div className="flex gap-1">
        <Boton variante="secundario" disabled={pagina <= 1} onClick={() => cambiar(pagina - 1)} aria-label="Página anterior">
          <ChevronLeft className="size-4" />
        </Boton>
        <Boton variante="secundario" disabled={pagina >= paginas} onClick={() => cambiar(pagina + 1)} aria-label="Página siguiente">
          <ChevronRight className="size-4" />
        </Boton>
      </div>
    </nav>
  )
}

/** Estado activo/inactivo de un registro maestro. */
export const Activo = ({ activo }: { activo: boolean }) => (
  <span className={cx('inline-flex items-center gap-1.5 text-xs font-medium', activo ? 'text-sello-ok' : 'text-grafito-2')}>
    <span className={cx('size-1.5 rounded-full', activo ? 'bg-sello-ok' : 'bg-filete')} aria-hidden />
    {activo ? 'Activo' : 'Inactivo'}
  </span>
)

export { cx }
