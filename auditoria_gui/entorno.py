"""Servicios QA propios en loopback. Nunca lee DATABASE_URL del .env.

Ejecutar con backend/.venv/Scripts/python.exe; DSU_GUI_PASSWORD solo en entorno.
Detener creando runtime/DETENER. Las operaciones del producto se hacen en recorridos.py.
"""
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

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'auditoria_gui'
RUN = OUT / 'runtime'
BACK = ROOT / 'gestion-residuos-dsu/backend'
PG = Path(r'C:\Program Files\PostgreSQL\18\bin')
FLAGS = {'creationflags': subprocess.CREATE_NO_WINDOW}

def port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def main():
    sys.stdout.reconfigure(encoding='utf8')
    assert os.environ.get('DSU_GUI_PASSWORD'), 'Falta credencial efímera'
    RUN.mkdir(parents=True, exist_ok=True)
    stop = RUN / 'DETENER'
    stop.unlink(missing_ok=True)
    data = RUN / 'postgres'
    def cmd(args, **kw):
        if Path(args[0]).stem == 'pg_ctl':
            r = subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,**FLAGS,**kw)
        else:
            r = subprocess.run(args,capture_output=True,text=True,encoding='utf8',errors='replace',**FLAGS,**kw)
            with (RUN/'preparacion_segura.log').open('a',encoding='utf8') as log:
                log.write((r.stdout+r.stderr).replace(os.environ['DSU_GUI_PASSWORD'],'[OMITIDO]'))
        if r.returncode:
            raise RuntimeError('Falló preparación: ' + Path(args[0]).name)
    if not (data / 'PG_VERSION').exists():
        cmd([str(PG/'initdb.exe'), '-D', str(data), '-U', 'dsu_gui', '-A', 'trust', '--encoding=UTF8', '--locale=C'])
    pp, ap, wp = port(), port(), port()
    cmd([str(PG/'pg_ctl.exe'), '-D', str(data), '-l', str(RUN/'postgres.log'), '-w', 'start', '-o', f'-h 127.0.0.1 -p {pp}'])
    children, logs = [], []
    env = os.environ.copy()
    env.update(DATABASE_URL=f'postgresql://dsu_gui@127.0.0.1:{pp}/postgres',
        SECRET_KEY='qa-local-aislada-sin-valor-productivo', DEBUG='False', SECURE_SSL_REDIRECT='False',
        MODELOS_DIR=str(RUN/'modelos'), PYTHONIOENCODING='utf8', PYTHONUNBUFFERED='1',
        DSU_API_PROXY=f'http://127.0.0.1:{ap}', VITE_API_URL='', JWT_ACCESS_MINUTES='1')
    try:
        cmd([sys.executable, 'manage.py', 'migrate', '--noinput'], cwd=BACK, env=env)
        if not (RUN/'preparado').exists():
            cmd([sys.executable, 'manage.py', 'seed', '--demo', '--historico', '--admin-password', env['DSU_GUI_PASSWORD']], cwd=BACK, env=env)
            # Solo fixture: las cinco cuentas en la BD nueva mantienen sus roles documentados.
            code = "from django.contrib.auth import get_user_model; from django.contrib.auth.models import Group; import os; U=get_user_model(); u,created=U.objects.get_or_create(username='administrativo',defaults={'first_name':'Administración','last_name':'QA'}); u.groups.add(Group.objects.get(name='Administrador')); u.set_password(os.environ['DSU_GUI_PASSWORD']) if created else None; u.save() if created else None"
            cmd([sys.executable, 'manage.py', 'shell', '-c', code], cwd=BACK, env=env)
            (RUN/'preparado').touch()
        for name,args,cwd in [
            ('backend',[sys.executable,'manage.py','runserver',f'127.0.0.1:{ap}','--noreload'],BACK),
            ('frontend',['node','node_modules/vite/bin/vite.js','--host','127.0.0.1','--port',str(wp)],ROOT/'gestion-residuos-dsu/frontend')]:
            log=(RUN/(name+'.log')).open('a',encoding='utf8'); logs.append(log)
            children.append(subprocess.Popen(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,**FLAGS))
            for _ in range(120):
                try:
                    urllib.request.urlopen(f'http://127.0.0.1:{ap}/api/' if name=='backend' else f'http://127.0.0.1:{wp}/',timeout=1).close(); break
                except urllib.error.HTTPError as e:
                    if name=='backend' and e.code==401: break
                except Exception: time.sleep(.25)
            else: raise RuntimeError('Servicio no disponible: '+name)
        metadata=dict(inicio_utc=dt.datetime.now(dt.timezone.utc).isoformat(),web=f'http://127.0.0.1:{wp}',api=f'http://127.0.0.1:{ap}',pg_port=pp,pids=[p.pid for p in children],
            commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),cambios_locales=True,datos='Sintéticos; PostgreSQL 18 propio, usuario dsu_gui, loopback',jwt_access_minutes=1)
        (RUN/'servicios.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
        print('Servicios GUI aislados listos. '+metadata['web'],flush=True)
        while not stop.exists(): time.sleep(1)
    finally:
        for child in reversed(children): subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],capture_output=True,**FLAGS)
        for log in logs: log.close()
        cmd([str(PG/'pg_ctl.exe'),'-D',str(data),'-w','stop','-m','fast'])

if __name__=='__main__': main()
