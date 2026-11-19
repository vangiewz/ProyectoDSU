# -*- coding: utf-8 -*-
"""Diagramas UML de la Fase 1 (cap. 3 y 4) rehechos en Enterprise Architect:
el flujo operativo actual (Figura 11), el modelo de dominio (Figura 12) y los
diagramas de actividad de los RF (Figuras 13-20). Los pasos salen de
figuras.py / requisitos.py, los mismos que generaban las figuras SVG.

Lo invoca ea_modelo.main() con la parte "cap4". insertar.py reemplaza en el
documento cada figura vieja por su version de EA (REEMPLAZOS)."""
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BASE))

import requisitos                      # noqa: E402

DIR = os.path.join(os.path.dirname(BASE), "figuras", "fase1")
# figura vieja (generador/figuras) -> figura de EA (generador/figuras/fase1)
REEMPLAZOS = {"flujo_operativo.png": "flujo_operativo.png",
              "modelo_dominio.png": "modelo_dominio.png"}
REEMPLAZOS.update({requisitos.archivo_diagrama(r["id"]): requisitos.archivo_diagrama(r["id"])
                   for r in requisitos.con_diagrama()})

# los textos de requisitos.py estan sin tildes (los usaba el SVG)
TILDES = {
    "modulo": "módulo", "generacion": "generación", "validacion": "validación",
    "operacion": "operación", "omision": "omisión", "Si": "Sí", "vehiculos": "vehículos",
    "vehiculo": "vehículo", "vacia": "vacía", "continua": "continúa", "area": "área",
    "ejecucion": "ejecución", "atipicos": "atípicos", "analiticas": "analíticas",
    "analitica": "analítica", "analisis": "análisis", "bitacora": "bitácora",
    "informacion": "información", "criticos": "críticos", "critico": "crítico",
    "Que": "Qué", "historicas": "históricas", "metricas": "métricas",
    "categoricas": "categóricas", "cronologico": "cronológico", "version": "versión",
    "recomendacion": "recomendación", "evalua": "evalúa", "decision": "decisión",
    "R2": "R²", "historico": "histórico", "periodico": "periódico", "Observada": "Observada", "periodo": "periodo",
}


def tildes(texto):
    return re.sub(r"[A-Za-z0-9]+", lambda m: TILDES.get(m.group(0), m.group(0)), texto)


def pregunta(texto):
    """'Quedan puntos?' -> '¿Quedan puntos?'"""
    texto = tildes(texto)
    return texto if texto.startswith("¿") else "¿" + texto


# ----------------------------------------------------------------------
# actividad
# ----------------------------------------------------------------------
CARRILES = [("El sistema", "Sistema"), ("El proceso", "Sistema"),
            ("El operario", "Personal Operativo de Limpieza"),
            ("La cuadrilla", "Personal Operativo de Limpieza"),
            ("El supervisor", "Supervisor de Recolección"),
            ("El usuario", "Usuario"), ("El administrador", "Administrador del Sistema")]

# bucles: (diagrama, texto de la decision) -> (rama que vuelve, accion destino)
LAZOS = {
    ("flujo_operativo.png", "Quedan puntos por recorrer?"):
        ("Si", "La cuadrilla se desplaza al siguiente punto del recorrido"),
    ("rf12_actividad.png", "Quedan puntos pendientes en la ruta?"):
        ("Si", "El sistema presenta el siguiente punto de la ruta"),
    ("rf8_actividad.png", "La validacion es correcta?"):
        ("No", "El sistema valida la cantidad y la coherencia del registro"),
}

# ramas que cortan el proceso (sin datos, sin modelo): terminan en un nodo
# final propio en lugar de volver al flujo principal
TERMINA = {
    ("rf15_actividad.png", "Existen registros nuevos por procesar?"): "No",
    ("rf16_actividad.png", "Existe informacion para el periodo?"): "No",
    ("rf20_actividad.png", "Existen datos para el alcance definido?"): "No",
    ("rf22_actividad.png", "El volumen de registros es suficiente?"): "No",
    ("rf23_actividad.png", "Existe un modelo publicado vigente?"): "No",
}

NODO_W, NODO_H, FILA = 190, 56, 92
CARRIL_W = 2 * NODO_W + 70


def carril(texto):
    for prefijo, nombre in CARRILES:
        if texto.startswith(prefijo):
            return nombre
    raise ValueError("sin carril: " + texto)


