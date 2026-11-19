import { AlertOctagon, Ban, Check, ChevronDown, PackageOpen, Plus, X } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router'

import { Sello } from '../components/Sello'
import { Area, Aviso, Boton, Campo as CampoForm, Cargando, Entrada, Seleccion, Vacio, cx } from '../components/ui'
import { api, type Pagina } from '../lib/api'
import { useAuth } from '../lib/auth'
import { fecha, hora, useCarga } from '../lib/datos'
import type { Jornada, Parada, TipoResiduo } from '../lib/tipos'

type Detalle = { tipo: TipoResiduo; cantidad: string }

const GRAVEDADES = [
  { valor: 'BAJA', texto: 'Baja' },
  { valor: 'MEDIA', texto: 'Media' },
  { valor: 'ALTA', texto: 'Alta' },
  { valor: 'CRITICA', texto: 'Crítica' },
]
const TIPOS_INCIDENCIA = [
  { valor: 'CONTENEDOR_DANADO', texto: 'Contenedor dañado' },
  { valor: 'ACCESO_BLOQUEADO', texto: 'Acceso bloqueado' },
  { valor: 'MAL_SEGREGADO', texto: 'Residuos mal segregados' },
  { valor: 'RESIDUO_PELIGROSO', texto: 'Residuo peligroso' },
  { valor: 'DESBORDE', texto: 'Desborde' },
  { valor: 'OTRO', texto: 'Otro' },
]

/** Lista comprimida de paradas: las registradas con su sello, la actual resaltada. */
function Recorrido({ ruta, actual, recien, elegir }: { ruta: Parada[]; actual?: number; recien: number | null; elegir: (p: Parada) => void }) {
  return (
    <ol className="flex flex-col">
      {ruta.map((p) => (
        <li key={p.id}>
          <button
            onClick={() => elegir(p)}
            className={cx(
              'flex min-h-12 w-full items-center gap-3 border-b border-filete-suave px-1 text-left text-sm',
              p.id === actual && 'font-bold text-grafito',
              p.atendido !== null && 'text-grafito-2',
            )}
            aria-current={p.id === actual ? 'step' : undefined}
          >
            <span className="w-5 text-right text-xs">{p.orden}</span>
            <span className="font-semibold [font-stretch:85%]">{p.codigo}</span>
            <span className="min-w-0 flex-1 truncate">{p.nombre}</span>
            {p.atendido === true && <Sello estado={p.sin_generacion ? 'SIN RESIDUOS' : 'ATENDIDO'} nota={hora(p.atendido_en)} recien={recien === p.id} />}
            {p.atendido === false && <Sello estado="OMITIDO" recien={recien === p.id} />}
            {p.atendido === null && p.id === actual && <span className="text-xs font-semibold text-boligrafo">Ahora</span>}
          </button>
        </li>
      ))}
    </ol>
  )
}

