"""Prueba de concurrencia (RNF4, RCM1, RCM2): N usuarios simultáneos contra un servidor en marcha.

Solo usa la biblioteca estándar. Ejemplos:

    # Lectura: 12 usuarios durante 60 s (no modifica datos, salvo la entrada de inicio de sesión en la bitácora)
    python scripts/carga.py --url http://127.0.0.1:8000 --usuario supervisor --clave '<clave>'

    # Con escrituras (RCM2): además registra vaciados en una jornada EN EJECUCIÓN. Correr contra una
    # rama de prueba de Neon, nunca contra producción: los vaciados quedan registrados.
    python scripts/carga.py --url ... --usuario supervisor --clave '<clave>' \\
        --jornada 12 --operario operario1 --clave-operario '<clave>'
"""

import argparse
import json
import random
import statistics
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, timedelta

LECTURAS = {
    "RTR3 búsqueda de puntos": ("puntos/", {"search": "P1"}),
    "RTR2 jornadas": ("jornadas/", {}),
    "RTR6 histórico": ("registros/", {}),
    "RTR9 indicadores 30 días": ("analitica/indicadores/", {}),
    "RTR7 mapa 30 días": ("analitica/mapa/", {}),
}
LIMITES = {"RTR3": 2, "RTR2": 3, "RTR6": 4, "RTR9": 5, "RTR7": 4, "RTR4": 3}


def pedir(base, ruta, token=None, datos=None, query=None):
    url = f"{base}/api/{ruta}"
    if query:
        url += "?" + "&".join(f"{k}={v}" for k, v in query.items())
    req = urllib.request.Request(
        url,
        data=json.dumps(datos).encode() if datos is not None else None,
        method="POST" if datos is not None else "GET",
    )
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    t = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            cuerpo = r.read()
            return r.status, time.perf_counter() - t, json.loads(cuerpo or b"null")
    except urllib.error.HTTPError as e:
        return e.code, time.perf_counter() - t, None
    except (urllib.error.URLError, TimeoutError):
        return 0, time.perf_counter() - t, None


def token(base, usuario, clave):
    estado, _, datos = pedir(base, "auth/login/", datos={"username": usuario, "password": clave})
    if estado != 200:
        raise SystemExit(f"No se pudo iniciar sesión como {usuario} (HTTP {estado}).")
    return datos["access"]


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--url", default="http://127.0.0.1:8000")
    a.add_argument("--usuarios", type=int, default=12)
    a.add_argument("--segundos", type=int, default=60)
    a.add_argument("--usuario", required=True)
    a.add_argument("--clave", required=True)
    a.add_argument("--jornada", type=int, help="Jornada EN EJECUCIÓN donde registrar vaciados (activa las escrituras).")
    a.add_argument("--operario")
    a.add_argument("--clave-operario")
    o = a.parse_args()
    base = o.url.rstrip("/")

    hoy = date.today()
    rango = {"desde": (hoy - timedelta(days=29)).isoformat(), "hasta": hoy.isoformat()}
    lectura = token(base, o.usuario, o.clave)  # un inicio de sesión compartido: el login limita 10 por minuto
    escritura = paradas = None
    if o.jornada:
        escritura = token(base, o.operario, o.clave_operario)
        _, _, jornada = pedir(base, f"jornadas/{o.jornada}/", escritura)
        paradas = [p["punto"] for p in jornada["ruta"]]
        tipo = pedir(base, "tipos-residuo/", escritura)[2]["results"][0]["id"]
        antes = pedir(base, "registros/", lectura, query={"jornada": o.jornada})[2]["count"]

    tiempos, errores, enviados = defaultdict(list), defaultdict(int), [0]
    candado = threading.Lock()
    fin = time.time() + o.segundos

    def usuario_virtual(n):
        rnd = random.Random(n)
        while time.time() < fin:
            if paradas and rnd.random() < 0.3:
                nombre = "RTR4 registro de vaciado"
                estado, seg, _ = pedir(
                    base,
                    f"jornadas/{o.jornada}/visitas/",
                    escritura,
                    datos={"punto": rnd.choice(paradas), "detalles": [{"tipo_residuo": tipo, "cantidad": "1.5"}]},
                )
                if estado == 201:
                    with candado:
                        enviados[0] += 1
            else:
                nombre, (ruta, query) = rnd.choice(list(LECTURAS.items()))
                q = {**query, **rango} if ruta.startswith(("analitica", "registros")) else query
                estado, seg, _ = pedir(base, ruta, lectura, query=q)
            with candado:
                tiempos[nombre].append(seg)
                if estado == 0 or estado >= 500:
                    errores[nombre] += 1
            time.sleep(rnd.uniform(0.5, 2))  # tiempo de "pensar" de una persona

    hilos = [threading.Thread(target=usuario_virtual, args=(i,)) for i in range(o.usuarios)]
    print(f"{o.usuarios} usuarios simultáneos durante {o.segundos} s contra {base}…")
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    total = sum(len(v) for v in tiempos.values())
    print(f"\n{total} peticiones, {sum(errores.values())} errores de servidor o conexión\n")
    print("| Operación | Peticiones | Mediana | p95 | Máximo | Límite | Cumple (p95) |")
    print("|---|---|---|---|---|---|---|")
    for nombre, v in sorted(tiempos.items()):
        v = sorted(v)
        p95 = v[min(len(v) - 1, int(len(v) * 0.95))]
        limite = LIMITES.get(nombre.split()[0])
        cumple = "✅" if limite and p95 <= limite and not errores[nombre] else "❌"
        print(
            f"| {nombre} | {len(v)} | {statistics.median(v):.2f} s | {p95:.2f} s | {v[-1]:.2f} s | "
            f"≤ {limite} s | {cumple} |"
        )
    if o.jornada:
        despues = pedir(base, "registros/", lectura, query={"jornada": o.jornada})[2]["count"]
        ok = despues - antes == enviados[0]
        veredicto = "sin pérdida ✅" if ok else "PÉRDIDA ❌"
        print(f"\nRCM2: {enviados[0]} vaciados confirmados, {despues - antes} guardados → {veredicto}")


if __name__ == "__main__":
    main()
