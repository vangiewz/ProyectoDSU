# -*- coding: utf-8 -*-
"""Especificacion del capitulo 7 que no sale de esquema.json: despliegue,
capas logicas, servicios, composiciones y diagramas de secuencia.
Verificado contra backend/Dockerfile, docker-compose.yml, config/settings.py y
docs/ESTADO.md (2026-10-18)."""

# ----------------------------------------------------------------------
# 7.1.1 despliegue: nodos con sus artefactos y conexiones con protocolo
# ----------------------------------------------------------------------
NODOS = [
    # clave, nombre, tipo EA, estereotipo, [artefactos], (x, y, w, h)
    # los dos navegadores arriba y abajo, con las teselas entre ellos y el
    # hosting a la izquierda: asi sus cuatro conexiones no se cruzan; a la
    # derecha Power BI, el servidor y la base de datos
    ("pc", "PC de oficina (DSU)", "Device", "device",
     ["Navegador web: SPA React (escritorio)"], (520, 40, 300, 130)),
    ("osm", "Servidores de teselas OpenStreetMap", "Node", "",
     ["tile.openstreetmap.org"], (520, 400, 300, 130)),
    ("movil", "Teléfono del operario", "Device", "device",
     ["Navegador móvil: SPA React (campo)"], (520, 760, 300, 130)),
    ("vercel", "Vercel (hosting estático)", "Node", "",
     ["frontend: build de Vite (HTML, JS, CSS)", "sitio corporativo Residata (HTML)"], (40, 360, 300, 210)),
    ("pbi", "Microsoft Power BI (Desktop / Service)", "Node", "",
     ["DSU-Residuos.pbip (informe publicado)"], (1000, 40, 340, 130)),
    ("srv", "Azure VM: Ubuntu 24.04 y Docker (Mexico Central)", "Node", "",
     ["Caddy: proxy inverso con TLS (443)", "Contenedor app: Gunicorn + Django REST",
      "Modelo Random Forest (.joblib)", "cron: ETL programado",
      "Contenedor respaldo: pg_dump diario"], (1000, 290, 340, 340)),
    ("neon", "Neon: PostgreSQL 18 (São Paulo)", "Node", "",
     ["Base de datos dsu", "Vistas bi_*", "Trigger de bitácora inalterable"],
     (1000, 760, 340, 230)),
]
CONEXIONES = [
    ("pc", "vercel", "HTTPS (TLS 1.2+, puerto 443)"),
    ("pc", "srv", "HTTPS 443 · API REST/JSON con JWT"),
    ("pc", "osm", "HTTPS 443 · teselas del mapa"),
    ("pc", "pbi", "HTTPS 443 · informe insertado (iframe)"),
    ("movil", "vercel", "HTTPS 443 · red 4G / Wi-Fi"),
    ("movil", "srv", "HTTPS 443 · API REST/JSON con JWT"),
    ("movil", "osm", "HTTPS 443 · teselas del mapa"),
    ("srv", "neon", "Protocolo PostgreSQL sobre TLS (5432, sslmode=require)"),
    ("pbi", "neon", "PostgreSQL/TLS 5432 | rol powerbi de solo lectura"),
]
# conexiones que rodean un nodo: clave -> quiebres (x, y)
RODEOS = {("pbi", "neon"): [(1480, 105), (1480, 875)]}

