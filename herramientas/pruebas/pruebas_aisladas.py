"""Ejecuta pruebas en PostgreSQL desechable, sin usar DATABASE_URL de Neon.

Usa Docker local con puerto aleatorio enlazado exclusivamente a loopback.
Las credenciales aleatorias viven solo en los procesos de esta ejecución.
"""
import datetime as dt
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACK = ROOT / 'gestion-residuos-dsu/backend'
OUT = ROOT / 'docs/auditoria-fase-final/pruebas'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    label = 'dsu-software2-auditoria-' + secrets.token_hex(5)
    password = secrets.token_urlsafe(30)
    subprocess.run(['docker', 'run', '-d', '--name', label, '--label', f'dsu.audit={label}',
                    '-e', f'POSTGRES_PASSWORD={password}', '-e', 'POSTGRES_DB=dsu_auditoria',
                    '-p', '127.0.0.1::5432', 'postgres:18-alpine'], check=True, capture_output=True)
    try:
        for _ in range(60):
            if subprocess.run(['docker', 'exec', label, 'pg_isready', '-U', 'postgres'],
                              capture_output=True).returncode == 0:
                break
            time.sleep(1)
        else:
            raise RuntimeError('PostgreSQL aislado no inició')
        info = json.loads(subprocess.check_output(['docker', 'inspect', label]))[0]
        port = info['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']
        env = os.environ.copy()
        env.update(DATABASE_URL=f'postgres://postgres:{password}@127.0.0.1:{port}/dsu_auditoria',
                   SECRET_KEY=secrets.token_urlsafe(60), DEBUG='True',
                   MODELOS_DIR=str(OUT / '.modelos.local'), PYTHONIOENCODING='utf-8',
                   DSU_AUDIT_OUTPUT=str(OUT), PYTHONPATH=str(Path(__file__).parent))
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        result = subprocess.run([str(BACK / '.venv/Scripts/python.exe'), '-m', 'pytest',
                                 '-p', 'evidencias_pytest', '--junitxml', str(OUT / 'pytest.xml'), '-q'],
                                cwd=BACK, env=env, capture_output=True, text=True, encoding='utf-8')
        (OUT / 'pytest.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
        summary = dict(inicio_utc=started, fin_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                       entorno='Windows / PostgreSQL 18 Docker aislado en loopback',
                       datos='Fixtures sintéticas de prueba; ninguna escritura en Neon',
                       exit_code=result.returncode, comando='python -m pytest --junitxml <evidencia> -q',
                       objetivo='Regresión de API y servicios; no certifica rendimiento productivo')
        (OUT / 'ejecucion.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
        print(result.stdout[-5000:])
        return result.returncode
    finally:
        # Solo retirar el contenedor creado y etiquetado por esta ejecución.
        info = json.loads(subprocess.check_output(['docker', 'inspect', label]))[0]
        if info['Config']['Labels'].get('dsu.audit') != label:
            raise RuntimeError('Etiqueta de propiedad del contenedor no coincide')
        subprocess.run(['docker', 'rm', '-f', '-v', label], check=True, capture_output=True)


if __name__ == '__main__':
    sys.exit(main())
