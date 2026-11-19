# -*- coding: utf-8 -*-
"""Realizacion de cada caso de uso para el capitulo 6 (diagramas de
colaboracion) con clases de analisis: interfaz (boundary), control y entidad.

Cada caso de uso tiene: quien inicia (clave de actor o nombre de objeto),
la vista, el controlador y una lista de operaciones. Cada operacion es
(mensaje del actor a la vista, mensaje de la vista al controlador,
[(destino, mensaje del controlador)]). La numeracion 1, 1.1, 1.2... se
genera sola. Un destino "CU9" significa el controlador de ese caso de uso.

Los nombres de entidades son los de las clases del backend (User, AuditLog,
Group = rol) para que coincidan con el diagrama de clases del capitulo 7.
"""
import datos as D

CONTROL_CU = {9: "VisitaController", 15: "JornadaController"}

R = {
    1: dict(ini=D.TODOS, vista="LoginView", ctrl="AuthController", ops=[
        ("iniciarSesion(usuario, clave)", "login(credenciales)",
         [("User", "buscarPorUsuario(usuario)"), ("User", "verificarClave(clave)"),
          ("BitacoraController", "registrar(LOGIN)")])]),
    2: dict(ini=D.TODOS, vista="MenuView", ctrl="AuthController", ops=[
        ("cerrarSesion()", "logout(refresh)",
         [("TokenRenovacion", "invalidar(refresh)"), ("BitacoraController", "registrar(LOGOUT)")])]),
    3: dict(ini=D.ADM, vista="UsuariosView", ctrl="UserController", ops=[
        ("listar()", "findAll()", [("User", "find()")]),
        ("registrar(datos)", "create(dto)",
         [("Group", "find(roles)"), ("User", "create(dto)"), ("BitacoraController", "registrar(ALTA)")]),
        ("actualizar(id, datos)", "update(id, dto)",
         [("User", "update(dto)"), ("BitacoraController", "registrar(MODIFICACION)")]),
        ("desactivar(id)", "desactivar(id)",
         [("User", "setActivo(false)"), ("BitacoraController", "registrar(BAJA)")])]),
    4: dict(ini=D.ADM, vista="RolesView", ctrl="RoleController", ops=[
        ("listar()", "findAll()", [("Group", "find()")]),
        ("registrar(nombre, permisos)", "create(dto)",
         [("Permission", "find(ids)"), ("Group", "create(dto)"), ("BitacoraController", "registrar(ALTA)")]),
        ("modificarPermisos(id, permisos)", "update(id, dto)",
         [("Group", "setPermisos(ids)"), ("BitacoraController", "registrar(MODIFICACION)")])]),
    5: dict(ini=D.ADM, vista="SectoresView", ctrl="SectorController", ops=[
        ("listar()", "findAll()", [("Sector", "find()")]),
        ("registrar(datos)", "create(dto)",
         [("User", "find(supervisor)"), ("Sector", "create(dto)"), ("BitacoraController", "registrar(ALTA)")]),
        ("actualizar(id, datos)", "update(id, dto)",
         [("Sector", "update(dto)"), ("BitacoraController", "registrar(MODIFICACION)")]),
        ("desactivar(id)", "desactivar(id)",
         [("PuntoRecoleccion", "contarActivos(sector)"), ("Sector", "setActivo(false)")])]),
    6: dict(ini=D.SUP, vista="PuntosView", ctrl="PuntoRecoleccionController", ops=[
        ("listar(filtros)", "findAll(filtros)", [("PuntoRecoleccion", "find(filtros)")]),
        ("registrar(datos, lat, lon)", "create(dto)",
         [("Sector", "find(id)"), ("PuntoRecoleccion", "validarCoordenadas()"),
          ("PuntoRecoleccion", "create(dto)"), ("BitacoraController", "registrar(ALTA)")]),
        ("desactivar(id, motivo)", "desactivar(id, motivo)",
         [("PuntoRecoleccion", "setActivo(false)"), ("BitacoraController", "registrar(BAJA)")])]),
    7: dict(ini=D.SUP, vista="ContenedoresView", ctrl="ContenedorController", ops=[
        ("listar(punto)", "findAll(punto)", [("Contenedor", "find(punto)")]),
        ("registrar(datos)", "create(dto)",
         [("PuntoRecoleccion", "find(id)"), ("Contenedor", "create(dto)"),
          ("BitacoraController", "registrar(ALTA)")]),
        ("cambiarEstado(id, estado)", "update(id, dto)",
         [("Contenedor", "setEstado(estado)"), ("BitacoraController", "registrar(MODIFICACION)")])]),
    8: dict(ini=D.ADM, vista="CatalogosView", ctrl="CatalogoController", ops=[
        ("listar()", "findAll()", [("TipoResiduo", "find()"), ("UnidadMedida", "find()")]),
        ("registrarTipo(datos)", "createTipo(dto)",
         [("UnidadMedida", "find(id)"), ("TipoResiduo", "create(dto)"),
          ("BitacoraController", "registrar(ALTA)")]),
        ("registrarUnidad(datos)", "createUnidad(dto)",
         [("UnidadMedida", "create(dto)"), ("BitacoraController", "registrar(ALTA)")]),
        ("actualizarUnidad(id, factor)", "updateUnidad(id, dto)",
         [("RegistroResiduo", "existenCon(unidad)"), ("UnidadMedida", "update(dto)")])]),
    9: dict(ini=D.POL, vista="CampoView", ctrl="VisitaController", ops=[
        ("verRuta()", "siguientePunto(jornada)",
         [("Jornada", "find(id)"), ("JornadaPunto", "siguientePendiente()")]),
        ("registrarVaciado(detalles)", "registrarVisita(jornada, punto, detalles)",
         [("Jornada", "exigirEnEjecucion()"), ("PuntoRecoleccion", "capacidad()"),
          ("RegistroResiduo", "create(detalle)"), ("JornadaPunto", "marcarVisitado()")])]),
    10: dict(ini=D.POL, vista="IncidenciaView", ctrl="IncidenciaController", ops=[
        ("registrarIncidencia(datos)", "create(dto)",
         [("PuntoRecoleccion", "find(id)"), ("Jornada", "find(id)"),
          ("Incidencia", "create(dto)")])]),
    11: dict(ini=D.SUP, vista="IncidenciasView", ctrl="IncidenciaController", ops=[
        ("listarPendientes()", "findAll(PENDIENTE)", [("Incidencia", "find(sector)")]),
        ("atender(id, accion)", "atender(id, accion)",
         [("Incidencia", "atender(accion, usuario)"), ("BitacoraController", "registrar(MODIFICACION)")])]),
    12: dict(ini=D.SUP, vista="RegistrosView", ctrl="RegistroResiduoController", ops=[
        ("consultar(filtros)", "findAll(filtros)",
         [("RegistroResiduo", "find(filtros)"), ("RegistroResiduo", "totalesPorTipo()")]),
        ("verDetalle(id)", "findOne(id)",
         [("RegistroResiduo", "find(id)"), ("Jornada", "find(jornada)")])]),
    13: dict(ini=D.SUP, vista="VehiculosView", ctrl="VehiculoController", ops=[
        ("listar()", "findAll()", [("Vehiculo", "find()")]),
        ("registrar(datos)", "create(dto)",
         [("Vehiculo", "create(dto)"), ("BitacoraController", "registrar(ALTA)")]),
        ("actualizar(id, datos)", "update(id, dto)",
         [("Vehiculo", "update(dto)"), ("BitacoraController", "registrar(MODIFICACION)")])]),
    14: dict(ini=D.SUP, vista="JornadasView", ctrl="JornadaController", ops=[
        ("nuevaJornada(fecha, turno, sector)", "puntosPropuestos(sector)",
         [("PuntoRecoleccion", "find(sector)"), ("Recomendacion", "aceptadas(sector)")]),
        ("guardar(datos, ruta)", "create(dto)",
         [("Jornada", "create(dto)"), ("JornadaPunto", "create(orden)")]),
        ("asignar(personal, vehiculos)", "asignar(id, recursos)", [("CU15", "asignar()")]),
        ("confirmar(id)", "confirmar(id)",
         [("Jornada", "setEstado(CONFIRMADA)"), ("BitacoraController", "registrar(MODIFICACION)")])]),
    15: dict(ini=D.SUP, vista="JornadasView", ctrl="JornadaController", ops=[
        ("verDisponibles(turno)", "disponibles(fecha, turno)",
         [("User", "find(OPERATIVO)"), ("Vehiculo", "find(OPERATIVO)")]),
        ("asignar(personal, vehiculos, responsable)", "asignar(id, recursos)",
         [("Jornada", "validarSuperposicion()"), ("Jornada", "setPersonal(ids)"),
          ("Jornada", "setVehiculos(ids)")])]),
    16: dict(ini=D.SUP, vista="CampoView", ctrl="JornadaController", ops=[
        ("abrir(jornada)", "abrir(id)",
         [("Jornada", "exigirEstado(CONFIRMADA)"), ("Jornada", "setEstado(EN_EJECUCION)")]),
        ("atenderPunto(punto)", "registrarVisita(punto, detalles)", [("CU9", "registrarVisita()")]),
        ("verAvance()", "avance(id)", [("JornadaPunto", "contarPorEstado()")])]),
    17: dict(ini=D.POL, vista="CampoView", ctrl="JornadaController", ops=[
        ("omitir(punto, motivo)", "omitir(id, punto, motivo)",
         [("JornadaPunto", "exigirPendiente()"), ("JornadaPunto", "marcarOmitido(motivo)")])]),
    18: dict(ini=D.SUP, vista="JornadasView", ctrl="JornadaController", ops=[
        ("verResumen(id)", "resumen(id)",
         [("RegistroResiduo", "totalesPorTipo(jornada)"), ("JornadaPunto", "contarPorEstado()")]),
        ("cerrar(id, observaciones)", "cerrar(id, obs)",
         [("JornadaPunto", "exigirSinPendientes()"), ("Jornada", "setEstado(CERRADA)"),
          ("BitacoraController", "registrar(CIERRE)")])]),
    19: dict(ini=D.SUP, vista="JornadasView", ctrl="JornadaController", ops=[
        ("consultar(filtros)", "findAll(filtros)",
         [("Jornada", "find(filtros)"), ("JornadaPunto", "cobertura()")]),
        ("verDetalle(id)", "findOne(id)",
         [("RegistroResiduo", "find(jornada)"), ("Incidencia", "find(jornada)")])]),
    20: dict(ini=D.ADM, vista="EtlView", ctrl="EtlController", ops=[
        ("ejecutarETL()", "ejecutar()",
         [("EjecucionETL", "iniciar(usuario)"), ("RegistroResiduo", "pendientes()"),
          ("UnidadMedida", "factores()"), ("PeriodoAcademico", "find()"),
          ("HechoResiduo", "cargar(df)"), ("RegistroDescartado", "create(motivo)"),
          ("EjecucionETL", "finalizar(conteos)"), ("BitacoraController", "registrar(ETL)")])]),
    21: dict(ini=D.CDD, vista="TableroView", ctrl="AnaliticaController", ops=[
        ("abrirTablero(filtros)", "indicadores(alcance)", [("IndicadoresController", "indicadores()")]),
        ("filtrar(sector, tipo)", "indicadores(alcance)", [("IndicadoresController", "indicadores()")]),
        ("abrirPowerBI()", "powerbi()", [("ParametrosSistema", "enlacePowerBI()")])]),
    22: dict(ini=D.CDD, vista="TableroView", ctrl="AnaliticaController", ops=[
        ("comparar(base, comparacion)", "comparacion(base, comp)",
         [("HechoResiduo", "totales(base)"), ("HechoResiduo", "totales(comp)"),
          ("HechoResiduo", "serieMensual()")])]),
    23: dict(ini=D.SUP, vista="MapaView", ctrl="AnaliticaController", ops=[
        ("abrirMapa()", "mapa(alcance)",
         [("PuntoRecoleccion", "find(activos)"), ("HechoResiduo", "totalesPorPunto()")]),
        ("seleccionarPunto(id)", "detallePunto(id)",
         [("PuntoRecoleccion", "find(id)"), ("Contenedor", "capacidad(punto)")])]),
    24: dict(ini=D.CDD, vista="MapaView", ctrl="AnaliticaController", ops=[
        ("activarCalor(observada)", "mapa(alcance)",
         [("HechoResiduo", "totalesPorPunto()"), ("ParametrosSistema", "umbralCritico()")]),
        ("activarCalor(proyectada)", "mapaProyectado(alcance)",
         [("Prediccion", "vigentesPorPunto()")])]),
    25: dict(ini=D.SUP, vista="MapaView", ctrl="AnaliticaController", ops=[
        ("aplicarFiltros(filtros)", "mapa(alcance)",
         [("HechoResiduo", "totalesPorPunto(alcance)"), ("PuntoRecoleccion", "find(sector)")])]),
    26: dict(ini=D.ADM, vista="ModeloView", ctrl="ModeloController", ops=[
        ("verPropuestos()", "propuestos()", [("ParametrosSistema", "hiperparametros()")]),
        ("entrenar(hiperparametros)", "entrenar(hp)",
         [("HechoResiduo", "serieDiaria()"), ("ParametrosSistema", "minimoRegistros()"),
          ("ModeloEntrenado", "create(version)"), ("ModeloEntrenado", "evaluar(prueba)"),
          ("BitacoraController", "registrar(ENTRENAMIENTO)")])]),
    27: dict(ini=D.ADM, vista="ModeloView", ctrl="ModeloController", ops=[
        ("listarVersiones()", "findAll()", [("ModeloEntrenado", "find()")]),
        ("publicar(id)", "publicar(id)",
         [("ModeloEntrenado", "vigente()"), ("ModeloEntrenado", "setVigente(true)"),
          ("BitacoraController", "registrar(PUBLICACION)")])]),
    28: dict(ini=D.SUP, vista="PrediccionView", ctrl="PrediccionController", ops=[
        ("predecir(horizonte, sector)", "create(horizonte, alcance)",
         [("ModeloEntrenado", "vigente()"), ("HechoResiduo", "estadoActual(puntos)"),
          ("LotePrediccion", "create(modelo)"), ("Prediccion", "create(estimacion, margen)"),
          ("RecomendacionController", "evaluar(lote)")]),
        ("verLote(id)", "retrieve(id)", [("Prediccion", "agrupar(sector, tipo)")])]),
    29: dict(ini=D.SUP, vista="RecomendacionesView", ctrl="RecomendacionController", ops=[
        ("listar(filtros)", "findAll(filtros)", [("Recomendacion", "find(alcance)")]),
        ("verEvidencia(id)", "findOne(id)",
         [("Recomendacion", "find(id)"), ("Prediccion", "find(lote, punto)")])]),
    30: dict(ini=D.SUP, vista="RecomendacionesView", ctrl="RecomendacionController", ops=[
        ("aceptar(id, motivo)", "aceptar(id, motivo)",
         [("Recomendacion", "resolver(ACEPTADA)"), ("Jornada", "proximaPlanificada(sector)"),
          ("JornadaPunto", "priorizar(punto)"), ("BitacoraController", "registrar(RESOLUCION)")]),
        ("descartar(id, motivo)", "descartar(id, motivo)",
         [("Recomendacion", "resolver(DESCARTADA)"), ("BitacoraController", "registrar(RESOLUCION)")])]),
    31: dict(ini=D.ADM, vista="ParametrosView", ctrl="ParametrosController", ops=[
        ("verParametros()", "get()", [("ParametrosSistema", "actual()")]),
        ("modificar(parametro, valor)", "patch(dto)",
         [("ParametrosSistema", "validarRango()"), ("ParametrosSistema", "update(dto)"),
          ("BitacoraController", "registrar(MODIFICACION)")]),
        ("registrarPeriodo(inicio, fin)", "createPeriodo(dto)",
         [("PeriodoAcademico", "validarSuperposicion()"), ("PeriodoAcademico", "create(dto)")])]),
    32: dict(ini=D.ADM, vista="BitacoraView", ctrl="BitacoraController", ops=[
        ("consultar(filtros)", "findAll(filtros)", [("AuditLog", "find(filtros)")]),
        ("verDetalle(id)", "findOne(id)", [("AuditLog", "find(id)")])]),
    33: dict(ini=D.ADM, vista="ReportesView", ctrl="ReporteController", ops=[
        ("generar(tipo, filtros)", "generar(tipo, alcance)",
         [("HechoResiduo", "totales(alcance)"), ("Jornada", "find(alcance)"),
          ("Incidencia", "find(alcance)"), ("Prediccion", "vigentes()")]),
        ("imprimir()", "vistaImpresion()", [])]),
    34: dict(ini=D.ADM, vista="ReportesView", ctrl="ExportacionController", ops=[
        ("exportar(formato)", "exportar(reporte, formato)",
         [("Reporte", "encabezado(alcance)"),
          ("BitacoraController", "registrar(REPORTE)")])]),
}

assert sorted(R) == list(range(1, 35))