# ----------------------------------------------------------------------
# 7.1.2 diseno logico: capas (coherentes con la figura de arquitectura del
# capitulo 4) y paquetes de cada capa
# ----------------------------------------------------------------------
CAPAS = [
    # (capa, [(paquete, columna, fila)]): la ubicacion evita que una dependencia
    # atraviese otro paquete de la misma capa
    ("Capa de presentación (React + Vite)",
     [("Páginas (vistas de los CU)", 1, 0), ("Componentes reutilizables", 0, 1),
      ("Cliente API (JWT)", 1, 1), ("Cartografía (Leaflet)", 2, 1)]),
    ("Capa de servicios (Django REST Framework)",
     [("Autenticación JWT y permisos por rol", 0, 0), ("Controladores (ViewSets)", 1, 0),
      ("Serializadores", 2, 0), ("Servicio de inferencia", 3, 0)]),
    ("Capa de lógica de negocio (Django)", None),      # grupos de abajo
    ("Capa de datos",
     [("ORM de Django (modelos)", 0, 0), ("Artefactos del modelo (.joblib)", 3, 0),
      ("PostgreSQL (Neon)", 1, 1), ("Vistas analíticas bi_*", 2, 1)]),
]
# la capa de negocio en dos grupos: las aplicaciones de dominio (centro de cada
# paquete dentro del grupo; ubicacion buscada para que sus dependencias no se
# crucen) y las transversales, que usan todas las demas
DOMINIO = ("Aplicaciones de dominio", {
    "analytics (ETL, indicadores, reportes)": (330, 70),
    "prediction (Random Forest)": (690, 450),
    "operations": (300, 480),
    "campus": (450, 380),
    "catalogs": (90, 630),
})
TRANSVERSALES = ("Transversales", ["accounts", "audit (bitácora)"])
# (nombre, capa con la que trabaja, fila de esa capa; None = al medio)
EXTERNOS = [("OpenStreetMap", 0, 1), ("Pandas / NumPy · scikit-learn", 2, None),
            ("Microsoft Power BI", 3, 1)]
# dependencias reales (imports del backend y del frontend, 30/10/2026); los
# nombres de capa o de grupo apuntan al marco completo
_AN, _PR = "analytics (ETL, indicadores, reportes)", "prediction (Random Forest)"
DEP_LOGICAS = [
    ("Páginas (vistas de los CU)", "Componentes reutilizables"),
    ("Páginas (vistas de los CU)", "Cliente API (JWT)"),
    ("Páginas (vistas de los CU)", "Cartografía (Leaflet)"),
    ("Componentes reutilizables", "Cliente API (JWT)"),
    ("Cartografía (Leaflet)", "OpenStreetMap"),
    ("Cliente API (JWT)", "Controladores (ViewSets)"),
    ("Controladores (ViewSets)", "Serializadores"),
    ("Controladores (ViewSets)", "Autenticación JWT y permisos por rol"),
    ("Controladores (ViewSets)", "Capa de lógica de negocio (Django)"),
    ("Serializadores", "Capa de lógica de negocio (Django)"),
    ("Servicio de inferencia", _PR),
    ("Autenticación JWT y permisos por rol", "accounts"),
    ("operations", "campus"), ("operations", "catalogs"),
    (_AN, "operations"), (_AN, "campus"), (_AN, "catalogs"), (_AN, _PR),
    (_PR, _AN), (_PR, "operations"), (_PR, "campus"), (_PR, "catalogs"),
    ("Aplicaciones de dominio", "Transversales"),
    ("accounts", "audit (bitácora)"),
    (_AN, "Pandas / NumPy · scikit-learn"), (_PR, "Pandas / NumPy · scikit-learn"),
    (_PR, "Artefactos del modelo (.joblib)"),
    ("Capa de lógica de negocio (Django)", "ORM de Django (modelos)"),
    ("ORM de Django (modelos)", "PostgreSQL (Neon)"),
    ("Vistas analíticas bi_*", "PostgreSQL (Neon)"),
    ("Microsoft Power BI", "Vistas analíticas bi_*"),
]

