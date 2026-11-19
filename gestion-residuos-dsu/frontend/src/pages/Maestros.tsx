import { useState } from 'react'

import { CrudPage, opcionesDe, type CrudConfig, type Fila } from '../components/Crud'
import { MapaPuntos, type PuntoMapa } from '../components/Mapa'
import { cx } from '../components/ui'
import { numero } from '../lib/datos'

const txt = (k: string) => (f: Fila) => (f[k] as string) || '—'
const mono = (k: string) => (f: Fila) => <span className="font-semibold [font-stretch:85%]">{String(f[k] ?? '—')}</span>

const sectores = () => opcionesDe('sectores/', (f) => `${f.codigo} · ${f.nombre}`, { is_active: 'true' })

const cfgSectores: CrudConfig = {
  recurso: 'sectores',
  titulo: 'Sectores y facultades',
  detalle: 'Unidades territoriales del campus sobre las que se agregan registros, indicadores y predicciones.',
  modelo: 'campus.sector',
  columnas: [
    { titulo: 'Código', celda: mono('codigo') },
    { titulo: 'Nombre', celda: txt('nombre') },
    { titulo: 'Tipo', celda: txt('tipo_display') },
    { titulo: 'Supervisor', celda: txt('supervisor_nombre') },
    { titulo: 'Puntos activos', celda: (f) => numero(f.puntos_activos as number), derecha: true },
  ],
  campos: [
    { nombre: 'codigo', etiqueta: 'Código', requerido: true },
    { nombre: 'nombre', etiqueta: 'Nombre', requerido: true },
    {
      nombre: 'tipo',
      etiqueta: 'Tipo',
      tipo: 'seleccion',
      requerido: true,
      opciones: [
        { valor: 'FACULTAD', texto: 'Facultad' },
        { valor: 'MODULO', texto: 'Módulo' },
        { valor: 'AREA_COMUN', texto: 'Área común' },
        { valor: 'UNIDAD_DESCONCENTRADA', texto: 'Unidad desconcentrada' },
      ],
    },
    {
      nombre: 'supervisor',
      etiqueta: 'Supervisor responsable',
      tipo: 'seleccion',
      opciones: () => opcionesDe('usuarios/', (f) => `${f.first_name} ${f.last_name}`, { groups__name: 'Supervisor', is_active: 'true' }),
    },
    { nombre: 'descripcion', etiqueta: 'Descripción', tipo: 'area' },
  ],
  inicial: { tipo: 'FACULTAD' },
  filtros: [{ nombre: 'is_active', etiqueta: 'Estado', opciones: [{ valor: 'true', texto: 'Activos' }, { valor: 'false', texto: 'Inactivos' }] }],
}

const cfgPuntos: CrudConfig = {
  recurso: 'puntos',
  titulo: 'Puntos de recolección',
  detalle: 'Contenedores y basureros georreferenciados del campus. Toque un punto del mapa para ver su código.',
  modelo: 'campus.puntorecoleccion',
  arriba: (filas) => <MapaPuntos puntos={filas as unknown as PuntoMapa[]} />,
  columnas: [
    { titulo: 'Código', celda: mono('codigo') },
    { titulo: 'Nombre', celda: txt('nombre') },
    { titulo: 'Sector', celda: txt('sector_nombre') },
    { titulo: 'Capacidad', celda: (f) => `${numero(f.capacidad_kg as string)} kg`, derecha: true },
    { titulo: 'Contenedores', celda: (f) => (f.capacidad_contenedores_litros ? `${numero(f.capacidad_contenedores_litros as string)} L` : '—'), derecha: true },
    { titulo: 'Condición', celda: txt('estado_display') },
  ],
  campos: [
    { nombre: 'sector', etiqueta: 'Sector', tipo: 'seleccion', requerido: true, opciones: sectores },
    { nombre: 'codigo', etiqueta: 'Código', requerido: true },
    { nombre: 'nombre', etiqueta: 'Nombre o referencia corta', requerido: true },
    { nombre: 'referencia', etiqueta: 'Cómo llegar', tipo: 'area' },
    { nombre: 'ubicacion', etiqueta: 'Ubicación', tipo: 'coordenadas' },
    { nombre: 'capacidad_kg', etiqueta: 'Capacidad estimada (kg)', tipo: 'numero', paso: '0.01', requerido: true },
    {
      nombre: 'estado',
      etiqueta: 'Condición operativa',
      tipo: 'seleccion',
      opciones: [
        { valor: 'OPERATIVO', texto: 'Operativo' },
        { valor: 'OBSERVADO', texto: 'Observado' },
        { valor: 'FUERA_SERVICIO', texto: 'Fuera de servicio' },
      ],
    },
  ],
  inicial: { estado: 'OPERATIVO' },
  pideMotivo: true,
  filtros: [{ nombre: 'is_active', etiqueta: 'Estado', opciones: [{ valor: 'true', texto: 'Activos' }, { valor: 'false', texto: 'Inactivos' }] }],
}

