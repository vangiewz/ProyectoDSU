"""Caja blanca sobre diagramas de secuencia (Software 2, clase del 17/11/2026).

Tres CU con complejidad >= 3. Cada validación del servicio es un fragmento «break» (si la guarda se
cumple, se envía el rechazo y termina la interacción) y cada filtro opcional un «opt». Del diagrama se
deriva el grafo de flujo: un nodo por bloque de mensajes o decisión, un nodo común de rechazo y el fin.
V(G) se calcula de tres formas (aristas - nodos + 2, predicados + 1 y matriz de conexiones) y cada
camino básico se enlaza con la prueba automatizada que lo recorre.
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JUNIT = ROOT / 'docs/auditoria-fase-final/pruebas_ci/pytest.xml'

OP, SUP = 'Personal Operativo de Limpieza', 'Supervisor de Recolección'
R = 1  # mensaje de retorno

SPECS = [
 dict(cu=9, nombre='Registrar vaciado de residuos', actor=OP, rf='RF8',
      servicio='operations/services/visita.py · registrar_visita',
      vidas=['CampoView', 'JornadaController', 'VisitaService', 'Jornada', 'JornadaPunto', 'PuntoRecoleccion', 'RegistroResiduo', 'BitacoraService'],
      mensajes=[
        (OP, 'CampoView', 'registrarVaciado(punto, detalles)', 0),
        ('CampoView', 'JornadaController', 'POST /jornadas/{id}/visitas/', 0),
        ('JornadaController', 'VisitaService', 'registrar_visita(jornada, punto, detalles)', 0),
        ('VisitaService', 'Jornada', 'personal.incluye(usuario)', 0),
        ('VisitaService', 'JornadaController', '403 no forma parte del personal', R),
        ('VisitaService', 'Jornada', 'estado()', 0),
        ('VisitaService', 'JornadaController', '400 la jornada no está en ejecución', R),
        ('VisitaService', 'JornadaPunto', 'parada(punto) con bloqueo', 0),
        ('VisitaService', 'JornadaController', '400 el punto no pertenece a la ruta', R),
        ('VisitaService', 'JornadaController', '400 visita sin generación con detalle', R),
        ('VisitaService', 'JornadaController', '400 falta el detalle de residuos', R),
        ('VisitaService', 'PuntoRecoleccion', 'capacidad_kg y capacidad en litros', 0),
        ('VisitaService', 'JornadaController', '400 excede la capacidad en kg', R),
        ('VisitaService', 'JornadaController', '400 excede la capacidad en litros', R),
        ('VisitaService', 'RegistroResiduo', 'bulk_create(detalles)', 0),
        ('VisitaService', 'JornadaPunto', 'marcarAtendida(ahora)', 0),
        ('VisitaService', 'BitacoraService', 'registrar(CREAR, visita)', 0),
        ('VisitaService', 'JornadaController', 'registros', R),
        ('JornadaController', 'CampoView', '201 Created', R),
        ('CampoView', OP, 'mostrarSiguientePunto()', R)],
      fragmentos=[('break', [('operario no asignado a la jornada', 5, 5)]),
                  ('break', [('estado distinto de EN_EJECUCION', 7, 7)]),
                  ('break', [('punto fuera de la ruta', 9, 9)]),
                  ('break', [('sin generación y con detalle', 10, 10)]),
                  ('break', [('con generación y sin detalle', 11, 11)]),
                  ('break', [('kg > capacidad x tolerancia', 13, 13)]),
                  ('break', [('litros > capacidad x tolerancia', 14, 14)])],
      nodos=[(1, 'Solicitud y personal asignado', '1–4'), (2, '¿Operario no asignado?', '5'),
             (3, '¿Jornada no está en ejecución?', '6–7'), (4, '¿Punto fuera de la ruta?', '8–9'),
             (5, '¿Sin generación con detalle?', '10'), (6, '¿Sin detalle de residuos?', '11'),
             (7, '¿Excede la capacidad en kg?', '12–13'), (8, '¿Excede la capacidad en litros?', '14'),
             (9, 'Registrar, marcar parada y auditar', '15–19'), (10, 'Rechazo y mensaje al operario', '5, 7, 9, 10, 11, 13, 14'),
             (11, 'Fin', '20')],
      aristas=[(1, 2, ''), (2, 10, 'sí'), (2, 3, 'no'), (3, 10, 'sí'), (3, 4, 'no'), (4, 10, 'sí'), (4, 5, 'no'),
               (5, 10, 'sí'), (5, 6, 'no'), (6, 10, 'sí'), (6, 7, 'no'), (7, 10, 'sí'), (7, 8, 'no'),
               (8, 10, 'sí'), (8, 9, 'no'), (9, 11, ''), (10, 11, '')],
      caminos=[('1-2-10-11', 'Operario fuera de la cuadrilla', '403; sin registros', 'test_caminos_registro[no_asignado]'),
               ('1-2-3-10-11', 'Jornada PLANIFICADA', '400; sin registros', 'test_caminos_registro[estado]'),
               ('1-2-3-4-10-11', 'Punto que no está en la ruta', '400; sin registros', 'test_caminos_registro[fuera_ruta]'),
               ('1-2-3-4-5-10-11', 'Sin generación con un detalle', '400; sin registros', 'test_caminos_registro[sin_generacion_con_detalle]'),
               ('1-2-3-4-5-6-10-11', 'Vaciado sin detalle', '400; sin registros', 'test_caminos_registro[sin_detalle]'),
               ('1-2-3-4-5-6-7-10-11', '151 kg en un punto de 100 kg', '400; sin registros', 'test_caminos_registro[excede_kg]'),
               ('1-2-3-4-5-6-7-8-10-11', '301 L en un punto de 200 L', '400; sin registros', 'test_caminos_registro[excede_litros]'),
               ('1-2-3-4-5-6-7-8-9-11', '35,5 kg de orgánico en P1', '201; registro y parada atendida', 'test_caminos_registro[valido]')]),
 dict(cu=15, nombre='Asignar personal y vehículos a la jornada', actor=SUP, rf='RF13',
      servicio='operations/services/jornada.py · asignar',
      vidas=['JornadasView', 'JornadaController', 'JornadaService', 'Jornada', 'User', 'Vehiculo', 'BitacoraService'],
      mensajes=[
        (SUP, 'JornadasView', 'asignar(personal, vehículos, responsable)', 0),
        ('JornadasView', 'JornadaController', 'POST /jornadas/{id}/asignar/', 0),
        ('JornadaController', 'JornadaService', 'asignar(jornada, personal, vehiculos, responsable)', 0),
        ('JornadaService', 'Jornada', 'estado()', 0),
        ('JornadaService', 'JornadaController', '400 el estado no admite asignación', R),
        ('JornadaService', 'JornadaController', '400 falta el responsable', R),
        ('JornadaService', 'JornadaController', '400 responsable fuera del personal', R),
        ('JornadaService', 'User', 'is_active y roles', 0),
        ('JornadaService', 'JornadaController', '400 personal no operativo o inactivo', R),
        ('JornadaService', 'Vehiculo', 'estado e is_active', 0),
        ('JornadaService', 'JornadaController', '400 vehículo fuera de servicio', R),
        ('JornadaService', 'Jornada', 'asignaciones del mismo turno', 0),
        ('JornadaService', 'JornadaController', '400 personal ya asignado en el turno', R),
        ('JornadaService', 'JornadaController', '400 vehículo ya asignado en el turno', R),
        ('JornadaService', 'Jornada', 'set(personal, vehículos, responsable)', 0),
        ('JornadaService', 'BitacoraService', 'registrar(ACTUALIZAR, asignación)', 0),
        ('JornadaService', 'JornadaController', 'jornada', R),
        ('JornadaController', 'JornadasView', '200 asignación registrada', R),
        ('JornadasView', SUP, 'mostrarCuadrilla()', R)],
      fragmentos=[('break', [('estado no es PLANIFICADA ni CONFIRMADA', 5, 5)]),
                  ('break', [('responsable ausente', 6, 6)]),
                  ('break', [('responsable fuera del personal', 7, 7)]),
                  ('break', [('personal no operativo o inactivo', 9, 9)]),
                  ('break', [('vehículo fuera de servicio', 11, 11)]),
                  ('break', [('personal ocupado en el turno', 13, 13)]),
                  ('break', [('vehículo ocupado en el turno', 14, 14)])],
      nodos=[(1, 'Solicitud y estado de la jornada', '1–4'), (2, '¿Estado no admite asignación?', '5'),
             (3, '¿Responsable ausente?', '6'), (4, '¿Responsable fuera del personal?', '7'),
             (5, '¿Personal no operativo o inactivo?', '8–9'), (6, '¿Vehículo fuera de servicio?', '10–11'),
             (7, '¿Personal ocupado en el turno?', '12–13'), (8, '¿Vehículo ocupado en el turno?', '14'),
             (9, 'Persistir asignación y auditar', '15–18'), (10, 'Rechazo y mensaje al supervisor', '5, 6, 7, 9, 11, 13, 14'),
             (11, 'Fin', '19')],
      aristas=[(1, 2, ''), (2, 10, 'sí'), (2, 3, 'no'), (3, 10, 'sí'), (3, 4, 'no'), (4, 10, 'sí'), (4, 5, 'no'),
               (5, 10, 'sí'), (5, 6, 'no'), (6, 10, 'sí'), (6, 7, 'no'), (7, 10, 'sí'), (7, 8, 'no'),
               (8, 10, 'sí'), (8, 9, 'no'), (9, 11, ''), (10, 11, '')],
      caminos=[('1-2-10-11', 'Jornada CERRADA', '400; asignación intacta', 'test_caminos_asignacion[estado]'),
               ('1-2-3-10-11', 'Sin responsable', '400; asignación intacta', 'test_caminos_asignacion[sin_responsable]'),
               ('1-2-3-4-10-11', 'Responsable que no está en el personal', '400; asignación intacta', 'test_caminos_asignacion[fuera_personal]'),
               ('1-2-3-4-5-10-11', 'Operario inactivo', '400; asignación intacta', 'test_caminos_asignacion[inactivo]'),
               ('1-2-3-4-5-6-10-11', 'Vehículo fuera de servicio', '400; asignación intacta', 'test_caminos_asignacion[vehiculo_fuera]'),
               ('1-2-3-4-5-6-7-10-11', 'Operario en otra jornada del turno', '400; asignación intacta', 'test_caminos_asignacion[personal_ocupado]'),
               ('1-2-3-4-5-6-7-8-10-11', 'Vehículo en otra jornada del turno', '400; asignación intacta', 'test_caminos_asignacion[vehiculo_ocupado]'),
               ('1-2-3-4-5-6-7-8-9-11', 'Cuadrilla, vehículo y responsable válidos', '200; asignación persistida y auditada', 'test_caminos_asignacion[valido]')]),
 dict(cu=28, nombre='Predecir generación futura y emitir alertas', actor=SUP, rf='RF23, RF24',
      servicio='prediction/services/prediccion.py · generar',
      vidas=['PrediccionView', 'PrediccionController', 'PrediccionService', 'ParametrosSistema', 'ModeloEntrenado', 'PuntoRecoleccion', 'HechoResiduo', 'LotePrediccion', 'RecomendacionService'],
      mensajes=[
        (SUP, 'PrediccionView', 'predecir(horizonte, sector, punto)', 0),
        ('PrediccionView', 'PrediccionController', 'POST /predicciones/', 0),
        ('PrediccionController', 'PrediccionService', 'generar(horizonte, sector, punto)', 0),
        ('PrediccionService', 'ParametrosSistema', 'horizonte_max_dias', 0),
        ('PrediccionService', 'PrediccionController', '400 horizonte fuera de rango', R),
        ('PrediccionService', 'ModeloEntrenado', 'vigente()', 0),
        ('PrediccionService', 'PrediccionController', '400 no hay modelo publicado', R),
        ('PrediccionService', 'PrediccionController', '403 sector fuera de su alcance', R),
        ('PrediccionService', 'PuntoRecoleccion', 'filter(sector)', 0),
        ('PrediccionService', 'PuntoRecoleccion', 'filter(pk = punto)', 0),
        ('PrediccionService', 'PrediccionController', '400 sin puntos activos', R),
        ('PrediccionService', 'HechoResiduo', 'estado_actual(hoy, puntos)', 0),
        ('PrediccionService', 'PrediccionController', '400 sin historial reciente', R),
        ('PrediccionService', 'HechoResiduo', 'dias_habituales(hoy, puntos)', 0),
        ('PrediccionService', 'PrediccionController', '400 sin días de recolección', R),
        ('PrediccionService', 'ModeloEntrenado', 'cargar().predict(filas)', 0),
        ('PrediccionService', 'LotePrediccion', 'create(modelo) y predicciones con margen', 0),
        ('PrediccionService', 'RecomendacionService', 'evaluar(lote)', 0),
        ('PrediccionService', 'PrediccionController', 'lote', R),
        ('PrediccionController', 'PrediccionView', '201 lote con margen de error', R),
        ('PrediccionView', SUP, 'mostrarPrediccion()', R)],
      fragmentos=[('break', [('horizonte fuera de 1..máximo', 5, 5)]),
                  ('break', [('sin modelo publicado', 7, 7)]),
                  ('break', [('alcance sin permiso territorial', 8, 8)]),
                  ('opt', [('se indicó un sector', 9, 9)]),
                  ('opt', [('se indicó un punto', 10, 10)]),
                  ('break', [('ningún punto activo', 11, 11)]),
                  ('break', [('historial vacío', 13, 13)]),
                  ('break', [('ninguna fecha de recolección', 15, 15)])],
      nodos=[(1, 'Solicitud y horizonte máximo', '1–4'), (2, '¿Horizonte fuera de rango?', '5'),
             (3, '¿Sin modelo publicado?', '6–7'), (4, '¿Alcance sin permiso?', '8'),
             (5, '¿Se indicó sector?', 'guarda opt'), (6, 'Filtrar por sector', '9'),
             (7, '¿Se indicó punto?', 'guarda opt'), (8, 'Filtrar por punto', '10'),
             (9, '¿Sin puntos activos?', '11'), (10, '¿Sin historial reciente?', '12–13'),
             (11, '¿Sin días de recolección?', '14–15'), (12, 'Inferir, guardar lote y evaluar alertas', '16–20'),
             (13, 'Rechazo y mensaje al supervisor', '5, 7, 8, 11, 13, 15'), (14, 'Fin', '21')],
      aristas=[(1, 2, ''), (2, 13, 'sí'), (2, 3, 'no'), (3, 13, 'sí'), (3, 4, 'no'), (4, 13, 'sí'), (4, 5, 'no'),
               (5, 6, 'sí'), (5, 7, 'no'), (6, 7, ''), (7, 8, 'sí'), (7, 9, 'no'), (8, 9, ''),
               (9, 13, 'sí'), (9, 10, 'no'), (10, 13, 'sí'), (10, 11, 'no'), (11, 13, 'sí'), (11, 12, 'no'),
               (12, 14, ''), (13, 14, '')],
      caminos=[('1-2-13-14', 'Horizonte 0 y 999 días', '400; sin lote', 'test_rechazos_prediccion[horizonte_cero]'),
               ('1-2-3-13-14', 'Sin modelo entrenado', '400; sin lote', 'test_entrena_publica_predice_y_revierte'),
               ('1-2-3-4-13-14', 'Supervisor de otro sector', '403; sin lote', 'test_rechazos_prediccion[sector_ajeno]'),
               ('1-2-3-4-5-7-9-13-14', 'Todos los puntos inactivos', '400; sin lote', 'test_rechazos_prediccion[sin_puntos]'),
               ('1-2-3-4-5-7-9-10-13-14', 'Puntos sin historial', '400; sin lote', 'test_rechazos_prediccion[sin_historia]'),
               ('1-2-3-4-5-7-9-10-11-13-14', 'Sin días habituales en el horizonte', '400; sin lote', 'test_rechazos_prediccion[sin_dias]'),
               ('1-2-3-4-5-7-9-10-11-12-14', 'Horizonte 7 sin filtros', '201; lote con margen', 'test_alerta_de_desborde_se_resuelve_y_entra_en_la_jornada'),
               ('1-2-3-4-5-6-7-9-10-11-12-14', 'Horizonte 7 con sector', '201; lote del sector', 'test_prediccion_con_filtros[sector]'),
               ('1-2-3-4-5-7-8-9-10-11-12-14', 'Horizonte 7 con punto', '201; lote del punto', 'test_prediccion_con_filtros[punto]')]),
]


def junit():
    if not JUNIT.exists():
        return {}
    out = {}
    for tc in ET.parse(JUNIT).getroot().iter('testcase'):
        fallo = any(ch.tag in ('failure', 'error', 'skipped') for ch in tc)
        out[tc.get('name')] = 'Fallido' if fallo else 'Aprobado'
    return out


def calcular(spec):
    nodos = [n for n, _, _ in spec['nodos']]
    N, E = len(nodos), len(spec['aristas'])
    sal = {n: [b for a, b, _ in spec['aristas'] if a == n] for n in nodos}
    predicados = [n for n in nodos if len(sal[n]) == 2]
    matriz = [[1 if b in sal[a] else 0 for b in nodos] for a in nodos]
    suma_matriz = sum(max(sum(f) - 1, 0) for f in matriz) + 1
    V = E - N + 2
    assert V == len(predicados) + 1 == suma_matriz, spec['cu']
    estados = junit()
    caminos = []
    for i, (c, entrada, salida, test) in enumerate(spec['caminos'], 1):
        seq = [int(x) for x in c.split('-')]
        assert all(b in sal[a] for a, b in zip(seq, seq[1:])), (spec['cu'], c)
        caminos.append(dict(n=i, camino=c.replace('-', '–'), entrada=entrada, salida=salida, prueba=test, resultado=estados.get(test, 'Sin ejecutar')))
    assert len(caminos) == V
    # independencia lineal de los caminos (rango de la matriz de incidencia de aristas)
    idx = {(a, b): k for k, (a, b, _) in enumerate(spec['aristas'])}
    filas = []
    for c in spec['caminos']:
        seq = [int(x) for x in c[0].split('-')]
        v = [0] * E
        for a, b in zip(seq, seq[1:]):
            v[idx[(a, b)]] += 1
        filas.append(v)
    from fractions import Fraction
    M = [[Fraction(x) for x in f] for f in filas]; rango = 0
    for col in range(E):
        piv = next((r for r in range(rango, len(M)) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[rango], M[piv] = M[piv], M[rango]
        for r in range(len(M)):
            if r != rango and M[r][col] != 0:
                f = M[r][col] / M[rango][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[rango])]
        rango += 1
    assert rango == V, (spec['cu'], rango)
    return dict(cu=spec['cu'], nombre=spec['nombre'], rf=spec['rf'], servicio=spec['servicio'], N=N, E=E, P=len(predicados),
                V=V, regiones=V, predicados=predicados, matriz=matriz, nodos=spec['nodos'], aristas=spec['aristas'],
                suma_matriz=suma_matriz, caminos=caminos, rango_caminos=rango)


def guardar():
    out = ROOT / 'docs/auditoria-fase-final/pruebas/caja_blanca_secuencias.json'
    datos = [calcular(s) for s in SPECS]
    out.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding='utf-8')
    for d in datos:
        print(f"CU{d['cu']}: N={d['N']} E={d['E']} P={d['P']} V={d['V']} caminos={len(d['caminos'])}",
              {c['resultado'] for c in d['caminos']})
    return datos


def posiciones(spec):
    """Cadena principal en una columna; el rechazo a la derecha; las ramas opt a la izquierda."""
    lado = {6, 8} if spec['cu'] == 28 else set()
    rechazo, fin = spec['nodos'][-2][0], spec['nodos'][-1][0]
    pos, y = {}, 20
    for n, _, _ in spec['nodos']:
        if n in (rechazo, fin):
            continue
        if n in lado:
            pos[n] = (40, y - 40)
            continue
        pos[n] = (200, y); y += 80
    pos[rechazo] = (520, (20 + y) // 2 - 40)
    pos[fin] = (360, y + 10)
    return pos


def fragmentos(m, p, d, spec, x0):
    """Un fragmento por decisión. Los de un solo mensaje se ajustan a 34 unidades (EA separa los
    mensajes 35): así dos validaciones seguidas quedan una debajo de la otra sin solaparse."""
    import ea_cap7
    centro = {spec['actor']: x0 + 30}
    centro.update({v: x0 + i * 200 + 60 for i, v in enumerate(spec['vidas'], 1)})
    for operador, operandos in spec['fragmentos']:
        (guarda, desde, hasta), = operandos
        usadas = {x for a, b, _, _ in spec['mensajes'][desde - 1:hasta] for x in (a, b)}
        izq = min(centro[v] for v in usadas) - max(80, len(guarda) * 6 + 30)
        der = max(centro[v] for v in usadas) + 80
        arriba, abajo = ea_cap7._y_mensaje(desde) - 22, ea_cap7._y_mensaje(hasta) + 12
        f = p.Elements.AddNew('', 'InteractionFragment'); f.Subtype = ea_cap7.OPERADOR[operador]; f.Update()
        pa = f.Partitions.AddNew(guarda, ''); pa.Size = abajo - arriba; f.Update()
        m.colocar(d, f, izq, arriba, der - izq, abajo - arriba)


def diagramas(m, raiz, fig):
    import ea_cap7
    for spec in SPECS:
        p = m.paquete(f"CU{spec['cu']} {spec['nombre']}", raiz)
        # Secuencia con fragmentos
        d = m.diagrama(p, f"Secuencia CU{spec['cu']} (caja blanca)", 'Sequence')
        actor = m.elemento(p, spec['actor'], 'Actor')
        objs = {spec['actor']: actor}
        alto = 180 + 35 * len(spec['mensajes'])
        x0 = 150
        m.colocar(d, actor, x0, 50, 60, alto)
        for i, v in enumerate(spec['vidas'], 1):
            est = ('boundary' if v.endswith('View') else 'control' if v.endswith('Controller')
                   else 'service' if v.endswith('Service') else 'entity')
            e = m.elemento(p, v, 'Object', estereotipo=est); objs[v] = e
            m.colocar(d, e, x0 + i * 200, 50, 120, alto)
        for k, (a, b, texto, ret) in enumerate(spec['mensajes'], 1):
            c = objs[a].Connectors.AddNew(texto, 'Sequence')
            c.SupplierID = objs[b].ElementID; c.SequenceNo = k; c.DiagramID = d.DiagramID; c.Update()
            if ret:
                m.r.Execute("UPDATE t_connector SET PDATA4='1' WHERE Connector_ID=%d" % c.ConnectorID)
        fragmentos(m, p, d, spec, x0)
        m.exportar(d, str(fig / f"c9_seq_cu{spec['cu']:02d}.png"))
        # Grafo de flujo derivado
        g = m.diagrama(p, f"Grafo de flujo CU{spec['cu']}", 'Activity')
        pos = posiciones(spec); els = {}
        for n, etiqueta, mens in spec['nodos']:
            e = m.elemento(p, str(n), 'State', notas=f'{etiqueta} (mensajes {mens})')
            x, y = pos[n]; o = m.colocar(g, e, x, y, 40, 40)
            o.SetStyleEx('font', 'Arial'); o.SetStyleEx('fontsz', '160'); o.Update(); els[n] = e
        for a, b, rot in spec['aristas']:
            c = m.conectar(els[a], els[b], 'ControlFlow', nombre='')
            if not rot:
                continue
            (sx, sy), (tx, ty) = pos[a], pos[b]
            rama_izq = any(pos[b2][0] < sx for a2, b2, _ in spec['aristas'] if a2 == a)
            if sx == tx:  # tramo vertical: a la derecha si el nodo abre una rama a la izquierda
                x, y = (sx - 40, sy + 48) if rama_izq else (sx - 55, sy + 45)
            else:
                x, y = (sx + 50, sy - 20) if tx > sx else (sx - 75, sy + 2)
            t = m.elemento(p, rot, 'Text', notas=rot)
            o = m.colocar(g, t, x, y, 40, 25); o.SetStyleEx('font', 'Arial'); o.SetStyleEx('fontsz', '160'); o.Update()
        m.exportar(g, str(fig / f"c9_grafo_cu{spec['cu']:02d}.png"))


if __name__ == '__main__':
    guardar()