# ----------------------------------------------------------------------
# 7.2 clases de servicio (logica de negocio) con sus metodos reales
# ----------------------------------------------------------------------
SERVICIOS = [
    ("JornadaService", "operations/services/jornada.py",
     ["asignar(jornada, personal, vehiculos, responsable)", "confirmar(jornada)",
      "abrir(jornada)", "cerrar(jornada, observaciones)", "resumen(jornada): dict"],
     ["Jornada", "JornadaPunto", "User", "Vehiculo"]),
    ("VisitaService", "operations/services/visita.py",
     ["registrar_visita(jornada, punto, detalles, observaciones, sin_generacion)",
      "omitir_punto(jornada, punto, motivo)", "-validar_capacidad(punto, detalles)"],
     ["RegistroResiduo", "JornadaPunto", "PuntoRecoleccion"]),
    ("EtlService", "analytics/services/etl.py",
     ["iniciar(usuario): EjecucionETL", "ejecutar(ejecucion): EjecucionETL",
      "extraer(): DataFrame", "transformar(df): DataFrame", "cargar(df, ejecucion): int"],
     ["EjecucionETL", "HechoResiduo", "RegistroDescartado", "RegistroResiduo"]),
    ("IndicadoresService", "analytics/services/indicadores.py",
     ["indicadores(user, alcance): dict", "comparar(user, base, comp): dict",
      "puntos_criticos(user, alcance): list", "tendencia_creciente(user, base, comp): set",
      "mapa(user, alcance): dict"],
     ["HechoResiduo", "ParametrosSistema"]),
    ("ReporteService", "analytics/services/reportes.py",
     ["generar(tipo, user, alcance): Reporte", "a_excel(reporte, alcance): bytes",
      "a_pdf(reporte, alcance): bytes"],
     ["HechoResiduo", "Jornada", "Incidencia", "Prediccion"]),
    ("EntrenamientoService", "prediction/services/entrenamiento.py",
     ["iniciar(usuario, hiperparametros): ModeloEntrenado", "entrenar(modelo): ModeloEntrenado",
      "publicar(modelo): ModeloEntrenado", "vigente(): ModeloEntrenado", "cargar(pk)"],
     ["ModeloEntrenado", "HechoResiduo", "ParametrosSistema"]),
    ("PrediccionService", "prediction/services/prediccion.py",
     ["generar(horizonte, sector, punto): LotePrediccion", "resumen(lote, user): dict",
      "mapa(user, sector): dict"],
     ["LotePrediccion", "Prediccion", "ModeloEntrenado"]),
    ("RecomendacionService", "prediction/services/recomendaciones.py",
     ["evaluar(lote, preds): list", "resolver(rec, aceptar, motivo): Recomendacion",
      "-incorporar(rec): Jornada"],
     ["Recomendacion", "Jornada", "Contenedor"]),
    ("BitacoraService", "audit/services/bitacora.py",
     ["registrar(request, operacion, instancia, antes, despues)", "snapshot(instancia): dict"],
     ["AuditLog"]),
]

# relaciones todo-parte: (parte, todo, composicion?)
TODO_PARTE = [("JornadaPunto", "Jornada", True), ("Prediccion", "LotePrediccion", True),
              ("RegistroResiduo", "Jornada", False), ("HechoResiduo", "EjecucionETL", False),
              ("RegistroDescartado", "EjecucionETL", False),
              ("Recomendacion", "LotePrediccion", False), ("Contenedor", "PuntoRecoleccion", False),
              ("PuntoRecoleccion", "Sector", False)]