def _plan(archivo, pasos):
    """Convierte los pasos en nodos con fila y carril, y en flujos.
    nodo: dict(id, tipo, texto, carril, fila, rama); flujo: (a, b, guarda)."""
    destinos = {v[1] for k, v in LAZOS.items() if k[0] == archivo}
    nodos, flujos = [], []
    fila = [0]

    def nuevo(tipo, texto="", car=None, rama=0, avanza=True, dec=None):
        n = {"id": len(nodos), "tipo": tipo, "texto": texto, "carril": car,
             "fila": fila[0], "rama": rama, "dec": dec}
        nodos.append(n)
        if avanza:
            fila[0] += 1
        return n

    previo = None
    pendientes = []                      # (nodo, guarda) que entran al siguiente
    por_texto = {}

    def enlazar(n):
        for p, g in pendientes:
            flujos.append((p["id"], n["id"], g))
        pendientes.clear()

    for paso in pasos:
        if paso[0] in ("inicio", "fin"):
            car = previo["carril"] if previo else None
            n = nuevo(paso[0], car=car)
            enlazar(n)
            pendientes.append((n, ""))
            previo = n
            continue
        if paso[0] == "accion":
            if paso[1] in destinos:      # entrada de un bucle: nodo de fusion
                mg = nuevo("merge", car=carril(paso[1]))
                mg["lazo"] = True
                enlazar(mg)
                pendientes.append((mg, ""))
                por_texto["merge:" + paso[1]] = mg
            n = nuevo("accion", tildes(paso[1]), carril(paso[1]))
            por_texto[paso[1]] = n
            enlazar(n)
            pendientes.append((n, ""))
            previo = n
            continue
        _, texto, g1, r1, g2, r2 = paso
        d = nuevo("decision", pregunta(texto), previo["carril"])
        enlazar(d)
        lazo = LAZOS.get((archivo, texto))
        inicio = fila[0]
        salidas = []
        largos = [len(r1), len(r2)]
        for k, (g, acciones) in enumerate(((g1, r1), (g2, r2))):
            fila[0] = inicio
            ant, guarda = d, tildes(g)
            for a in acciones:
                n = nuevo("accion", tildes(a), carril(a), rama=k + 1, dec=d["id"])
                flujos.append((ant["id"], n["id"], guarda))
                ant, guarda = n, ""
            if lazo and g == lazo[0]:
                flujos.append((ant["id"], por_texto["merge:" + lazo[1]]["id"], guarda))
            elif TERMINA.get((archivo, texto)) == g:
                fin = nuevo("fin", car=ant["carril"], rama=k + 1, dec=d["id"])
                flujos.append((ant["id"], fin["id"], guarda))
                largos[k] += 1
            else:
                salidas.append((ant, guarda))
        fila[0] = inicio + max(largos)
        if len(salidas) == 2:
            mg = nuevo("merge", car=d["carril"])
            for ant, guarda in salidas:
                flujos.append((ant["id"], mg["id"], guarda))
            pendientes.append((mg, ""))
            previo = mg
        else:
            pendientes.extend(salidas)
            previo = salidas[0][0]
    return nodos, flujos