const cfgContenedores: CrudConfig = {
  recurso: 'contenedores',
  titulo: 'Contenedores',
  detalle: 'Capacidad instalada en cada punto. Los cambios de estado quedan en la bitácora.',
  modelo: 'campus.contenedor',
  columnas: [
    { titulo: 'Código', celda: mono('codigo') },
    { titulo: 'Punto', celda: txt('punto_codigo') },
    { titulo: 'Tipo', celda: txt('tipo') },
    { titulo: 'Capacidad', celda: (f) => `${numero(f.capacidad_litros as string)} L`, derecha: true },
    { titulo: 'Estado', celda: txt('estado_display') },
  ],
  campos: [
    { nombre: 'punto', etiqueta: 'Punto de recolección', tipo: 'seleccion', requerido: true, opciones: () => opcionesDe('puntos/', (f) => `${f.codigo} · ${f.nombre}`, { is_active: 'true' }) },
    { nombre: 'codigo', etiqueta: 'Código', requerido: true },
    { nombre: 'tipo', etiqueta: 'Tipo de contenedor', requerido: true, ayuda: 'Ej.: turril plástico, contenedor metálico, basurero de pasillo.' },
    { nombre: 'capacidad_litros', etiqueta: 'Capacidad (L)', tipo: 'numero', paso: '0.01', requerido: true },
    { nombre: 'fecha_instalacion', etiqueta: 'Fecha de instalación', tipo: 'fecha', requerido: true },
    {
      nombre: 'estado',
      etiqueta: 'Estado',
      tipo: 'seleccion',
      opciones: [
        { valor: 'BUENO', texto: 'Bueno' },
        { valor: 'DETERIORADO', texto: 'Deteriorado' },
        { valor: 'REEMPLAZADO', texto: 'Reemplazado' },
        { valor: 'REUBICADO', texto: 'Reubicado' },
        { valor: 'BAJA', texto: 'De baja' },
      ],
    },
    { nombre: 'observacion', etiqueta: 'Observación', tipo: 'area' },
  ],
  inicial: { estado: 'BUENO' },
}

const cfgVehiculos: CrudConfig = {
  recurso: 'vehiculos',
  titulo: 'Vehículos',
  detalle: 'Flota asignada a las jornadas de recolección.',
  modelo: 'operations.vehiculo',
  columnas: [
    { titulo: 'Placa', celda: mono('placa') },
    { titulo: 'Descripción', celda: txt('descripcion') },
    { titulo: 'Capacidad', celda: (f) => (f.capacidad_kg ? `${numero(f.capacidad_kg as string)} kg` : '—'), derecha: true },
    { titulo: 'Condición', celda: txt('estado_display') },
  ],
  campos: [
    { nombre: 'placa', etiqueta: 'Placa', requerido: true },
    { nombre: 'descripcion', etiqueta: 'Descripción', requerido: true },
    { nombre: 'capacidad_kg', etiqueta: 'Capacidad (kg)', tipo: 'numero', paso: '0.01' },
    {
      nombre: 'estado',
      etiqueta: 'Condición',
      tipo: 'seleccion',
      opciones: [
        { valor: 'OPERATIVO', texto: 'Operativo' },
        { valor: 'FUERA_SERVICIO', texto: 'Fuera de servicio' },
      ],
    },
  ],
  inicial: { estado: 'OPERATIVO' },
}

const unidades = () => opcionesDe('unidades/', (f) => `${f.nombre} (${f.simbolo})`, { is_active: 'true' })