# ----------------------------------------------------------------------
# 7.4 diagramas de secuencia de los casos de uso principales
# (origen, destino, mensaje, es_retorno); los nombres coinciden con cap. 6/7.2
# ----------------------------------------------------------------------
SECUENCIAS = {
    1: ("Supervisor de Recolección", ["LoginView", "AuthController", "User", "BitacoraService"], [
        ("Supervisor de Recolección", "LoginView", "iniciarSesion(usuario, clave)", 0),
        ("LoginView", "AuthController", "POST /api/auth/login/", 0),
        ("AuthController", "User", "authenticate(usuario, clave)", 0),
        ("User", "AuthController", "user", 1),
        ("AuthController", "BitacoraService", "registrar(LOGIN, user)", 0),
        ("AuthController", "LoginView", "tokens(access, refresh)", 1),
        ("LoginView", "Supervisor de Recolección", "mostrarMenuSegunRol()", 1),
        ("AuthController", "BitacoraService", "registrar(LOGIN_FALLIDO)", 0),
        ("AuthController", "LoginView", "401 credenciales inválidas", 1),
        ("LoginView", "Supervisor de Recolección", "mostrarError()", 1)]),
    9: ("Personal Operativo de Limpieza",
        ["CampoView", "JornadaController", "VisitaService", "PuntoRecoleccion", "RegistroResiduo", "JornadaPunto"], [
        ("Personal Operativo de Limpieza", "CampoView", "registrarVaciado(tipo, cantidad)", 0),
        ("CampoView", "JornadaController", "POST /jornadas/{id}/visitas/", 0),
        ("JornadaController", "VisitaService", "registrar_visita(jornada, punto, detalles)", 0),
        ("VisitaService", "PuntoRecoleccion", "capacidad()", 0),
        ("PuntoRecoleccion", "VisitaService", "capacidad_kg", 1),
        ("VisitaService", "RegistroResiduo", "create(detalle)", 0),
        ("VisitaService", "JornadaPunto", "marcarVisitado()", 0),
        ("VisitaService", "JornadaController", "registros", 1),
        ("JornadaController", "CampoView", "201 Created", 1),
        ("CampoView", "Personal Operativo de Limpieza", "mostrarSiguientePunto()", 1)]),
    14: ("Supervisor de Recolección",
         ["JornadasView", "JornadaController", "Recomendacion", "Jornada", "JornadaService", "BitacoraService"], [
        ("Supervisor de Recolección", "JornadasView", "nuevaJornada(fecha, turno, sector)", 0),
        ("JornadasView", "JornadaController", "GET puntos propuestos", 0),
        ("JornadaController", "Recomendacion", "aceptadas(sector)", 0),
        ("Recomendacion", "JornadaController", "puntos priorizados", 1),
        ("JornadaController", "JornadasView", "ruta propuesta", 1),
        ("Supervisor de Recolección", "JornadasView", "guardar(ruta, personal, vehículos)", 0),
        ("JornadasView", "JornadaController", "POST /jornadas/", 0),
        ("JornadaController", "Jornada", "create(dto, ruta)", 0),
        ("JornadaController", "JornadaService", "asignar(jornada, personal, vehiculos, responsable)", 0),
        ("JornadaController", "JornadaService", "confirmar(jornada)", 0),
        ("JornadaService", "BitacoraService", "registrar(MODIFICACION)", 0),
        ("JornadaController", "JornadasView", "jornada CONFIRMADA", 1)]),
    18: ("Supervisor de Recolección",
         ["JornadasView", "JornadaController", "JornadaService", "Jornada", "BitacoraService"], [
        ("Supervisor de Recolección", "JornadasView", "verResumen(jornada)", 0),
        ("JornadasView", "JornadaController", "GET /jornadas/{id}/resumen/", 0),
        ("JornadaController", "JornadaService", "resumen(jornada)", 0),
        ("JornadaService", "JornadaController", "totales y cobertura", 1),
        ("JornadaController", "JornadasView", "resumen", 1),
        ("Supervisor de Recolección", "JornadasView", "cerrar(observaciones)", 0),
        ("JornadasView", "JornadaController", "POST /jornadas/{id}/cerrar/", 0),
        ("JornadaController", "JornadaService", "cerrar(jornada, observaciones)", 0),
        ("JornadaService", "Jornada", "setEstado(CERRADA)", 0),
        ("JornadaService", "BitacoraService", "registrar(CIERRE)", 0),
        ("JornadaController", "JornadasView", "jornada CERRADA", 1)]),
    20: ("Administrador del Sistema",
         ["EtlView", "EtlController", "EtlService", "RegistroResiduo", "HechoResiduo", "EjecucionETL"], [
        ("Administrador del Sistema", "EtlView", "ejecutarETL()", 0),
        ("EtlView", "EtlController", "POST /etl/ejecutar/", 0),
        ("EtlController", "EtlService", "iniciar(usuario)", 0),
        ("EtlService", "EjecucionETL", "create(EN_CURSO)", 0),
        ("EtlController", "EtlView", "202 Accepted (en segundo plano)", 1),
        ("EtlService", "RegistroResiduo", "extraer() pendientes", 0),
        ("RegistroResiduo", "EtlService", "DataFrame", 1),
        ("EtlService", "EtlService", "transformar(df): duplicados, kg, periodo, atípicos", 0),
        ("EtlService", "HechoResiduo", "cargar(df)", 0),
        ("EtlService", "EjecucionETL", "finalizar(procesados, aceptados, observados)", 0)]),
    26: ("Administrador del Sistema",
         ["ModeloView", "ModeloController", "EntrenamientoService", "HechoResiduo", "ModeloEntrenado"], [
        ("Administrador del Sistema", "ModeloView", "entrenar(hiperparámetros)", 0),
        ("ModeloView", "ModeloController", "POST /modelos/entrenar/", 0),
        ("ModeloController", "EntrenamientoService", "iniciar(usuario, hp)", 0),
        ("EntrenamientoService", "ModeloEntrenado", "create(version, ENTRENANDO)", 0),
        ("ModeloController", "ModeloView", "202 Accepted", 1),
        ("EntrenamientoService", "HechoResiduo", "serie_diaria()", 0),
        ("HechoResiduo", "EntrenamientoService", "observaciones", 1),
        ("EntrenamientoService", "EntrenamientoService", "split cronológico, fit RandomForestRegressor", 0),
        ("EntrenamientoService", "EntrenamientoService", "_evaluar(): MAE, RMSE, R², importancias", 0),
        ("EntrenamientoService", "ModeloEntrenado", "guardar(métricas, artefacto, estado)", 0)]),
    28: ("Supervisor de Recolección",
         ["PrediccionView", "PrediccionController", "PrediccionService", "ModeloEntrenado",
          "LotePrediccion", "RecomendacionService"], [
        ("Supervisor de Recolección", "PrediccionView", "predecir(horizonte, sector)", 0),
        ("PrediccionView", "PrediccionController", "POST /predicciones/", 0),
        ("PrediccionController", "PrediccionService", "generar(horizonte, sector)", 0),
        ("PrediccionService", "ModeloEntrenado", "vigente()", 0),
        ("ModeloEntrenado", "PrediccionService", "pipeline", 1),
        ("PrediccionService", "PrediccionService", "estado_actual() y predict()", 0),
        ("PrediccionService", "LotePrediccion", "create(modelo) + predicciones", 0),
        ("PrediccionService", "RecomendacionService", "evaluar(lote, preds)", 0),
        ("RecomendacionService", "PrediccionService", "recomendaciones", 1),
        ("PrediccionController", "PrediccionView", "lote con margen de error", 1)]),
    30: ("Supervisor de Recolección",
         ["RecomendacionesView", "RecomendacionController", "RecomendacionService",
          "Recomendacion", "Jornada", "BitacoraService"], [
        ("Supervisor de Recolección", "RecomendacionesView", "aceptar(recomendación, motivo)", 0),
        ("RecomendacionesView", "RecomendacionController", "POST /recomendaciones/{id}/aceptar/", 0),
        ("RecomendacionController", "RecomendacionService", "resolver(rec, True, motivo)", 0),
        ("RecomendacionService", "Recomendacion", "setEstado(ACEPTADA)", 0),
        ("RecomendacionService", "Jornada", "próxima PLANIFICADA del sector", 0),
        ("Jornada", "RecomendacionService", "jornada", 1),
        ("RecomendacionService", "Jornada", "priorizar(punto)", 0),
        ("RecomendacionService", "BitacoraService", "registrar(RESOLUCION)", 0),
        ("RecomendacionController", "RecomendacionesView", "recomendación resuelta", 1)]),
}

