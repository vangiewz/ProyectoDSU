import { CircleMarker, MapContainer, TileLayer, Tooltip, useMapEvents } from 'react-leaflet'

import { Entrada } from './ui'

// Ciudad Universitaria UAGRM (aprox.).
export const CENTRO_CAMPUS: [number, number] = [-17.7762, -63.1952]

const capaBase = (
  <TileLayer
    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    maxZoom={19}
  />
)

export type PuntoMapa = {
  id: number
  codigo: string
  nombre: string
  latitud: string
  longitud: string
  sector_nombre?: string
  estado?: string
  is_active?: boolean
}

const colorPunto = (p: PuntoMapa) =>
  p.is_active === false ? '#4a5560' : p.estado === 'FUERA_SERVICIO' ? '#c4122f' : p.estado === 'OBSERVADO' ? '#9a5b00' : '#1f3fa8'

export function MapaPuntos({ puntos, alto = 'h-80' }: { puntos: PuntoMapa[]; alto?: string }) {
  const centro: [number, number] = puntos.length ? [Number(puntos[0].latitud), Number(puntos[0].longitud)] : CENTRO_CAMPUS
  return (
    <div className={`${alto} overflow-hidden rounded-hoja border border-filete`}>
      <MapContainer center={centro} zoom={17} scrollWheelZoom={false} className="h-full w-full">
        {capaBase}
        {puntos.map((p) => (
          <CircleMarker
            key={p.id}
            center={[Number(p.latitud), Number(p.longitud)]}
            radius={8}
            pathOptions={{ color: '#ffffff', weight: 2, fillColor: colorPunto(p), fillOpacity: 1 }}
          >
            <Tooltip>
              <strong>{p.codigo}</strong> · {p.nombre}
              {p.sector_nombre && <br />}
              {p.sector_nombre}
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  )
}

function Clic({ alClic }: { alClic: (lat: number, lon: number) => void }) {
  useMapEvents({ click: (e) => alClic(e.latlng.lat, e.latlng.lng) })
  return null
}

export function SelectorCoordenadas({
  latitud,
  longitud,
  cambiar,
}: {
  latitud?: string
  longitud?: string
  cambiar: (lat: string, lon: string) => void
}) {
  const hay = latitud && longitud && !Number.isNaN(Number(latitud)) && !Number.isNaN(Number(longitud))
  const pos: [number, number] = hay ? [Number(latitud), Number(longitud)] : CENTRO_CAMPUS
  return (
    <div className="flex flex-col gap-2">
      <div className="h-56 overflow-hidden rounded-hoja border border-filete">
        <MapContainer center={pos} zoom={17} className="h-full w-full">
          {capaBase}
          <Clic alClic={(lat, lon) => cambiar(lat.toFixed(6), lon.toFixed(6))} />
          {hay && <CircleMarker center={pos} radius={9} pathOptions={{ color: '#fff', weight: 2, fillColor: '#1f3fa8', fillOpacity: 1 }} />}
        </MapContainer>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <Entrada aria-label="Latitud" placeholder="Latitud" inputMode="decimal" value={latitud ?? ''} onChange={(e) => cambiar(e.target.value, longitud ?? '')} />
        <Entrada aria-label="Longitud" placeholder="Longitud" inputMode="decimal" value={longitud ?? ''} onChange={(e) => cambiar(latitud ?? '', e.target.value)} />
      </div>
    </div>
  )
}
