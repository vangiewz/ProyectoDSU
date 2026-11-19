"""Regresión sobre la imagen Linux de despliegue, con PostgreSQL aislado."""
import datetime as dt
import json
import secrets
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/auditoria-fase-final/pruebas_linux'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    name='dsu-linux-'+secrets.token_hex(4)
    db=name+'-db'
    password=secrets.token_urlsafe(30)
    subprocess.run(['docker','network','create','--label',f'dsu.audit={name}',name],check=True,capture_output=True)
    created=False
    try:
        subprocess.run(['docker','run','-d','--name',db,'--network',name,'--label',f'dsu.audit={name}',
                        '-e',f'POSTGRES_PASSWORD={password}','-e','POSTGRES_DB=dsu_auditoria',
                        'postgres:18-alpine'],check=True,capture_output=True)
        created=True
        for _ in range(60):
            if subprocess.run(['docker','exec',db,'pg_isready','-U','postgres'],capture_output=True).returncode==0:
                break
            time.sleep(1)
        else:
            raise RuntimeError('PostgreSQL aislado no inició')
        started=dt.datetime.now(dt.timezone.utc).isoformat()
        cmd=['docker','run','--rm','--network',name,'--label',f'dsu.audit={name}',
             '-e',f'DATABASE_URL=postgres://postgres:{password}@{db}:5432/dsu_auditoria',
             '-e',f'SECRET_KEY={secrets.token_urlsafe(60)}','-e','DEBUG=True',
             '-e','MODELOS_DIR=/tmp/modelos-audit','-e','DSU_AUDIT_OUTPUT=/evidencia',
             '-e','PYTHONPATH=/audit','-v',f'{Path(__file__).parent}:/audit:ro',
             '-v',f'{OUT}:/evidencia:rw','--entrypoint','sh','dsu-taller-audit:20261116','-c',
             'python -m pip install --user pytest pytest-django --quiet && python -m pytest -p evidencias_pytest --junitxml /evidencia/pytest.xml -q']
        r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
        (OUT/'pytest.txt').write_text(r.stdout+r.stderr,encoding='utf-8')
        info=json.loads(subprocess.check_output(['docker','image','inspect','dsu-taller-audit:20261116']))[0]
        (OUT/'ejecucion.json').write_text(json.dumps(dict(inicio_utc=started,fin_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            imagen=info['Id'],exit_code=r.returncode,entorno='Linux Docker / PostgreSQL 18 aislado; sin Neon',
            objetivo='Regresión sobre dependencias resueltas del contenedor; no acredita despliegue AWS'),ensure_ascii=False,indent=2),encoding='utf-8')
        print(r.stdout[-2500:])
        return r.returncode
    finally:
        if created:
            info=json.loads(subprocess.check_output(['docker','inspect',db]))[0]
            assert info['Config']['Labels'].get('dsu.audit')==name
            subprocess.run(['docker','rm','-f','-v',db],check=True,capture_output=True)
        net=json.loads(subprocess.check_output(['docker','network','inspect',name]))[0]
        assert net['Labels'].get('dsu.audit')==name
        subprocess.run(['docker','network','rm',name],check=True,capture_output=True)


if __name__=='__main__':
    sys.exit(main())