# fragmentos combinados de cada secuencia: (operador, [(guarda, primer mensaje,
# ultimo mensaje), ...]) con los mensajes numerados desde 1 en SECUENCIAS
FRAGMENTOS = {
    1: [("alt", [("credenciales válidas", 5, 7), ("else", 8, 10)])],
    9: [("loop", [("por cada tipo de residuo", 6, 6)])],
    20: [("opt", [("existen registros pendientes", 8, 9)])],
    28: [("loop", [("por cada punto y fecha del horizonte", 6, 6)])],
    30: [("opt", [("existe una jornada PLANIFICADA del sector", 7, 7)])],
}

# clases de la capa de negocio sin tabla propia del sistema: el token de
# renovacion lo persiste la biblioteca simplejwt (lista negra) y el reporte se
# arma en memoria. (nombre, atributos, metodos, vista, asociacion con User)
CLASES_SIN_TABLA = [
    ("TokenRenovacion", [("jti", "String"), ("token", "String"), ("creado_en", "DateTime"),
                         ("expira_en", "DateTime")],
     ["invalidar(refresh): void", "estaRevocado(): Boolean"], "seguridad",
     ("User", "0..*", "1", "usuario")),
    ("Reporte", [("titulo", "String"), ("columnas", "List<String>"), ("filas", "List<List>"),
                 ("numericas", "Set<Integer>"), ("emitido_en", "DateTime")],
     ["encabezado(alcance): List<String>"],
     "analitica", ("User", "0..*", "1", "solicitado_por")),
]
# servicio -> clases sin tabla que usa
USA_SIN_TABLA = {"ReporteService": ["Reporte"]}
