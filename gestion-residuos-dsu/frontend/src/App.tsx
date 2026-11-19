import type { ReactNode } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router'

import { NAVEGACION, Shell } from './components/Shell'
import { Cargando, Vacio } from './components/ui'
import { AuthProvider, useAuth } from './lib/auth'
import { Bitacora, Roles, Usuarios } from './pages/Admin'
import { Campo } from './pages/Campo'
import { DetalleJornada, Jornadas, NuevaJornada } from './pages/Jornadas'
import { Login } from './pages/Login'
import { MapaCampus } from './pages/MapaCampus'
import { ModeloPredictivo } from './pages/Modelo'
import { Predicciones } from './pages/Prediccion'
import { Recomendaciones } from './pages/Recomendaciones'
import { Catalogos, Contenedores, Puntos, Sectores, Vehiculos } from './pages/Maestros'
import { Historico, Incidencias } from './pages/Registros'
import { Reportes } from './pages/Reportes'
import { ParametrosPage, ProcesoETL } from './pages/Sistema'
import { Tablero } from './pages/Tablero'

/** Ruta visible solo con el permiso; el servidor vuelve a validarlo en cada operación. */
function Con({ permiso, children }: { permiso: string; children: ReactNode }) {
  const { puede } = useAuth()
  return puede(permiso) ? children : <Vacio titulo="Sin acceso">Su rol no tiene permiso para este módulo.</Vacio>
}

/** Pantalla de inicio según el rol: el operativo va directo al registro en campo. */
function Inicio() {
  const { yo, puede } = useAuth()
  if (yo?.roles.includes('Operativo') && puede('operations.ejecutar_jornada')) return <Navigate to="/campo" replace />
  if (yo?.roles.includes('Directivo') && puede('analytics.view_hechoresiduo')) return <Navigate to="/tablero" replace />
  const primero = NAVEGACION.flatMap((g) => g.items).find((i) => puede(i.permiso))
  return primero ? <Navigate to={primero.a === '/campo' ? '/jornadas' : primero.a} replace /> : <Vacio titulo="Su cuenta no tiene módulos asignados" />
}

function Rutas() {
  const { yo, cargando } = useAuth()
  if (cargando) return <Cargando texto="Verificando sesión…" />
  if (!yo) return <Login />
  return (
    <Routes>
      <Route element={<Shell />}>
        <Route index element={<Inicio />} />
        <Route path="campo" element={<Con permiso="operations.ejecutar_jornada"><Campo /></Con>} />
        <Route path="jornadas" element={<Con permiso="operations.view_jornada"><Jornadas /></Con>} />
        <Route path="jornadas/nueva" element={<Con permiso="operations.add_jornada"><NuevaJornada /></Con>} />
        <Route path="jornadas/:id/editar" element={<Con permiso="operations.change_jornada"><NuevaJornada /></Con>} />
        <Route path="jornadas/:id" element={<Con permiso="operations.view_jornada"><DetalleJornada /></Con>} />
        <Route path="historico" element={<Con permiso="operations.view_registroresiduo"><Historico /></Con>} />
        <Route path="incidencias" element={<Con permiso="operations.view_incidencia"><Incidencias /></Con>} />
        <Route path="tablero" element={<Con permiso="analytics.view_hechoresiduo"><Tablero /></Con>} />
        <Route path="mapa" element={<Con permiso="analytics.view_hechoresiduo"><MapaCampus /></Con>} />
        <Route path="predicciones" element={<Con permiso="prediction.view_prediccion"><Predicciones /></Con>} />
        <Route path="recomendaciones" element={<Con permiso="prediction.view_recomendacion"><Recomendaciones /></Con>} />
        <Route path="modelo" element={<Con permiso="prediction.view_modeloentrenado"><ModeloPredictivo /></Con>} />
        <Route path="reportes" element={<Con permiso="analytics.generar_reporte"><Reportes /></Con>} />
        <Route path="procesos" element={<Con permiso="analytics.view_ejecucionetl"><ProcesoETL /></Con>} />
        <Route path="parametros" element={<Con permiso="catalogs.view_parametrossistema"><ParametrosPage /></Con>} />
        <Route path="sectores" element={<Con permiso="campus.view_sector"><Sectores /></Con>} />
        <Route path="puntos" element={<Con permiso="campus.view_puntorecoleccion"><Puntos /></Con>} />
        <Route path="contenedores" element={<Con permiso="campus.view_contenedor"><Contenedores /></Con>} />
        <Route path="tipos-residuo" element={<Con permiso="catalogs.view_tiporesiduo"><Catalogos /></Con>} />
        <Route path="vehiculos" element={<Con permiso="operations.view_vehiculo"><Vehiculos /></Con>} />
        <Route path="usuarios" element={<Con permiso="accounts.view_user"><Usuarios /></Con>} />
        <Route path="roles" element={<Con permiso="auth.view_group"><Roles /></Con>} />
        <Route path="bitacora" element={<Con permiso="audit.view_auditlog"><Bitacora /></Con>} />
        <Route path="*" element={<Vacio titulo="Página no encontrada" />} />
      </Route>
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Rutas />
      </AuthProvider>
    </BrowserRouter>
  )
}
