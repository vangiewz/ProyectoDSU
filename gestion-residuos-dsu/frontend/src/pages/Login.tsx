import { useState, type FormEvent } from 'react'

import { Aviso, Boton, Campo, Entrada } from '../components/ui'
import { ApiError } from '../lib/api'
import { useAuth } from '../lib/auth'

export function Login() {
  const { entrar } = useAuth()
  const [usuario, setUsuario] = useState('')
  const [clave, setClave] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  async function enviar(e: FormEvent) {
    e.preventDefault()
    setEnviando(true)
    setError(null)
    try {
      await entrar(usuario.trim(), clave)
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 401
          ? 'Usuario o contraseña incorrectos, o la cuenta está desactivada.'
          : err instanceof ApiError && err.status === 429
            ? 'Demasiados intentos. Espere un minuto y vuelva a intentar.'
            : err instanceof Error
              ? err.message
              : String(err),
      )
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="grid min-h-dvh lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)]">
      <section className="flex flex-col justify-between bg-dsu px-6 py-8 text-white sm:px-12 lg:py-14">
        <span className="grid h-16 w-fit place-items-center rounded-[4px] bg-white px-3 text-[2.6rem] leading-none font-extrabold tracking-tight text-dsu [font-stretch:78%] lg:h-28 lg:px-5 lg:text-[4.75rem]">
          DSU
        </span>
        <div className="mt-8 lg:mt-0">
          <p className="max-w-md text-xl leading-snug font-semibold [font-stretch:90%] lg:text-[1.75rem]">Dirección de Servicios Universitarios</p>
          <p className="mt-2 text-sm text-white/85">Universidad Autónoma Gabriel René Moreno · Gestión de residuos sólidos</p>
        </div>
      </section>

      <section className="flex items-center justify-center px-6 py-10">
        <form onSubmit={enviar} className="flex w-full max-w-sm flex-col gap-5">
          <div>
            <h1 className="text-2xl font-bold [font-stretch:88%]">Ingresar al sistema</h1>
            <p className="mt-1 text-sm text-grafito-2">Use las credenciales que le asignó el administrador.</p>
          </div>
          {error && <Aviso tono="error">{error}</Aviso>}
          <Campo etiqueta="Usuario">
            <Entrada autoComplete="username" autoCapitalize="none" value={usuario} onChange={(e) => setUsuario(e.target.value)} required className="min-h-12" />
          </Campo>
          <Campo etiqueta="Contraseña">
            <Entrada type="password" autoComplete="current-password" value={clave} onChange={(e) => setClave(e.target.value)} required className="min-h-12" />
          </Campo>
          <Boton type="submit" grande cargando={enviando} disabled={!usuario || !clave}>
            Ingresar
          </Boton>
        </form>
      </section>
    </div>
  )
}