function Incidencia({ jornada, parada, listo }: { jornada: Jornada; parada: Parada; listo: (msg: string) => void }) {
  const [tipo, setTipo] = useState('')
  const [gravedad, setGravedad] = useState('MEDIA')
  const [descripcion, setDescripcion] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  async function enviar() {
    setEnviando(true)
    setError(null)
    try {
      await api('incidencias/', { body: { jornada: jornada.id, punto: parada.punto, tipo, gravedad, descripcion } })
      listo('Incidencia reportada. El supervisor del sector ya la ve como pendiente.')
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="flex flex-col gap-3 rounded-hoja border border-filete bg-hoja p-4">
      <h3 className="font-bold">Incidencia en {parada.codigo}</h3>
      {error && <Aviso tono="error">{error}</Aviso>}
      <div className="grid grid-cols-2 gap-2">
        {TIPOS_INCIDENCIA.map((t) => (
          <button
            key={t.valor}
            onClick={() => setTipo(t.valor)}
            aria-pressed={tipo === t.valor}
            className={cx(
              'min-h-12 rounded-hoja border px-2 text-sm font-semibold',
              tipo === t.valor ? 'border-boligrafo bg-boligrafo text-white' : 'border-filete bg-hoja text-grafito',
            )}
          >
            {t.texto}
          </button>
        ))}
      </div>
      <CampoForm etiqueta="Gravedad">
        <Seleccion value={gravedad} onChange={(e) => setGravedad(e.target.value)} className="min-h-12">
          {GRAVEDADES.map((g) => (
            <option key={g.valor} value={g.valor}>
              {g.texto}
            </option>
          ))}
        </Seleccion>
      </CampoForm>
      <CampoForm etiqueta="Qué pasó">
        <Area value={descripcion} onChange={(e) => setDescripcion(e.target.value)} />
      </CampoForm>
      <Boton grande cargando={enviando} disabled={!tipo || !descripcion.trim()} onClick={() => void enviar()}>
        Enviar incidencia
      </Boton>
    </div>
  )
}

function RegistroParada({ jornada, parada, tipos, registrado }: { jornada: Jornada; parada: Parada; tipos: TipoResiduo[]; registrado: (msg: string) => void }) {
  const [detalles, setDetalles] = useState<Detalle[]>([])
  const [tipoSel, setTipoSel] = useState<TipoResiduo | null>(null)
  const [cantidad, setCantidad] = useState('')
  const [observaciones, setObservaciones] = useState('')
  const [verObs, setVerObs] = useState(false)
  const [modo, setModo] = useState<'registro' | 'omitir' | 'incidencia'>('registro')
  const [motivo, setMotivo] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  const todos: Detalle[] = [...detalles, ...(tipoSel && Number(cantidad) > 0 ? [{ tipo: tipoSel, cantidad }] : [])]

  async function enviar(ruta: 'visitas' | 'omitir', body: unknown, ok: string) {
    setEnviando(true)
    setError(null)
    try {
      await api(`jornadas/${jornada.id}/${ruta}/`, { body })
      registrado(ok)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setEnviando(false)
    }
  }

  const registrar = () =>
    void enviar(
      'visitas',
      { punto: parada.punto, observaciones, detalles: todos.map((d) => ({ tipo_residuo: d.tipo.id, cantidad: d.cantidad })) },
      `${parada.codigo} registrado.`,
    )

  return (
    <section aria-labelledby="parada-actual" className="flex flex-col gap-4">
      <div className="rounded-hoja border border-filete bg-hoja p-4">
        <p className="rotulo">Parada {parada.orden} de {jornada.ruta.length}</p>
        <h2 id="parada-actual" className="mt-1 text-[2.5rem] leading-none font-extrabold tracking-tight [font-stretch:75%]">
          {parada.codigo}
        </h2>
        <p className="mt-1 text-grafito-2">{parada.nombre}</p>
      </div>

      {error && <Aviso tono="error">{error}</Aviso>}

      {modo === 'registro' && (
        <>
          <fieldset>
            <legend className="rotulo mb-2">¿Qué residuo retira?</legend>
            <div className="grid grid-cols-2 gap-2">
              {tipos.map((t) => (
                <button
                  key={t.id}
                  onClick={() => setTipoSel(t)}
                  aria-pressed={tipoSel?.id === t.id}
                  className={cx(
                    'min-h-14 rounded-hoja border-2 px-3 text-left text-[0.95rem] leading-tight font-semibold transition-colors duration-100',
                    tipoSel?.id === t.id ? 'border-boligrafo bg-boligrafo text-white' : 'border-filete bg-hoja text-grafito active:border-boligrafo',
                  )}
                >
                  {t.nombre}
                </button>
              ))}
            </div>
          </fieldset>

          {tipoSel && (
            <CampoForm etiqueta={`Cantidad de ${tipoSel.nombre.toLowerCase()}`}>
              <div className="flex items-center gap-2">
                <Entrada
                  autoFocus
                  type="number"
                  inputMode="decimal"
                  min="0"
                  step="0.1"
                  value={cantidad}
                  onChange={(e) => setCantidad(e.target.value)}
                  className="min-h-16 flex-1 text-center !text-[2rem] font-bold"
                  aria-describedby="unidad"
                />
                <span id="unidad" className="w-12 text-xl font-bold text-grafito-2">
                  {tipoSel.unidad_simbolo}
                </span>
              </div>
            </CampoForm>
          )}

          {detalles.length > 0 && (
            <ul className="flex flex-col gap-1 text-sm">
              {detalles.map((d, i) => (
                <li key={i} className="flex items-center justify-between rounded-hoja bg-hoja px-3 py-2">
                  <span>{d.tipo.nombre}</span>
                  <span className="flex items-center gap-2">
                    <span className="tinta font-bold">
                      {d.cantidad} {d.tipo.unidad_simbolo}
                    </span>
                    <button onClick={() => setDetalles(detalles.filter((_, j) => j !== i))} className="p-2 text-dsu" aria-label={`Quitar ${d.tipo.nombre}`}>
                      <X className="size-4" />
                    </button>
                  </span>
                </li>
              ))}
            </ul>
          )}

          {tipoSel && Number(cantidad) > 0 && (
            <button
              onClick={() => {
                setDetalles(todos)
                setTipoSel(null)
                setCantidad('')
              }}
              className="inline-flex min-h-11 items-center gap-2 self-start text-sm font-semibold text-boligrafo"
            >
              <Plus className="size-4" aria-hidden /> Agregar otro tipo en esta parada
            </button>
          )}

          <button onClick={() => setVerObs(!verObs)} className="inline-flex min-h-11 items-center gap-1 self-start text-sm font-semibold text-grafito-2" aria-expanded={verObs}>
            <ChevronDown className={cx('size-4 transition-transform duration-100', verObs && 'rotate-180')} aria-hidden /> Observaciones
          </button>
          {verObs && <Area value={observaciones} onChange={(e) => setObservaciones(e.target.value)} aria-label="Observaciones" />}

          <div className="sticky bottom-0 -mx-4 flex flex-col gap-2 border-t border-filete bg-papel px-4 pt-3 pb-[max(0.75rem,env(safe-area-inset-bottom))]">
            <Boton grande cargando={enviando} disabled={!todos.length} onClick={registrar}>
              <Check className="size-5" aria-hidden /> Registrar vaciado
            </Boton>
            <div className="grid grid-cols-3 gap-2">
              <Boton
                variante="secundario"
                className="min-h-12 text-xs"
                disabled={enviando}
                onClick={() => void enviar('visitas', { punto: parada.punto, sin_generacion: true, observaciones }, `${parada.codigo}: visita sin residuos.`)}
              >
                <PackageOpen className="size-4" aria-hidden /> Sin residuos
              </Boton>
              <Boton variante="secundario" className="min-h-12 text-xs" onClick={() => setModo('omitir')}>
                <Ban className="size-4" aria-hidden /> No pude
              </Boton>
              <Boton variante="secundario" className="min-h-12 text-xs" onClick={() => setModo('incidencia')}>
                <AlertOctagon className="size-4" aria-hidden /> Incidencia
              </Boton>
            </div>
          </div>
        </>
      )}

      {modo === 'omitir' && (
        <div className="flex flex-col gap-3 rounded-hoja border border-filete bg-hoja p-4">
          <h3 className="font-bold">¿Por qué no se pudo atender {parada.codigo}?</h3>
          <div className="flex flex-wrap gap-2">
            {['Acceso bloqueado', 'Punto sin contenedor', 'Falta de tiempo', 'Contenedor dañado'].map((m) => (
              <button key={m} onClick={() => setMotivo(m)} className={cx('min-h-11 rounded-hoja border px-3 text-sm', motivo === m ? 'border-boligrafo text-boligrafo' : 'border-filete')}>
                {m}
              </button>
            ))}
          </div>
          <Area value={motivo} onChange={(e) => setMotivo(e.target.value)} aria-label="Motivo" />
          <Boton grande cargando={enviando} disabled={!motivo.trim()} onClick={() => void enviar('omitir', { punto: parada.punto, motivo }, `${parada.codigo} omitido.`)}>
            Confirmar omisión
          </Boton>
          <Boton variante="fantasma" onClick={() => setModo('registro')}>
            Volver al registro
          </Boton>
        </div>
      )}

      {modo === 'incidencia' && (
        <>
          <Incidencia
            jornada={jornada}
            parada={parada}
            listo={(msg) => {
              setModo('registro')
              registrado(msg)
            }}
          />
          <Boton variante="fantasma" onClick={() => setModo('registro')}>
            Volver al registro
          </Boton>
        </>
      )}
    </section>
  )
}

export function Campo() {
  const { puede } = useAuth()
  const [params] = useSearchParams()
  const [version, setVersion] = useState(0)
  const [elegida, setElegida] = useState<number | null>(null)
  const [recien, setRecien] = useState<number | null>(null)
  const [aviso, setAviso] = useState<{ tono: 'ok' | 'error'; texto: string } | null>(null)
  const [abriendo, setAbriendo] = useState(false)

  const idParam = params.get('jornada')
  const jornadas = useCarga(
    () => (idParam ? api<Jornada>(`jornadas/${idParam}/`).then((j) => [j]) : api<Jornada[]>('jornadas/mias/')),
    [idParam, version],
  )
  const tipos = useCarga(() => api<Pagina<TipoResiduo>>('tipos-residuo/', { query: { is_active: 'true', page_size: 100 } }), [])

  const j = jornadas.data?.find((x) => x.estado === 'EN_EJECUCION') ?? jornadas.data?.[0]
  const parada = useMemo(() => {
    if (!j) return undefined
    return j.ruta.find((p) => p.id === elegida && p.atendido === null) ?? j.ruta.find((p) => p.atendido === null)
  }, [j, elegida])

  useEffect(() => {
    if (!aviso) return
    const t = setTimeout(() => setAviso(null), 5000)
    return () => clearTimeout(t)
  }, [aviso])

  async function abrir() {
    if (!j) return
    setAbriendo(true)
    try {
      await api(`jornadas/${j.id}/abrir/`, { body: {} })
      setVersion((v) => v + 1)
    } catch (e) {
      setAviso({ tono: 'error', texto: e instanceof Error ? e.message : String(e) })
    } finally {
      setAbriendo(false)
    }
  }

  if (jornadas.cargando && !jornadas.data) return <Cargando texto="Buscando su jornada de hoy…" />
  if (jornadas.error) return <Aviso tono="error">{jornadas.error}</Aviso>
  if (!j)
    return (
      <div className="mx-auto max-w-md">
        <Vacio titulo="No tiene jornadas para hoy">Cuando su supervisor confirme una jornada con usted en la cuadrilla, aparecerá aquí.</Vacio>
      </div>
    )

  const hechos = j.ruta.filter((p) => p.atendido !== null).length

  return (
    <div className="mx-auto flex max-w-md flex-col gap-4">
      <header className="flex items-end justify-between gap-3">
        <div>
          <p className="rotulo">
            {fecha(j.fecha)} · {j.turno_display}
          </p>
          <h1 className="text-xl font-bold [font-stretch:88%]">{j.sector_nombre}</h1>
        </div>
        <p className="text-right text-sm">
          <span className="tinta text-2xl font-bold">{hechos}</span>
          <span className="text-grafito-2"> / {j.ruta.length} puntos</span>
        </p>
      </header>

      {aviso && <Aviso tono={aviso.tono}>{aviso.texto}</Aviso>}

      {j.estado === 'CONFIRMADA' && (
        <div className="flex flex-col gap-3 rounded-hoja border border-filete bg-hoja p-4">
          <p>La jornada está confirmada. Ábrala al iniciar el recorrido para registrar los vaciados.</p>
          {puede('operations.ejecutar_jornada') && (
            <Boton grande cargando={abriendo} onClick={() => void abrir()}>
              Abrir jornada
            </Boton>
          )}
        </div>
      )}

      {j.estado === 'EN_EJECUCION' && parada && tipos.data && (
        <RegistroParada
          key={parada.id}
          jornada={j}
          parada={parada}
          tipos={tipos.data.results}
          registrado={(msg) => {
            setRecien(parada.id)
            setElegida(null)
            setAviso({ tono: 'ok', texto: msg })
            setVersion((v) => v + 1)
          }}
        />
      )}

      {j.estado === 'EN_EJECUCION' && !parada && (
        <div className="flex flex-col items-start gap-3 rounded-hoja border border-filete bg-hoja p-4">
          <Sello estado="ATENDIDO" nota="ruta completa" />
          <p>Todos los puntos tienen registro. Avise a su supervisor para cerrar la jornada.</p>
          {puede('operations.cerrar_jornada') && (
            <Link to={`/jornadas/${j.id}`} className="font-semibold text-boligrafo underline">
              Ir a cerrar la jornada
            </Link>
          )}
        </div>
      )}

      {j.estado === 'CERRADA' && <Aviso>Esta jornada ya está cerrada.</Aviso>}

      <section aria-label="Recorrido">
        <h2 className="rotulo mb-1">Recorrido</h2>
        <Recorrido ruta={j.ruta} actual={parada?.id} recien={recien} elegir={(p) => p.atendido === null && setElegida(p.id)} />
      </section>
    </div>
  )
}
