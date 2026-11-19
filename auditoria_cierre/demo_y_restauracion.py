"""Solo se ejecuta dentro del runner aislado. Restaura, crea demo y levanta servidores efímeros."""
import datetime as dt
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error
import uuid
from urllib.parse import urlparse

import psycopg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "auditoria_cierre/05_ejecuciones_pruebas"
BACK = ROOT / "gestion-residuos-dsu/backend"
PG = Path(os.environ.get("DSU_PG_BIN", r"C:\Program Files\PostgreSQL\18\bin"))
url = os.environ["DATABASE_URL"]
parsed = urlparse(url)
if parsed.hostname != "127.0.0.1" or parsed.username != "dsu_audit" or not parsed.port:
    raise RuntimeError("Demo y restauración requieren el clúster dsu_audit en loopback")
flags = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}


def command(args, **kwargs):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf8", errors="replace", **flags, **kwargs)
    if r.returncode:
        raise RuntimeError(f"Falló {Path(args[0]).name}: " + r.stderr[-1000:])
    return r


def libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def esperar(url, expected=200):
    for _ in range(120):
        try:
            urllib.request.urlopen(url, timeout=1).close()
            return
        except urllib.error.HTTPError as error:
            if error.code == expected:
                return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("Servidor de prueba no respondió")


def conteos(conn):
    with conn.cursor() as c:
        c.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
        tablas = [r[0] for r in c.fetchall()]
        salida = {}
        for t in tablas:
            c.execute(psycopg.sql.SQL("SELECT count(*) FROM {}").format(psycopg.sql.Identifier(t)))
            salida[t] = c.fetchone()[0]
        c.execute("SELECT count(*) FROM pg_constraint WHERE contype='f' AND NOT convalidated")
        assert c.fetchone()[0] == 0
        return salida


command([sys.executable, "manage.py", "migrate", "--noinput"], cwd=BACK)
# Afirmación anterior garantiza que seed nunca apunta a Neon. Solo datos sintéticos de este clúster.
command([sys.executable, "manage.py", "seed", "--demo", "--historico", "--admin-password", "Prueba.Aislada.2026"], cwd=BACK)
command([sys.executable, "manage.py", "etl"], cwd=BACK)
command([sys.executable, "manage.py", "entrenar"], cwd=BACK)
common = ["-h", "127.0.0.1", "-p", str(parsed.port), "-U", "dsu_audit"]
dump = OUT / "demo_sintetica.dump"
t0 = time.monotonic()
command([str(PG / "pg_dump.exe"), *common, "-d", "postgres", "-Fc", "--no-owner", "--no-privileges", "-f", str(dump)])
destino = "dsu_restauracion_" + uuid.uuid4().hex[:8]
command([str(PG / "createdb.exe"), *common, destino])
command([str(PG / "pg_restore.exe"), *common, "-d", destino, "--no-owner", "--no-privileges", "--exit-on-error", str(dump)])
with psycopg.connect(url) as a, psycopg.connect(url.replace("/postgres", "/" + destino)) as b:
    original, restaurado = conteos(a), conteos(b)
    assert original == restaurado
    assert original["operations_registroresiduo"] > 0
    with b.cursor() as c:
        c.execute("SELECT count(*) FROM pg_trigger WHERE tgrelid='audit_auditlog'::regclass AND NOT tgisinternal AND tgenabled='O'")
        assert c.fetchone()[0] > 0
(OUT / "restauracion.json").write_text(json.dumps(dict(fecha_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
    entorno="PostgreSQL 18 aislado, origen y destino sintéticos", resultado="APROBADO", duracion_segundos=round(time.monotonic()-t0,2),
    tablas=original, coincidencia_total=True, claves_foraneas_validadas=True, trigger_auditoria_habilitado=True,
    limite="No mide RTO productivo ni restaura datos de Neon"), indent=2), encoding="utf8")
api_port, web_port = libre(), libre()
env = os.environ.copy()
env.update(DSU_API_PROXY=f"http://127.0.0.1:{api_port}", VITE_API_URL="", PYTHONUNBUFFERED="1")
children = []
logs = []
try:
    for name, args, cwd in [
        ("api_demo", [sys.executable,"manage.py","runserver",f"127.0.0.1:{api_port}","--noreload"], BACK),
        ("vite_demo", ["node", "node_modules/vite/bin/vite.js", "--host", "127.0.0.1", "--port",str(web_port)], ROOT/"gestion-residuos-dsu/frontend")]:
        log = (OUT / f"{name}.txt").open("w",encoding="utf8");logs.append(log)
        children.append(subprocess.Popen(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,**flags))
    esperar(f"http://127.0.0.1:{api_port}/api/", expected=401)
    esperar(f"http://127.0.0.1:{web_port}/")
    # El navegador se ejecuta en el Python del equipo que ya dispone de Playwright, sin perfil personal.
    browser_env=env.copy()
    browser_env.pop("__PYVENV_LAUNCHER__",None)
    r=command(["py","-3.8",str(ROOT/"auditoria_cierre/probar_demo_ui.py"),f"http://127.0.0.1:{web_port}/"],env=browser_env)
    print(r.stdout)
finally:
    for child in reversed(children):
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(child.pid), "/T", "/F"], capture_output=True, **flags)
            continue
        child.terminate()
        try: child.wait(timeout=15)
        except subprocess.TimeoutExpired: child.kill();child.wait()
    for log in logs:log.close()
print("Restauración con recuentos y claves foráneas: APROBADA")
