"""Regresión local en PostgreSQL propio; nunca usa Neon ni servicios instalados.

Ejecutar con backend/.venv/Scripts/python.exe auditoria_cierre/ejecutar_aislado.py.
Los datos y dumps sintéticos quedan excluidos del versionado.
"""
import datetime as dt
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "auditoria_cierre/05_ejecuciones_pruebas"
PG = Path(os.environ.get("DSU_PG_BIN", r"C:\Program Files\PostgreSQL\18\bin"))


def main():
    sys.stdout.reconfigure(encoding="utf8")
    OUT.mkdir(parents=True, exist_ok=True)
    data = OUT / ".postgres"
    flags = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}

    def command(args, **kwargs):
        if Path(args[0]).stem == "pg_ctl":
            # PostgreSQL hereda handles en Windows; un PIPE puede esperar al servidor tras salir pg_ctl.
            target = OUT / "pg_ctl.txt"
            with target.open("w", encoding="utf8") as log:
                r = subprocess.run(args, stdout=log, stderr=subprocess.STDOUT, **flags, **kwargs)
            return subprocess.CompletedProcess(args, r.returncode, target.read_text(encoding="utf8", errors="replace"), "")
        return subprocess.run(args, capture_output=True, text=True, encoding="utf8", errors="replace", **flags, **kwargs)

    if not (data / "PG_VERSION").exists():
        r = command([str(PG / "initdb.exe"), "-D", str(data), "-U", "dsu_audit", "-A", "trust", "--encoding=UTF8", "--locale=C"])
        if r.returncode:
            print(r.stdout + r.stderr)
            return r.returncode
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    r = command([str(PG / "pg_ctl.exe"), "-D", str(data), "-l", str(OUT / ".postgres.log"), "-w", "start", "-o", f"-h 127.0.0.1 -p {port}"])
    if r.returncode:
        print(r.stdout + r.stderr)
        return r.returncode
    label = os.environ.get("DSU_RUN_LABEL", "regresion")
    env = os.environ.copy()
    env.update(DATABASE_URL=f"postgres://dsu_audit@127.0.0.1:{port}/postgres", SECRET_KEY="solo-entorno-aislado-no-produccion",
               DEBUG="False", SECURE_SSL_REDIRECT="False", MODELOS_DIR=str(OUT / ".modelos"), PYTHONIOENCODING="utf-8")
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        if os.environ.get("DSU_ONLY_PERFORMANCE") == "1":
            import psycopg

            def recuentos():
                with psycopg.connect(env["DATABASE_URL"]) as conn, conn.cursor() as cursor:
                    result = {}
                    for table in ["operations_registroresiduo", "operations_jornada", "campus_puntorecoleccion", "audit_auditlog", "prediction_modeloentrenado"]:
                        cursor.execute(psycopg.sql.SQL("SELECT count(*) FROM {}").format(psycopg.sql.Identifier(table)))
                        result[table] = cursor.fetchone()[0]
                    return result
            antes = recuentos()
            measured = command([sys.executable, "manage.py", "medir_rendimiento"], cwd=ROOT / "gestion-residuos-dsu/backend", env=env)
            (OUT / "rendimiento_local.txt").write_text(measured.stdout + measured.stderr, encoding="utf8")
            despues = recuentos()
            (OUT / "rendimiento_local.json").write_text(json.dumps(dict(inicio_utc=started,fin_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                exit_code=measured.returncode,antes=antes,despues=despues,rollback_verificado=antes==despues,
                entorno="Windows PostgreSQL 18 loopback; API en el mismo proceso, sin latencia de red productiva"),indent=2),encoding="utf8")
            assert antes == despues, "La medición no revirtió todos sus cambios"
            print(measured.stdout[-3500:] + measured.stderr[-1000:])
            return measured.returncode
        if os.environ.get("DSU_ONLY_EXTENDED") == "1":
            extended = command([sys.executable, str(ROOT / "auditoria_cierre/demo_y_restauracion.py")], cwd=ROOT, env=env)
            (OUT / "demo_ampliada.txt").write_text(extended.stdout + extended.stderr, encoding="utf8")
            print(extended.stdout[-2500:] + extended.stderr[-1500:])
            return extended.returncode
        r = command([sys.executable, "-m", "pytest", "-q", "--create-db", "--junitxml", str(OUT / f"{label}.xml"), *sys.argv[1:]],
                    cwd=ROOT / "gestion-residuos-dsu/backend", env=env)
        (OUT / f"{label}.txt").write_text(r.stdout + r.stderr, encoding="utf8")
        git = command(["git", "rev-parse", "HEAD"], cwd=ROOT)
        (OUT / f"{label}.json").write_text(json.dumps(dict(inicio_utc=started, fin_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            commit=git.stdout.strip(), cambios_locales=True, entorno="Windows PostgreSQL 18 aislado en loopback", exit_code=r.returncode,
            comando="python auditoria_cierre/ejecutar_aislado.py " + " ".join(sys.argv[1:]), datos="Fixtures sintéticas; no Neon"), indent=2), encoding="utf8")
        print(r.stdout[-7000:] + r.stderr[-1500:])
        if r.returncode == 0 and os.environ.get("DSU_EXTENDED") == "1":
            extended = command([sys.executable, str(ROOT / "auditoria_cierre/demo_y_restauracion.py")], cwd=ROOT, env=env)
            print(extended.stdout[-2500:] + extended.stderr[-1500:])
            if extended.returncode:
                return extended.returncode
        return r.returncode
    finally:
        command([str(PG / "pg_ctl.exe"), "-D", str(data), "-w", "stop", "-m", "fast"])


if __name__ == "__main__":
    sys.exit(main())
