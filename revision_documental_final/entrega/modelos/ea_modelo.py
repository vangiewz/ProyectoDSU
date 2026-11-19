# -*- coding: utf-8 -*-
"""Construye el modelo UML de la Fase 2 en Enterprise Architect y exporta sus
diagramas como PNG a generador/figuras/fase2/.

Uso (Python del sistema, con pywin32 y EA instalado):
    python fase2/ea_modelo.py            # todo
    python fase2/ea_modelo.py cap5       # solo los diagramas del capitulo 5
    (cap4 = los diagramas UML de la Fase 1 rehechos en EA: ver ea_fase1.py)

El modelo queda en modelo_uml/DSU-Residuos.eapx para abrirlo y retocarlo en EA.
Cada ejecucion lo reconstruye desde cero a partir de datos.py.
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import datos as D                      # noqa: E402
from ea_util import Modelo             # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(BASE))
RUTA_MODELO = os.path.join(RAIZ, "modelo_uml", "DSU-Residuos.eapx")
DIR_FIG = os.path.join(os.path.dirname(BASE), "figuras", "fase2")

CU_W, CU_H = 190, 80
ACT_W, ACT_H = 60, 90


def fig(nombre):
    return os.path.join(DIR_FIG, nombre)


# ----------------------------------------------------------------------
# elementos y relaciones de casos de uso (comunes a cap. 5 y 6)
# ----------------------------------------------------------------------
class CasosDeUso:
    def __init__(self, m):
        self.m = m
        self.p_act = m.paquete("Actores")
        self.p_req = m.paquete("Requisitos")
        self.act = {}
        for k, a in D.ACTORES.items():
            self.act[k] = m.elemento(self.p_act, a["nombre"], "Actor",
                                     abstracto=a.get("abstracto", False),
                                     notas=a["desc"])
        self.cu = {}
        for c in D.CU:
            self.cu[c["n"]] = m.elemento(self.p_req, D.etiqueta(c["n"]), "UseCase",
                                         notas=c["desc"])
        # relaciones: se guardan para decidir que mostrar en cada diagrama
        self.rel = []          # (tipo, origen_clave, destino_clave, conector)
        for c in D.CU:
            n = c["n"]
            for a in c["actores"]:
                con = m.conectar(self.act[a], self.cu[n], "Association")
                self.rel.append(("asoc", ("a", a), ("c", n), con))
            for i in c["incluye"]:
                con = m.conectar(self.cu[n], self.cu[i], "Dependency",
                                 estereotipo="include")
                self.rel.append(("include", ("c", n), ("c", i), con))
            if c["extiende"]:
                con = m.conectar(self.cu[n], self.cu[c["extiende"][0]], "Dependency",
                                 estereotipo="extend")
                self.rel.append(("extend", ("c", n), ("c", c["extiende"][0]), con))
            if c["especializa"]:
                con = m.conectar(self.cu[n], self.cu[c["especializa"]],
                                 "Generalization")
                self.rel.append(("gen_cu", ("c", n), ("c", c["especializa"]), con))

    def el(self, clave):
        return self.act[clave[1]] if clave[0] == "a" else self.cu[clave[1]]

    def relacionados(self, n):
        """CU vinculados a n por include, extend o especializacion."""
        otros = []
        for _, o, d, _c in self.rel:
            if o == ("c", n) and d[0] == "c":
                otros.append(d[1])
            elif d == ("c", n) and o[0] == "c":
                otros.append(o[1])
        return list(dict.fromkeys(otros))


# ----------------------------------------------------------------------
# capitulo 5
# ----------------------------------------------------------------------
def cap5(m, cu):
    p = cu.p_req
    nombres = []

    # 5.1 forma 1: paquete de actores + nota con el nombre del sistema (como
    # la Figura 19 del ejemplo: el paquete solo del alto de su lista)
    d = m.diagrama(cu.p_act, "Identificación de actores", "Use Case")
    pk_el = m.r.GetElementByGuid(cu.p_act.PackageGUID)
    m.colocar(d, pk_el, 40, 40, 240, 38 + 17 * len(D.ACTORES))
    nota = m.elemento(cu.p_act, "", "Note", notas=D.SISTEMA.upper())
    m.colocar(d, nota, 370, 55, 330, 75)
    m.conectar(nota, pk_el, "NoteLink")
    m.exportar(d, fig("c5_actores_paquete.png"))

    # 5.1 forma 2: cada actor con la nota de su funcion (Figura 20 del
    # ejemplo); los actores son independientes: sin relaciones entre ellos
    d = m.diagrama(cu.p_act, "Actores", "Use Case")
    for i, k in enumerate(D.ACTORES):
        y = 30 + i * 140
        m.colocar(d, cu.act[k], 80, y, ACT_W, ACT_H)
        n = m.elemento(cu.p_act, "", "Note", notas=D.ACTORES[k]["desc"])
        m.colocar(d, n, 280, y + 5, 400, 80)
        m.conectar(n, cu.act[k], "NoteLink")
    m.exportar(d, fig("c5_actores_descripcion.png"))

    # 5.4 un diagrama por caso de uso
    for c in D.CU:
        n = c["n"]
        d = m.diagrama(p, D.etiqueta(n), "Use Case")
        actores = c["actores"]
        otros = cu.relacionados(n)
        if len(otros) > 6:
            # CU incluido por muchos (CU33): el CU al centro y los demas en dos
            # columnas, sin actores propios
            izq, der = otros[:len(otros) // 2], otros[len(otros) // 2:]
            alto = len(der) * 100
            m.colocar(d, cu.cu[n], 330, 30 + alto // 2 - CU_H // 2, CU_W + 20, CU_H + 10)
            for col, x in ((izq, 40), (der, 640)):
                for i, o in enumerate(col):
                    y = 30 + i * 100 + (alto - len(col) * 100) // 2
                    m.colocar(d, cu.cu[o], x, y, CU_W, CU_H)
        else:
            alto = max(len(actores), len(otros), 1) * 140
            for i, a in enumerate(actores):
                y = 30 + i * 140 + (alto - len(actores) * 140) // 2
                m.colocar(d, cu.act[a], 60, y, ACT_W, ACT_H)
            m.colocar(d, cu.cu[n], 250, 30 + alto // 2 - CU_H // 2 - 20, CU_W + 20, CU_H + 10)
            for i, o in enumerate(otros):
                y = 30 + i * 140 + (alto - len(otros) * 140) // 2
                m.colocar(d, cu.cu[o], 560, y, CU_W, CU_H)
        # solo las asociaciones del CU del titulo: las de los actores con los CU
        # relacionados cruzaban el diagrama
        m.ocultar_conectores(d, [con.ConnectorID for t, o, de, con in cu.rel
                                 if t == "asoc" and de[1] in otros and o[1] in actores])
        m.exportar(d, fig("c5_cu%02d.png" % n))
        nombres.append(d)

    # 5.5 diagrama general
    general(m, cu)


COLS, FILAS, COL_W, FILA_H = 7, 11, 300, 120
PESO_LARGO = 0.1
# escala de las distancias del optimizador respecto de CU de 190x80 (1 = fase 2)
K = 1.0
# penalizaciones del optimizador del diagrama general
PESOS = dict(dentro=3000, roza=300, etiq=2000, cruces=2500)
X0, Y0 = 360, 330
ALTO_G = FILAS * FILA_H
ANCHO_G = COLS * COL_W + COL_W // 2      # las filas impares van corridas media celda
# los actores van por fuera del limite: tres lugares por lado y la busqueda
# elige en cual queda cada uno (menos cruces)
X_IZQ, X_DER = X0 - 190, X0 + ANCHO_G + 110
Y_ARR, Y_ABA = Y0 - 200, Y0 + ALTO_G + 90
LUGARES_ACTOR = ([(X_IZQ, Y0 + ALTO_G * (i + 1) // 4) for i in range(3)] +
                 [(X_DER, Y0 + ALTO_G * (i + 1) // 4) for i in range(3)] +
                 [(X0 + ANCHO_G * (i + 1) // 4, Y_ARR) for i in range(3)] +
                 [(X0 + ANCHO_G * (i + 1) // 4, Y_ABA) for i in range(3)])


def disposicion_general(semilla=0, pasos=200000, fijos=None):
    """Ubica los CU en una grilla escalonada y ordena los actores de cada
    lado por recocido simulado. Penaliza el largo de las lineas, las que pasan
    sobre el texto de otro CU (y menos las que lo rozan), las etiquetas
    «include»/«extend» que caen sobre un CU y los cruces. Devuelve
    ({n: (x, y)}, {actor: (x, y)}, costo) con centros en coordenadas del
    diagrama. ponytail: heuristica; ~1 min por semilla."""
    import math
    import random
    import numpy as np
    rnd = random.Random(semilla)
    celdas = [(X0 + c * COL_W + (COL_W // 2 if f % 2 else 0) + CU_W // 2,
               Y0 + f * FILA_H + CU_H // 2) for f in range(FILAS) for c in range(COLS)]
    huecos = celdas + LUGARES_ACTOR
    nc = len(celdas)
    lugares = list(range(nc, len(huecos)))
    nodos = [("c", c["n"]) for c in D.CU] + [("a", k) for k in D.ACTORES]
    idx = {nd: i for i, nd in enumerate(nodos)}
    ar = []
    for c in D.CU:
        for a in c["actores"]:
            ar.append((("a", a), ("c", c["n"])))
        for i in c["incluye"]:
            ar.append((("c", c["n"]), ("c", i)))
        if c["extiende"]:
            ar.append((("c", c["n"]), ("c", c["extiende"][0])))
        if c["especializa"]:
            ar.append((("c", c["n"]), ("c", c["especializa"])))
    U = np.array([idx[u] for u, _ in ar])
    V = np.array([idx[v] for _, v in ar])
    dep = np.array([u[0] == "c" and v[0] == "c" for u, v in ar])
    H = np.array(huecos, dtype=float)
    ncu, nn = len(D.CU), len(nodos)
    otro_cu = ~((np.arange(nn)[None, :] == U[:, None]) | (np.arange(nn)[None, :] == V[:, None]))         & (np.arange(nn) < ncu)[None, :]
    comparte = (U[:, None] == U[None, :]) | (U[:, None] == V[None, :]) |                (V[:, None] == U[None, :]) | (V[:, None] == V[None, :])

    def orient(p, q, r):
        return np.sign((q[..., 0] - p[..., 0]) * (r[..., 1] - p[..., 1]) -
                       (q[..., 1] - p[..., 1]) * (r[..., 0] - p[..., 0]))

    def costo(asig, detalle=False):
        P = H[asig]
        A, B = P[U], P[V]
        largo = np.hypot(*(A - B).T).sum()
        AB = B - A
        L2 = (AB ** 2).sum(1) + 1e-9
        t = (((P[None] - A[:, None]) * AB[:, None]).sum(2) / L2[:, None]).clip(0, 1)
        q = A[:, None] + t[:, :, None] * AB[:, None]
        dx, dy = P[None, :, 0] - q[:, :, 0], P[None, :, 1] - q[:, :, 1]
        dentro = (((dx / (95 * K)) ** 2 + (dy / (32 * K)) ** 2 < 1) & otro_cu).sum()
        roza = (((dx / (118 * K)) ** 2 + (dy / (48 * K)) ** 2 < 1) & otro_cu).sum() - dentro
        M = (A + B) / 2
        ex, ey = (P[None, :, 0] - M[:, None, 0]) / (130 * K), (P[None, :, 1] - M[:, None, 1]) / (55 * K)
        etiq = ((ex ** 2 + ey ** 2 < 1) & otro_cu & dep[:, None]).sum()
        a1, b1, a2, b2 = A[:, None], B[:, None], A[None], B[None]
        cruces = ((orient(a1, b1, a2) != orient(a1, b1, b2)) &
                  (orient(a2, b2, a1) != orient(a2, b2, b1)) & ~comparte).sum() / 2
        if detalle:
            return int(cruces), int(dentro), int(etiq)
        return (PESO_LARGO * largo + PESOS['dentro'] * dentro + PESOS['roza'] * roza +
                PESOS['etiq'] * etiq + PESOS['cruces'] * cruces)

    # arranque: actores en sus lugares (fijos o al azar); cada CU en la celda
    # libre mas cercana al promedio de sus actores, y los CU sin actor junto a
    # su CU base (incluido por, extendido o padre)
    la = lugares[:]
    rnd.shuffle(la)
    fijos = fijos or {}
    act_l = [nc + fijos[k] if k in fijos else None for k in D.ACTORES]
    libres_l = [h for h in la if h not in act_l]
    act_l = [h if h is not None else libres_l.pop() for h in act_l]
    pos_act = {k: H[h] for k, h in zip(D.ACTORES, act_l)}
    base = {}
    for c in D.CU:
        for i in c["incluye"]:
            base.setdefault(i, c["n"])
        if c["extiende"]:
            base[c["n"]] = c["extiende"][0]
        if c["especializa"]:
            base[c["n"]] = c["especializa"]

    def objetivo(n, prof=0):
        c = D.CU_POR_N[n]
        if c["actores"]:
            return np.mean([pos_act[a] for a in c["actores"]], axis=0)
        if n in base and prof < 5:
            return objetivo(base[n], prof + 1) + np.array([0, 60 * (n % 3 - 1)])
        return np.array([X0 + ANCHO_G / 2, Y0 + ALTO_G / 2])

    libres = set(range(nc))
    cel = [0] * ncu
    orden = sorted(range(ncu), key=lambda i: -len(D.CU[i]["actores"]))
    for i in orden:
        t = objetivo(D.CU[i]["n"]) + rnd.uniform(-40, 40)
        h = min(libres, key=lambda h: np.hypot(*(H[h] - t)))
        libres.discard(h)
        cel[i] = h
    asig = np.array(cel + act_l)
    ocupa = {h: i for i, h in enumerate(asig)}
    actual = costo(asig)
    mejor = (actual, asig.copy())
    T0, T1 = 1500.0, 5.0
    for k in range(pasos):
        T = T0 * (T1 / T0) ** (k / pasos)
        if rnd.random() < 0.9:
            i, dest = rnd.randrange(ncu), rnd.randrange(nc)
        else:
            i = rnd.randrange(ncu, nn)
            if D.CU and list(D.ACTORES)[i - ncu] in fijos:
                continue
            dest = rnd.choice(lugares)
        o = asig[i]
        if dest == o:
            continue
        j = ocupa.get(dest)
        asig[i] = dest
        if j is not None:
            asig[j] = o
        c = costo(asig)
        if c < actual or rnd.random() < math.exp((actual - c) / T):
            actual = c
            ocupa[dest] = i
            if j is not None:
                ocupa[o] = j
            else:
                ocupa.pop(o, None)
            if c < mejor[0]:
                mejor = (c, asig.copy())
        else:
            asig[i] = o
            if j is not None:
                asig[j] = dest
    # pulido: probar todos los movimientos y quedarse con los que mejoran,
    # hasta que ninguno mejore (el recocido solo se estanca en minimos locales)
    asig, actual = mejor[1].copy(), mejor[0]
    ocupa = {h: i for i, h in enumerate(asig)}
    movibles = [i for i in range(nn) if i < ncu or list(D.ACTORES)[i - ncu] not in fijos]
    mejoro = True
    while mejoro:
        mejoro = False
        for i in movibles:
            for dest in (range(nc) if i < ncu else lugares):
                o = asig[i]
                if dest == o:
                    continue
                j = ocupa.get(dest)
                asig[i] = dest
                if j is not None:
                    asig[j] = o
                c = costo(asig)
                if c < actual - 1e-6:
                    actual, mejoro = c, True
                    ocupa[dest] = i
                    if j is not None:
                        ocupa[o] = j
                    else:
                        ocupa.pop(o, None)
                else:
                    asig[i] = o
                    if j is not None:
                        asig[j] = dest
    mejor = (actual, asig)
    pos_c = {nodos[i][1]: huecos[asig[i]] for i in range(ncu)}
    pos_a = {nodos[i][1]: huecos[asig[i]] for i in range(ncu, nn)}
    return pos_c, pos_a, mejor[0], costo(asig, detalle=True)


def refinar(pos_c, pos_a, semilla=0, pasos=300000):
    """Parte de la grilla y mueve cada nodo libremente (CU dentro del limite,
    actores sobre uno de sus cuatro lados) por recocido: penaliza cruces,
    lineas sobre un CU, CU solapados y, poco, el largo. Devuelve lo mismo que
    disposicion_general. ponytail: heuristica; ~1,5 min por semilla y ~70
    cruces, el minimo practico con lineas rectas para estas asociaciones."""
    import math
    import random
    import numpy as np
    rnd = random.Random(semilla)
    nodos = [("c", c["n"]) for c in D.CU] + [("a", k) for k in D.ACTORES]
    idx = {nd: i for i, nd in enumerate(nodos)}
    P = np.array([pos_c[n] if t == "c" else pos_a[n] for t, n in nodos], float)
    ncu, nn = len(D.CU), len(nodos)
    ar = []
    for c in D.CU:
        ar += [(idx[("a", a)], idx[("c", c["n"])]) for a in c["actores"]]
        ar += [(idx[("c", c["n"])], idx[("c", i)]) for i in c["incluye"]]
        if c["extiende"]:
            ar.append((idx[("c", c["n"])], idx[("c", c["extiende"][0])]))
        if c["especializa"]:
            ar.append((idx[("c", c["n"])], idx[("c", c["especializa"])]))
    U = np.array([u for u, _ in ar])
    V = np.array([v for _, v in ar])
    comparte = ((U[:, None] == U[None]) | (U[:, None] == V[None]) |
                (V[:, None] == U[None]) | (V[:, None] == V[None]))
    otro = (~((np.arange(nn)[None] == U[:, None]) | (np.arange(nn)[None] == V[:, None])) &
            (np.arange(nn) < ncu)[None])
    x0, y0, x1, y1 = X0, Y0, X0 + ANCHO_G, Y0 + ALTO_G

    def orient(p, q, r):
        return np.sign((q[..., 0] - p[..., 0]) * (r[..., 1] - p[..., 1]) -
                       (q[..., 1] - p[..., 1]) * (r[..., 0] - p[..., 0]))

    def costo(P, detalle=False):
        A, B = P[U], P[V]
        a1, b1, a2, b2 = A[:, None], B[:, None], A[None], B[None]
        cruces = ((orient(a1, b1, a2) != orient(a1, b1, b2)) &
                  (orient(a2, b2, a1) != orient(a2, b2, b1)) & ~comparte).sum() / 2
        AB = B - A
        L2 = (AB ** 2).sum(1) + 1e-9
        t = (((P[None] - A[:, None]) * AB[:, None]).sum(2) / L2[:, None]).clip(0, 1)
        q = A[:, None] + t[:, :, None] * AB[:, None]
        dx, dy = P[None, :, 0] - q[:, :, 0], P[None, :, 1] - q[:, :, 1]
        dentro = (((dx / (110 * K)) ** 2 + (dy / (45 * K)) ** 2 < 1) & otro).sum()
        C = P[:ncu]
        solape = ((np.abs(C[:, None, 0] - C[None, :, 0]) < 240 * K) &
                  (np.abs(C[:, None, 1] - C[None, :, 1]) < 110 * K)).sum() - ncu
        if detalle:
            return int(cruces), int(dentro), int(solape)
        return (2500 * cruces + 3000 * dentro + 4000 * solape +
                0.1 * np.hypot(*(A - B).T).sum())

    actual = costo(P)
    mejor = (actual, P.copy())
    for k in range(pasos):
        T = 2000 * (5 / 2000) ** (k / pasos)
        i = rnd.randrange(nn)
        antes = P.copy()
        if i < ncu:
            if rnd.random() < 0.2:
                j = rnd.randrange(ncu)
                P[[i, j]] = P[[j, i]]
            else:
                s = 300 * (1 - k / pasos) + 30
                P[i] = [min(max(P[i, 0] + rnd.gauss(0, s), x0 + 110 * K), x1 - 90 * K),
                        min(max(P[i, 1] + rnd.gauss(0, s), y0 + 40 * K), y1 - 40 * K)]
        else:
            P[i] = rnd.choice([[X_IZQ, rnd.uniform(y0, y1)], [X_DER, rnd.uniform(y0, y1)],
                               [rnd.uniform(x0, x1), Y_ARR], [rnd.uniform(x0, x1), Y_ABA]])
        c = costo(P)
        if c < actual or rnd.random() < math.exp((actual - c) / T):
            actual = c
            if c < mejor[0]:
                mejor = (c, P.copy())
        else:
            P = antes
    P = mejor[1]
    pos_c = {n: tuple(P[i]) for i, (t, n) in enumerate(nodos) if t == "c"}
    pos_a = {n: tuple(P[i]) for i, (t, n) in enumerate(nodos) if t == "a"}
    return pos_c, pos_a, mejor[0], costo(P, detalle=True)


def general(m, cu):
    """Diagrama general: el sistema como limite, los 34 CU dentro y los
    actores alrededor, ubicados por disposicion_general() y refinar()."""
    d = m.diagrama(cu.p_req, "Diagrama general de casos de uso", "Use Case")
    base = min((disposicion_general(s, pasos=40000) for s in range(4)), key=lambda r: r[2])
    mejor = min((refinar(base[0], base[1], s) for s in range(1, 4)), key=lambda r: r[2])
    pos_c, pos_a, _, (cruces, sobre_cu, _e) = mejor
    limite = m.elemento(cu.p_req, D.SISTEMA, "Boundary")
    m.al_fondo(m.colocar(d, limite, X0 - 40, Y0 - 60, ANCHO_G + 20, ALTO_G + 60))
    print("general: costo %d, cruces %d, líneas sobre un CU %d" % (mejor[2], cruces, sobre_cu))
    for n, (x, y) in pos_c.items():
        m.al_frente(m.colocar(d, cu.cu[n], x - CU_W // 2, y - CU_H // 2, CU_W + 20, CU_H))
    for k, (x, y) in pos_a.items():
        m.colocar(d, cu.act[k], x - ACT_W // 2, y - ACT_H // 2, ACT_W, ACT_H)
    m.exportar(d, fig("c5_general.png"))


# ----------------------------------------------------------------------
# capitulo 6
# ----------------------------------------------------------------------
# dependencias entre paquetes de analisis (origen usa a destino), aciclicas;
# los paquetes 1 y 8 son transversales y se anotan aparte
DEP_PAQUETES = [(6, 5), (6, 7), (6, 2), (7, 5), (7, 4), (7, 2), (5, 3), (5, 4),
                (4, 3), (4, 2), (3, 2), (2, 1), (8, 1)]


def cap6(m, cu):
    import analisis as A
    p_paq = m.paquete("Paquetes de análisis")
    paq = {}
    for q in D.PAQUETES:
        paq[q["n"]] = m.paquete(q["nombre"], p_paq)
    el = {n: m.r.GetElementByGuid(p.PackageGUID) for n, p in paq.items()}

    # 6.1.1 identificacion de paquetes (sin relaciones)
    d = m.diagrama(p_paq, "Identificación de paquetes", "Package")
    for i, q in enumerate(D.PAQUETES):
        m.colocar(d, el[q["n"]], 40 + (i % 4) * 300, 40 + (i // 4) * 200, 250, 130)
    m.exportar(d, fig("c6_paquetes.png"))

    # «trace» de cada paquete a sus casos de uso
    traza = {}
    for c in D.CU:
        traza[c["n"]] = m.conectar(el[c["paq"]], cu.cu[c["n"]], "Dependency",
                                   estereotipo="trace")

    for q in D.PAQUETES:
        n = q["n"]
        cus = [c for c in D.CU if c["paq"] == n]
        # 6.1.2 relacion del paquete con sus CU
        d = m.diagrama(paq[n], "Relación del paquete %s" % q["nombre"], "Use Case")
        # CU en arco alrededor del paquete: cada «trace» llega derecho a su CU
        # sin pasar por otro
        import math
        radio = max(330, len(cus) * 62)
        abre = math.radians(min(70, 18 * len(cus)))
        px, py = 40, 30 + int(radio * math.sin(abre))
        m.colocar(d, el[n], px, py - 65, 230, 130)
        arco = []
        for i in range(len(cus)):
            t = -abre + (2 * abre * i / (len(cus) - 1) if len(cus) > 1 else abre)
            arco.append((px + 115 + int(radio * math.cos(t)) + 60 - (CU_W + 20) // 2,
                         py + int(radio * math.sin(t)) - CU_H // 2))
        # el orden en el arco lo elige el optimizador (el paquete queda fijo)
        import ea_cap7
        claves = [("c", c["n"]) for c in cus]
        dims = {k: (CU_W + 20, CU_H) for k in claves}
        dims["paq"] = (230, 130)
        aristas = [("paq", k) for k in claves] + [(o, de) for t, o, de, _ in cu.rel
                                                  if o in dims and de in dims]
        pos = ea_cap7.optimizar(claves + ["paq"], aristas, arco + [(px, py - 65)], dims,
                                permitidas={**{k: range(len(arco)) for k in claves},
                                            "paq": [len(arco)]})
        for k in claves:
            x, y = pos[k]
            m.colocar(d, cu.cu[k[1]], x, y, CU_W + 20, CU_H)
        m.exportar(d, fig("c6_rel_p%d.png" % n))

        # 6.1.3 encapsulamiento: paquete como contenedor con CU y actores
        d = m.diagrama(paq[n], "Encapsulamiento del paquete %s" % q["nombre"],
                       "Use Case")
        filas = (len(cus) + 1) // 2 + 1        # una fila de holgura
        alto = max(filas * 130 + 60, 330)
        # el paquete detras de sus CU (si no, los tapa)
        m.al_fondo(m.colocar(d, el[n], 260, 30, 620, alto))
        actores = list(dict.fromkeys(a for c in cus for a in c["actores"]))
        # CU en dos columnas dentro del paquete y actores a los costados: el
        # recocido elige el lado de cada actor y la celda de cada CU
        import ea_cap7
        celdas = [(300 + k * 290, 90 + f * 130) for f in range(filas) for k in range(2)]
        n_cu = len(celdas)
        lados = max(2, (len(actores) + 1) // 2 + 1)
        for x in (80, 1000):
            celdas += [(x, 30 + (f + 1) * alto // (lados + 1) - ACT_H // 2) for f in range(lados)]
        nombres = [("c", c["n"]) for c in cus] + [("a", a) for a in actores]
        dims = {k: ((CU_W + 20, CU_H) if k[0] == "c" else (ACT_W, ACT_H)) for k in nombres}
        permitidas = {k: range(n_cu) if k[0] == "c" else range(n_cu, len(celdas))
                      for k in nombres}
        aristas = [(o, de) for t, o, de, _ in cu.rel if o in dims and de in dims]
        pos = ea_cap7.optimizar(nombres, aristas, celdas, dims, permitidas=permitidas,
                                peso_cruce=8000)
        for k, (x, y) in pos.items():
            w, h = dims[k]
            o = m.colocar(d, cu.el(k), x, y, w, h)
            if k[0] == "c":
                m.al_frente(o)
        m.ocultar_conectores(d, [traza[c["n"]].ConnectorID for c in cus])
        m.exportar(d, fig("c6_enc_p%d.png" % n))

    # 6.2 analisis de cada caso de uso: diagrama de comunicacion
    p_an = m.paquete("Análisis de casos de uso")
    for c in D.CU:
        colaboracion(m, cu, p_an, c, A.R[c["n"]], A.CONTROL_CU)

    # 6.3 analisis de paquetes: dependencias
    d = m.diagrama(p_paq, "Análisis de paquetes", "Package")
    pos = {6: (420, 30), 5: (40, 290), 7: (800, 290), 4: (420, 550),
           3: (40, 810), 2: (800, 810), 8: (40, 1070), 1: (800, 1070)}
    for n, (x, y) in pos.items():
        m.colocar(d, el[n], x, y, 270, 130)
    for a, b in DEP_PAQUETES:
        m.conectar(el[a], el[b], "Dependency")
    for n, texto, x in ((8, "Paquete transversal: todos los paquetes registran sus "
                        "operaciones críticas en la bitácora de auditoría y emiten "
                        "reportes a partir de la información de los demás.", 330),
                       (1, "Paquete transversal: controla el acceso de todos los "
                        "demás paquetes según el rol del usuario.", 1100)):
        nota = m.elemento(p_paq, "", "Note", notas=texto)
        m.colocar(d, nota, x, 1260, 260, 90)
        m.conectar(nota, el[n], "NoteLink")
    m.exportar(d, fig("c6_analisis_paquetes.png"))


def colaboracion(m, cu, p_an, c, spec, control_cu):
    n = c["n"]
    p = m.paquete("CU%d" % n, p_an)
    d = m.diagrama(p, "Análisis %s" % D.etiqueta(n), "Communication")
    ym = 420

    def obj(nombre, estereotipo):
        return m.elemento(p, nombre, "Object", estereotipo=estereotipo)

    ini = spec["ini"]
    # varios actores (iniciar y cerrar sesion): en columna, cada uno con el
    # mismo mensaje hacia la vista
    inis = ini if isinstance(ini, list) else [ini]
    origenes = []
    for i, k in enumerate(inis):
        es_actor = k in D.ACTORES
        o = cu.act[k] if es_actor else obj(k, "control")
        y = ym - 45 + int((i - (len(inis) - 1) / 2) * 150)
        m.colocar(d, o, 40, y, ACT_W if es_actor else 70, ACT_H if es_actor else 70)
        origenes.append(o)
    origen = origenes[0]
    vista = obj(spec["vista"], "boundary") if spec["vista"] else None
    if vista:
        m.colocar(d, vista, 330, ym - 35, 70, 70)
    ctrl = obj(spec["ctrl"], "control")
    m.colocar(d, ctrl, 610, ym - 35, 70, 70)

    # destinos en orden de aparicion
    destinos = []
    for _, _, llamadas in spec["ops"]:
        for dest, _ in llamadas:
            nombre = control_cu[int(dest[2:])] if dest.startswith("CU") else dest
            if nombre not in destinos and nombre != spec["ctrl"]:
                destinos.append(nombre)
    der = destinos[:5]
    paso = 150
    huecos = [(900, ym + int((i - (len(der) - 1) / 2) * paso)) for i in range(len(der))]
    huecos += [(610, ym - 290), (610, ym + 290), (1150, ym)][:len(destinos) - len(der)]
    objs = {}
    for i, nombre in enumerate(destinos):
        est = "control" if nombre.endswith("Controller") else "entity"
        objs[nombre] = obj(nombre, est)
        x, y = huecos[i]
        m.colocar(d, objs[nombre], x, y - 35, 70, 70)

    # etiquetas agrupadas por enlace
    etiquetas = {}

    def msg(a, b, texto):
        etiquetas.setdefault((a, b), []).append(texto + " →")

    for i, (m_act, m_ctrl, llamadas) in enumerate(spec["ops"], 1):
        if vista:
            msg("o", "v", "%d: %s" % (i, m_act))
            msg("v", "c", "%d.1: %s" % (i, m_ctrl))
            k0 = 2
        else:
            msg("o", "c", "%d: %s" % (i, m_ctrl))
            k0 = 1
        for k, (dest, texto) in enumerate(llamadas, k0):
            nombre = control_cu[int(dest[2:])] if dest.startswith("CU") else dest
            msg("c", "self" if nombre == spec["ctrl"] else nombre,
                "%d.%d: %s" % (i, k, texto))
    nodo = {"o": origen, "v": vista, "c": ctrl, "self": ctrl, **objs}
    d.Update()
    for (a, b), lineas in etiquetas.items():
        if a == "o" and len(origenes) > 1:
            for o in origenes:
                m.conectar(o, nodo[b], "Association", nombre="\r\n".join(lineas))
            continue
        con = m.conectar(nodo[a], nodo[b], "Association", nombre="\r\n".join(lineas))
        if a != "c" or b == "self":
            # enlaces horizontales: etiqueta sobre la linea y centrada
            m.etiqueta_arriba(d, con, max(len(t) for t in lineas), len(lineas))
    m.exportar(d, fig("c6_cu%02d.png" % n))


def main(partes):
    os.makedirs(DIR_FIG, exist_ok=True)
    os.makedirs(os.path.dirname(RUTA_MODELO), exist_ok=True)
    m = Modelo(RUTA_MODELO)
    try:
        if "cap4" in partes:
            import ea_fase1
            ea_fase1.cap4(m)
        cu = CasosDeUso(m)
        if "cap5" in partes:
            cap5(m, cu)
        if "cap6" in partes:
            cap6(m, cu)
        if "cap7" in partes:
            import ea_cap7
            ea_cap7.cap7(m, cu, fig)
    finally:
        m.cerrar()
    print("Modelo:", RUTA_MODELO)


if __name__ == "__main__":
    main(sys.argv[1:] or ["cap4", "cap5", "cap6", "cap7"])