const cfgTipos: CrudConfig = {
  recurso: 'tipos-residuo',
  titulo: 'Tipos de residuo',
  detalle: 'Catálogo que el personal elige al registrar cada vaciado.',
  modelo: 'catalogs.tiporesiduo',
  columnas: [
    { titulo: 'Nombre', celda: (f) => <span className="font-semibold">{String(f.nombre)}</span> },
    { titulo: 'Clasificación', celda: txt('clasificacion_display') },
    { titulo: 'Aprovechable', celda: (f) => (f.aprovechable ? 'Sí' : 'No') },
    { titulo: 'Unidad', celda: txt('unidad_simbolo') },
  ],
  campos: [
    { nombre: 'nombre', etiqueta: 'Nombre', requerido: true },
    {
      nombre: 'clasificacion',
      etiqueta: 'Clasificación',
      tipo: 'seleccion',
      requerido: true,
      opciones: [
        { valor: 'ORGANICO', texto: 'Orgánico' },
        { valor: 'RECICLABLE', texto: 'Reciclable' },
        { valor: 'NO_APROVECHABLE', texto: 'No aprovechable' },
        { valor: 'PELIGROSO', texto: 'Peligroso' },
        { valor: 'ESPECIAL', texto: 'Especial' },
      ],
    },
    { nombre: 'aprovechable', etiqueta: 'Es aprovechable', tipo: 'casilla' },
    { nombre: 'unidad', etiqueta: 'Unidad de medida', tipo: 'seleccion', requerido: true, opciones: unidades },
    { nombre: 'descripcion', etiqueta: 'Descripción', tipo: 'area' },
  ],
}

const cfgUnidades: CrudConfig = {
  recurso: 'unidades',
  titulo: 'Unidades de medida',
  detalle: 'El factor convierte cada unidad a su base (kg o L). No puede cambiarse si la unidad ya tiene registros.',
  modelo: 'catalogs.unidadmedida',
  columnas: [
    { titulo: 'Nombre', celda: txt('nombre') },
    { titulo: 'Símbolo', celda: mono('simbolo') },
    { titulo: 'Magnitud', celda: (f) => (f.magnitud === 'PESO' ? 'Peso' : 'Volumen') },
    { titulo: 'Factor a base', celda: (f) => numero(f.factor_conversion as string), derecha: true },
  ],
  campos: [
    { nombre: 'nombre', etiqueta: 'Nombre', requerido: true },
    { nombre: 'simbolo', etiqueta: 'Símbolo', requerido: true },
    {
      nombre: 'magnitud',
      etiqueta: 'Magnitud',
      tipo: 'seleccion',
      requerido: true,
      opciones: [
        { valor: 'PESO', texto: 'Peso (base kg)' },
        { valor: 'VOLUMEN', texto: 'Volumen (base L)' },
      ],
    },
    { nombre: 'factor_conversion', etiqueta: 'Factor de conversión a la base', tipo: 'numero', paso: '0.000001', requerido: true },
  ],
}

const cfgPeriodos: CrudConfig = {
  recurso: 'periodos',
  titulo: 'Periodos académicos',
  detalle: 'Calendario que el análisis y la predicción usarán como variable. Los periodos no pueden superponerse.',
  modelo: 'catalogs.periodoacademico',
  sinBusqueda: true,
  columnas: [
    { titulo: 'Periodo', celda: (f) => <span className="font-semibold">{String(f.nombre)}</span> },
    { titulo: 'Inicio', celda: txt('fecha_inicio') },
    { titulo: 'Fin', celda: txt('fecha_fin') },
  ],
  campos: [
    { nombre: 'nombre', etiqueta: 'Nombre', requerido: true, ayuda: 'Ej.: 2-2026' },
    { nombre: 'fecha_inicio', etiqueta: 'Inicio', tipo: 'fecha', requerido: true },
    { nombre: 'fecha_fin', etiqueta: 'Fin', tipo: 'fecha', requerido: true },
  ],
}

export const Sectores = () => <CrudPage config={cfgSectores} />
export const Puntos = () => <CrudPage config={cfgPuntos} />
export const Contenedores = () => <CrudPage config={cfgContenedores} />
export const Vehiculos = () => <CrudPage config={cfgVehiculos} />

export function Catalogos() {
  const pestanas = [
    { id: 'tipos', texto: 'Tipos de residuo', cfg: cfgTipos },
    { id: 'unidades', texto: 'Unidades de medida', cfg: cfgUnidades },
    { id: 'periodos', texto: 'Periodos académicos', cfg: cfgPeriodos },
  ]
  const [activa, setActiva] = useState('tipos')
  const actual = pestanas.find((p) => p.id === activa)!
  return (
    <>
      <div role="tablist" aria-label="Catálogos" className="mb-6 flex gap-1 border-b border-filete">
        {pestanas.map((p) => (
          <button
            key={p.id}
            role="tab"
            aria-selected={p.id === activa}
            onClick={() => setActiva(p.id)}
            className={cx(
              '-mb-px min-h-11 border-b-2 px-4 text-sm font-semibold transition-colors duration-100',
              p.id === activa ? 'border-dsu text-grafito' : 'border-transparent text-grafito-2 hover:text-grafito',
            )}
          >
            {p.texto}
          </button>
        ))}
      </div>
      <CrudPage key={actual.id} config={actual.cfg} />
    </>
  )
}
