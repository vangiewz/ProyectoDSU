import { FileSpreadsheet, FileText, Printer } from 'lucide-react'
import { useState } from 'react'

import { FiltrosAnalisis, consulta, filtrosIniciales, type Filtros } from '../components/FiltrosAnalisis'
import { Aviso, Boton, Cargando, Encabezado, cx } from '../components/ui'
import { api } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fecha, numero, useCarga } from '../lib/datos'

const TIPOS = [
  { id: 'generacion-sector', texto: 'Generación por sector', detalle: 'Kilos y litros por sector, con registros y puntos.' },
  { id: 'generacion-tipo', texto: 'Generación por tipo de residuo', detalle: 'Totales por tipo en el periodo.' },
  { id: 'cumplimiento-jornadas', texto: 'Cumplimiento de jornadas', detalle: 'Planificado frente a ejecutado, con cobertura.' },
  { id: 'incidencias', texto: 'Incidencias registradas', detalle: 'Tipo, gravedad, estado y acción adoptada.' },
  { id: 'indicadores', texto: 'Indicadores del periodo', detalle: 'Resumen gerencial de indicadores.' },
  { id: 'prediccion', texto: 'Generación proyectada', detalle: 'Predicción vigente por punto, con su margen de error.', permiso: 'prediction.view_prediccion' },
]

type Vista = { titulo: string; columnas: string[]; filas: (string | number | null)[][]; numericas: number[] }

function celda(v: string | number | null) {
  if (v === null) return '—'
  if (typeof v === 'number' || /^-?\d+(\.\d+)?$/.test(v)) return numero(v)
  if (/^\d{4}-\d{2}-\d{2}$/.test(v)) return fecha(v)
  return v
}

export function Reportes() {
  const { puede } = useAuth()
  const tipos = TIPOS.filter((t) => !t.permiso || puede(t.permiso))
  const [tipo, setTipo] = useState(TIPOS[0].id)
  const [filtros, setFiltros] = useState<Filtros>(() => filtrosIniciales())
  const [ocupado, setOcupado] = useState<string | null>(null)
  const [aviso, setAviso] = useState<string | null>(null)
  const { data, error, cargando } = useCarga(() => api<Vista>(`reportes/${tipo}/`, { query: consulta(filtros) }), [tipo, JSON.stringify(filtros)])

  async function obtener(formato: 'xlsx' | 'pdf', accion: 'descargar' | 'imprimir') {
    setOcupado(`${formato}-${accion}`)
    setAviso(null)
    try {
      const blob = await api<Blob>(`reportes/${tipo}/`, { query: { ...consulta(filtros), formato }, archivo: true })
      const url = URL.createObjectURL(blob)
      if (accion === 'imprimir') {
        const marco = document.createElement('iframe')
        marco.style.cssText = 'position:fixed;width:0;height:0;border:0'
        marco.src = url
        marco.onload = () => marco.contentWindow?.print()
        document.body.appendChild(marco)
        setTimeout(() => {
          marco.remove()
          URL.revokeObjectURL(url)
        }, 60_000)
      } else {
        const a = document.createElement('a')
        a.href = url
        a.download = `dsu-${tipo}.${formato}`
        a.click()
        URL.revokeObjectURL(url)
      }
    } catch (e) {
      setAviso(e instanceof Error ? e.message : String(e))
    } finally {
      setOcupado(null)
    }
  }

  return (
    <>
      <Encabezado
        titulo="Reportes"
        detalle="Cada reporte sale con el encabezado institucional, la fecha de emisión y su usuario, y su emisión queda en la bitácora."
        acciones={
          <>
            <Boton variante="secundario" cargando={ocupado === 'xlsx-descargar'} onClick={() => void obtener('xlsx', 'descargar')} disabled={!data || cargando}>
              <FileSpreadsheet className="size-4" aria-hidden /> Excel
            </Boton>
            <Boton variante="secundario" cargando={ocupado === 'pdf-descargar'} onClick={() => void obtener('pdf', 'descargar')} disabled={!data || cargando}>
              <FileText className="size-4" aria-hidden /> PDF
            </Boton>
            <Boton cargando={ocupado === 'pdf-imprimir'} onClick={() => void obtener('pdf', 'imprimir')} disabled={!data || cargando}>
              <Printer className="size-4" aria-hidden /> Imprimir
            </Boton>
          </>
        }
      />
      <div role="radiogroup" aria-label="Tipo de reporte" className="mb-5 grid gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        {tipos.map((t) => (
          <button
            key={t.id}
            role="radio"
            aria-checked={tipo === t.id}
            onClick={() => setTipo(t.id)}
            className={cx(
              'rounded-hoja border bg-hoja px-3 py-2.5 text-left transition-colors duration-100',
              tipo === t.id ? 'border-grafito ring-1 ring-grafito' : 'border-filete hover:border-grafito-2',
            )}
          >
            <span className="block text-sm font-bold">{t.texto}</span>
            <span className="mt-0.5 block text-xs text-grafito-2">{t.detalle}</span>
          </button>
        ))}
      </div>
      {tipo === 'prediccion' && (
        <div className="mb-4">
          <Aviso>Usa la predicción vigente de cada punto con su propio horizonte; de los filtros solo se aplican el sector y el punto.</Aviso>
        </div>
      )}
      <FiltrosAnalisis valor={filtros} cambiar={setFiltros} sinPunto={tipo === 'cumplimiento-jornadas'} />
      {aviso && (
        <div className="mb-4">
          <Aviso tono="error">{aviso}</Aviso>
        </div>
      )}
      {error && <Aviso tono="error">{error}</Aviso>}
      {cargando && <Cargando texto="Preparando el reporte…" />}
      {data && !cargando && (
        <section className="overflow-x-auto rounded-hoja border border-filete bg-hoja">
          <header className="flex items-baseline justify-between gap-3 border-b border-filete px-4 py-3">
            <h2 className="font-bold">{data.titulo}</h2>
            <span className="text-xs text-grafito-2">{data.filas.length} fila(s)</span>
          </header>
          {data.filas.length ? (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-filete">
                  {data.columnas.map((c, i) => (
                    <th key={c} className={cx('rotulo px-3 py-2', data.numericas.includes(i) ? 'text-right' : 'text-left')}>
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.filas.map((f, i) => (
                  <tr key={i} className="border-b border-filete-suave last:border-0">
                    {f.map((v, j) => (
                      <td key={j} className={cx('px-3 py-2', data.numericas.includes(j) && 'text-right')}>
                        {celda(v)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="px-4 py-8 text-center text-sm text-grafito-2">No existe información para el periodo y los filtros seleccionados.</p>
          )}
        </section>
      )}
    </>
  )
}
