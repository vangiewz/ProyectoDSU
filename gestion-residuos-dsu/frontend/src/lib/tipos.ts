export type Parada = {
  id: number
  punto: number
  codigo: string
  nombre: string
  latitud: string
  longitud: string
  orden: number
  atendido: boolean | null
  sin_generacion: boolean
  motivo_omision: string
  atendido_en: string | null
}

export type Jornada = {
  id: number
  fecha: string
  turno: 'MANANA' | 'TARDE' | 'NOCHE'
  turno_display: string
  sector: number
  sector_nombre: string
  estado: 'PLANIFICADA' | 'CONFIRMADA' | 'EN_EJECUCION' | 'CERRADA'
  estado_display: string
  descripcion: string
  responsable: number | null
  responsable_nombre: string | null
  personal: number[]
  personal_detalle: { id: number; nombre: string }[]
  vehiculos: number[]
  hora_inicio: string | null
  hora_fin: string | null
  observaciones_cierre: string
  ruta: Parada[]
  puntos_planificados: number
  puntos_atendidos: number
}

export type Resumen = {
  planificados: number
  atendidos: number
  pendientes: number
  cobertura: number
  omitidos: { punto__codigo: string; motivo_omision: string }[]
  total_kg: string | number
  total_litros: string | number
  por_tipo: { tipo_residuo__nombre: string; unidad__magnitud: 'PESO' | 'VOLUMEN'; total: string }[]
  incidencias: number
  incidencias_pendientes: number
}

export type TipoResiduo = { id: number; nombre: string; clasificacion: string; unidad: number; unidad_simbolo: string }
