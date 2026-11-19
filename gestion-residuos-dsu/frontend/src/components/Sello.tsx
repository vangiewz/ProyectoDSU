import { cx } from './ui'

/** Estados que se asientan como sello sobre la planilla. */
const tintas = {
  ATENDIDO: 'text-sello-ok',
  'SIN RESIDUOS': 'text-sello-ok',
  OMITIDO: 'text-sello-omit',
  PENDIENTE: 'text-sello-omit',
  ATENDIDA: 'text-sello-ok',
  PLANIFICADA: 'text-grafito-2',
  CONFIRMADA: 'text-boligrafo',
  'EN EJECUCIÓN': 'text-sello-omit',
  CERRADA: 'text-dsu',
  VIGENTE: 'text-sello-ok',
  APROBADO: 'text-boligrafo',
  RECHAZADO: 'text-sello-omit',
  FALLIDO: 'text-dsu',
  'EN CURSO': 'text-boligrafo',
  ACEPTADA: 'text-sello-ok',
  DESCARTADA: 'text-grafito-2',
  REEMPLAZADA: 'text-grafito-2',
  'URGENCIA ALTA': 'text-dsu',
  'URGENCIA MEDIA': 'text-sello-omit',
  'URGENCIA BAJA': 'text-grafito-2',
} as const

export type EstadoSello = keyof typeof tintas

const ESTADO_JORNADA: Record<string, EstadoSello> = {
  PLANIFICADA: 'PLANIFICADA',
  CONFIRMADA: 'CONFIRMADA',
  EN_EJECUCION: 'EN EJECUCIÓN',
  CERRADA: 'CERRADA',
}

export const selloDeJornada = (estado: string) => ESTADO_JORNADA[estado] ?? 'PLANIFICADA'

export function Sello({ estado, nota, recien, className }: { estado: EstadoSello; nota?: string; recien?: boolean; className?: string }) {
  return (
    <span className={cx('sello', tintas[estado], recien && 'sello-recien', className)}>
      {estado}
      {nota && <span className="font-semibold [font-stretch:85%]">{nota}</span>}
    </span>
  )
}