def actividad(m, p, archivo, titulo, pasos, ruta_png):
    nodos, flujos = _plan(archivo, pasos)
    carriles = list(dict.fromkeys(n["carril"] for n in nodos if n["carril"]))
    for n in nodos:
        n["carril"] = n["carril"] or carriles[0]
    d = m.diagrama(p, titulo, "Activity")
    for nombre in carriles:
        d.SwimlaneDef.Swimlanes.Add(nombre, CARRIL_W)
    d.Update()

    # x: centro del carril; una rama se corre a su lado (1 izquierda, 2 derecha)
    # solo si la otra rama de la misma decision usa tambien ese carril
    centro = {c: 20 + i * CARRIL_W + CARRIL_W // 2 for i, c in enumerate(carriles)}
    izq_carril = {c: 20 + i * CARRIL_W for i, c in enumerate(carriles)}
    for n in nodos:
        n["x"], n["y"] = centro[n["carril"]], 70 + n["fila"] * FILA
        if n["rama"] and any(o["dec"] == n["dec"] and o["rama"] != n["rama"] and
                             o["carril"] == n["carril"] for o in nodos):
            n["x"] += (-1 if n["rama"] == 1 else 1) * (CARRIL_W // 4)

    tipos = {"inicio": ("StateNode", 100, 30, 30), "fin": ("StateNode", 101, 30, 30),
             "accion": ("Action", None, NODO_W, NODO_H),
             "decision": ("Decision", None, 40, 40), "merge": ("MergeNode", None, 40, 40)}
    el = {}
    for n in nodos:
        tipo, sub, w, h = tipos[n["tipo"]]
        e = p.Elements.AddNew(n["texto"], tipo)
        if sub is not None:
            e.Subtype = sub
        e.Update()
        el[n["id"]] = e
        m.colocar(d, e, n["x"] - w // 2, n["y"] - h // 2, w, h)
    p.Elements.Refresh()
    for a, b, guarda in flujos:
        na, nb = nodos[a], nodos[b]
        c = el[a].Connectors.AddNew("", "ControlFlow")
        c.SupplierID = el[b].ElementID
        if guarda:
            c.TransitionGuard = guarda
        c.Update()
        if nb["fila"] <= na["fila"]:
            # vuelta del bucle: sale por la izquierda, sube por dentro del
            # carril y entra a la fusion por el costado
            cx = max(izq_carril[na["carril"]] + 16, na["x"] - NODO_W // 2 - 35)
            m.quebrar(d, c, [(cx, na["y"]), (cx, nb["y"])])
        elif nb.get("lazo") and na["x"] != nb["x"]:
            # entrada normal a la fusion de un bucle: por arriba (el costado
            # queda para la vuelta)
            ym = nb["y"] - FILA // 2
            m.quebrar(d, c, [(na["x"], ym), (nb["x"], ym)])
        elif na["x"] != nb["x"]:
            # salida de una decision: horizontal y baja; llegada a una fusion:
            # baja y horizontal; entre acciones de carriles distintos: igual
            if nb["tipo"] == "merge":
                m.quebrar(d, c, [(na["x"], nb["y"])])
            elif na["tipo"] == "decision":
                m.quebrar(d, c, [(nb["x"], na["y"])])
            else:
                # baja hasta el hueco entre filas y recien ahi cruza de carril
                ym = (na["y"] + nb["y"]) // 2 if nb["fila"] - na["fila"] == 1 else                     nb["y"] - FILA // 2
                m.quebrar(d, c, [(na["x"], ym), (nb["x"], ym)])
    m.exportar(d, ruta_png)


# ----------------------------------------------------------------------
# modelo de dominio
# ----------------------------------------------------------------------
DOMINIO = {
    "Rol": [("nombre", "String"), ("permisos", "String")],
    "Usuario": [("nombre", "String"), ("correo", "String"), ("estado", "String")],
    "Bitacora": [("fecha", "DateTime"), ("operacion", "String"), ("entidad", "String")],
    "PeriodoAcademico": [("nombre", "String"), ("inicio", "Date"), ("fin", "Date")],
    "Jornada": [("fecha", "Date"), ("turno", "String"), ("estado", "String")],
    "RegistroResiduo": [("cantidad", "Decimal"), ("fecha", "Date"), ("hora", "Time")],
    "TipoResiduo": [("nombre", "String"), ("clasificacion", "String")],
    "UnidadMedida": [("nombre", "String"), ("factor", "Decimal")],
    "Sector": [("codigo", "String"), ("nombre", "String")],
    "PuntoRecoleccion": [("codigo", "String"), ("latitud", "Decimal"),
                         ("longitud", "Decimal"), ("capacidad", "Decimal")],
    "Contenedor": [("tipo", "String"), ("capacidad", "Decimal"), ("estado", "String")],
    "Incidencia": [("tipo", "String"), ("gravedad", "String"), ("estado", "String")],
    "Recomendacion": [("accion", "String"), ("estado", "String")],
    "Prediccion": [("fecha", "Date"), ("cantidad", "Decimal"), ("error", "Decimal")],
    "ModeloEntrenado": [("version", "String"), ("metricas", "String")],
}
# (A, B, nombre, multiplicidad en A, multiplicidad en B, agregacion en A)
# se lee "A nombre B"; agregacion: 1 = A agrega a B, 2 = A se compone de B
ASOCIACIONES = [
    ("Rol", "Usuario", "define", "1", "0..*", 0),
    ("Usuario", "Bitacora", "genera", "1", "0..*", 0),
    ("Usuario", "Jornada", "ejecuta", "1..*", "0..*", 0),
    ("Jornada", "RegistroResiduo", "contiene", "1", "0..*", 2),
    ("TipoResiduo", "RegistroResiduo", "clasifica", "1", "0..*", 0),
    ("TipoResiduo", "UnidadMedida", "se mide en", "0..*", "1", 0),
    ("RegistroResiduo", "PuntoRecoleccion", "se origina en", "0..*", "1", 0),
    ("RegistroResiduo", "PeriodoAcademico", "pertenece a", "0..*", "1", 0),
    ("Sector", "PuntoRecoleccion", "agrupa", "1", "1..*", 1),
    ("PuntoRecoleccion", "Contenedor", "posee", "1", "0..*", 1),
    ("PuntoRecoleccion", "Incidencia", "reporta", "1", "0..*", 0),
    ("PuntoRecoleccion", "Prediccion", "se proyecta en", "1", "0..*", 0),
    ("ModeloEntrenado", "Prediccion", "produce", "1", "0..*", 0),
    ("Recomendacion", "Prediccion", "se basa en", "0..*", "1", 0),
    ("Recomendacion", "Jornada", "ajusta", "0..*", "0..1", 0),
]
# grilla (columna, fila) pensada para que las lineas no se crucen
GRILLA_DOMINIO = {
    "Rol": (0, 0), "Usuario": (1, 0), "Bitacora": (2, 0),
    "Recomendacion": (0, 1), "Jornada": (1, 1), "PeriodoAcademico": (3, 1),
    "Prediccion": (0, 2), "RegistroResiduo": (1, 2), "TipoResiduo": (2, 2),
    "UnidadMedida": (3, 2),
    "ModeloEntrenado": (0, 3), "PuntoRecoleccion": (1, 3), "Sector": (2, 3),
    "Incidencia": (1, 4), "Contenedor": (2, 4),
}


def dominio(m, p, ruta_png):
    d = m.diagrama(p, "Modelo de dominio", "Logical")
    el = {}
    for nombre, atributos in DOMINIO.items():
        e = m.elemento(p, nombre, "Class")
        for a, t in atributos:
            at = e.Attributes.AddNew(a, t)
            at.Visibility = "Private"
            at.Update()
        el[nombre] = e
        c, f = GRILLA_DOMINIO[nombre]
        m.colocar(d, e, 40 + c * 330, 40 + f * 190, 200, 40 + 16 * len(atributos))
    for a, b, nombre, ma, mb, agr in ASOCIACIONES:
        con = m.conectar(el[a], el[b], "Association", nombre=nombre,
                         card_origen=ma, card_destino=mb, dirigido=False)
        if agr:
            con.ClientEnd.Aggregation = agr
            con.Update()
    m.exportar(d, ruta_png)


def cap4(m):
    os.makedirs(DIR, exist_ok=True)
    p = m.paquete("Fase 1 (cap. 3 y 4)")
    dominio(m, p, os.path.join(DIR, "modelo_dominio.png"))
    actividad(m, m.paquete("Flujo operativo actual", p), "flujo_operativo.png",
              "Flujo operativo actual", PASOS_FLUJO, os.path.join(DIR, "flujo_operativo.png"))
    for r in requisitos.con_diagrama():
        archivo = requisitos.archivo_diagrama(r["id"])
        actividad(m, m.paquete("Actividad %s" % r["id"], p), archivo,
                  "%s. %s" % (r["id"], r["nombre"]), r["pasos"], os.path.join(DIR, archivo))


# los mismos pasos de figuras.flujo_operativo()
PASOS_FLUJO = [
    ("inicio",),
    ("accion", "El supervisor define los sectores a atender en la jornada"),
    ("accion", "El supervisor asigna las cuadrillas y los vehiculos"),
    ("accion", "La cuadrilla se desplaza al siguiente punto del recorrido"),
    ("accion", "El operario verifica visualmente el estado del contenedor"),
    ("decision", "El contenedor requiere vaciado?",
     "No", ["La cuadrilla continua el recorrido"],
     "Si", ["El operario vacia el contenedor",
            "El operario carga los residuos en el vehiculo"]),
    ("decision", "Quedan puntos por recorrer?",
     "Si", ["La cuadrilla avanza al siguiente punto"],
     "No", ["La cuadrilla traslada los residuos al area de acopio"]),
    ("accion", "El supervisor consolida manualmente el reporte de la jornada"),
    ("fin",),
]
