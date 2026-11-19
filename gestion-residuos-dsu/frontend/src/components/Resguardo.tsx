import { RotateCcw } from 'lucide-react'
import { Component, type ReactNode } from 'react'

import { Aviso, Boton } from './ui'

/** Si una pantalla falla al dibujarse, el resto del sistema sigue en pie y se ofrece recargar. */
export class Resguardo extends Component<{ children: ReactNode }, { error: Error | null }> {
  state: { error: Error | null } = { error: null }

  static getDerivedStateFromError(error: Error) {
    return { error }
  }

  render() {
    if (!this.state.error) return this.props.children
    return (
      <div className="flex max-w-2xl flex-col items-start gap-3">
        <Aviso tono="error">
          Esta pantalla no pudo mostrarse. Recargue la página; si el problema sigue, avise al administrador del sistema.
        </Aviso>
        <Boton variante="secundario" onClick={() => window.location.reload()}>
          <RotateCcw className="size-4" aria-hidden /> Recargar
        </Boton>
      </div>
    )
  }
}
