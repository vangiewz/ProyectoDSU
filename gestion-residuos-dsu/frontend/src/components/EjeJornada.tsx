import type { Parada } from '../lib/tipos'
import { hora } from '../lib/datos'
import { cx } from './ui'

const INICIO = 8 * 60
const FIN = 15 * 60
const HORAS = [8, 9, 10, 11, 12, 13, 14, 15]

const minutos = (iso: string) => {
  const d = new Date(iso)
  return d.getHours() * 60 + d.getMinutes()
}

/** La jornada sobre el horario real de la DSU (08:00–15:00): cada atención cae en su hora. */
export function EjeJornada({ ruta, inicio, fin }: { ruta: Parada[]; inicio: string | null; fin: string | null }) {
  const marcas = ruta.filter((p) => p.atendido_en)
  const pos = (iso: string) => `${Math.min(100, Math.max(0, ((minutos(iso) - INICIO) / (FIN - INICIO)) * 100))}%`

  return (
    <figure className="rounded-hoja border border-filete bg-hoja px-5 pt-4 pb-3">
      <figcaption className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
        <span className="rotulo">Horario de la jornada</span>
        <span className="text-xs text-grafito-2">
          Inicio <span className="tinta font-semibold">{hora(inicio)}</span> · Cierre <span className="tinta font-semibold">{hora(fin)}</span>
        </span>
      </figcaption>
      <div className="relative h-16">
        <div className="absolute inset-x-0 top-9 border-t border-filete" />
        {inicio && fin && (
          <div className="absolute top-[34px] h-[5px] rounded-full bg-boligrafo/15" style={{ left: pos(inicio), right: `calc(100% - ${pos(fin)})` }} />
        )}
        {inicio && !fin && <div className="absolute top-[34px] right-0 h-[5px] rounded-full bg-boligrafo/15" style={{ left: pos(inicio) }} />}
        {marcas.map((p, i) => (
          <div
            key={p.id}
            className="absolute -translate-x-1/2"
            style={{ left: pos(p.atendido_en!), top: i % 2 ? 0 : 14 }}
            title={`${p.codigo} · ${hora(p.atendido_en)}${p.atendido ? '' : ` · omitido: ${p.motivo_omision}`}`}
          >
            <span
              className={cx(
                'block rounded-[2px] border-2 px-1 text-[0.62rem] leading-tight font-extrabold [font-stretch:70%]',
                p.atendido ? 'border-sello-ok bg-hoja text-sello-ok' : 'border-sello-omit bg-hoja text-sello-omit',
              )}
            >
              {p.codigo}
            </span>
          </div>
        ))}
      </div>
      <div className="relative h-4 text-[0.68rem] text-grafito-2">
        {HORAS.map((h) => (
          <span key={h} className="absolute -translate-x-1/2" style={{ left: `${((h * 60 - INICIO) / (FIN - INICIO)) * 100}%` }}>
            {String(h).padStart(2, '0')}:00
          </span>
        ))}
      </div>
    </figure>
  )
}
