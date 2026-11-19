"""Login real y pantallas contra API y PostgreSQL sintéticos. No usa tokens productivos."""
import datetime as dt
import json
from pathlib import Path
import sys
import time
import uuid
import subprocess
import os

from playwright.sync_api import sync_playwright

base = sys.argv[1]
assert base.startswith('http://127.0.0.1:')
out = Path(__file__).resolve().parent / '05_ejecuciones_pruebas/demo_ui'
out.mkdir(parents=True,exist_ok=True)
resultados=[]
flujo=[]
demo={}
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,channel='chrome')
    for user,rutas in [('admin',['usuarios','parametros','procesos','modelo','bitacora']),
                       ('supervisor',['jornadas','historico','incidencias','tablero','mapa','reportes','predicciones','recomendaciones']),
                       ('operario1',['campo']),('directivo',['tablero','usuarios'])]:
        context=browser.new_context(viewport={'width':1440,'height':900})
        page=context.new_page();errores=[]
        page.on('pageerror',lambda e:errores.append(str(e)))
        page.goto(base)
        page.get_by_label('Usuario',exact=True).fill(user)
        page.get_by_label('Contraseña',exact=True).fill('Prueba.Aislada.2026' if user=='admin' else 'Residuos.2026')
        page.get_by_role('button',name='Ingresar',exact=True).click()
        page.wait_for_url('**/'+('campo' if user=='operario1' else 'tablero' if user=='directivo' else 'jornadas'),timeout=45000)
        token=page.evaluate("JSON.parse(localStorage.getItem('dsu.sesion')).access")
        def api(path, data=None, permiso=None):
            response=context.request.fetch(base+'api/'+path,method='POST' if data is not None else 'GET',
                headers={'Authorization':'Bearer '+(permiso or token)},data=data)
            assert response.ok,(path,response.status,response.text()[:300])
            flujo.append({'usuario':user,'ruta_api':path,'http':response.status})
            return response
        if user=='admin':
            demo['admin_token']=token
            users=api('usuarios/').json()['results']
            supervisor=next(u['id'] for u in users if u['username']=='supervisor')
            code='QA'+uuid.uuid4().hex[:6]
            demo['operario']='oper_'+code.lower()
            demo['op']=api('usuarios/',{'username':demo['operario'],'first_name':'Operario','last_name':'Sintético',
                'password':'Residuos.2026','roles':['Operativo']}).json()['id']
            demo['sector']=api('sectores/',{'codigo':code,'nombre':'Sector sintético de cierre','supervisor':supervisor}).json()['id']
            demo['puntos']=[api('puntos/',{'codigo':code+str(i),'nombre':'Punto sintético '+str(i),'sector':demo['sector'],
                'latitud':'-17.775700','longitud':'-63.195600','capacidad_kg':'100'}).json()['id'] for i in range(2)]
        if user=='supervisor':
            hoy=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(hours=4)).date().isoformat()
            j=api('jornadas/',{'fecha':hoy,'turno':'TARDE','sector':demo['sector'],'puntos':demo['puntos']}).json()['id']
            api('jornadas/%s/asignar/'%j,{'personal':[demo['op']],'responsable':demo['op']})
            api('jornadas/%s/confirmar/'%j,{})
            api('jornadas/%s/abrir/'%j,{})
            tipo=api('tipos-residuo/').json()['results'][0]['id']
            api('jornadas/%s/visitas/'%j,{'punto':demo['puntos'][0],'detalles':[{'tipo_residuo':tipo,'cantidad':'1'}]})
            api('jornadas/%s/omitir/'%j,{'punto':demo['puntos'][1],'motivo':'Ensayo sintético'})
            api('jornadas/%s/cerrar/'%j,{})
            api('etl/ejecutar/',{},demo['admin_token'])
            for _ in range(100):
                estado=api('etl/',permiso=demo['admin_token']).json()['results'][0]['estado']
                if estado!='EN_CURSO':break
                time.sleep(.2)
            assert estado in ['EXITOSA','CON_ALERTA','SIN_CAMBIOS'],estado
            api('predicciones/',{'horizonte':7})
            for fmt,firma in [('pdf',b'%PDF'),('xlsx',b'PK')]:
                assert api('reportes/generacion-sector/?formato='+fmt).body().startswith(firma)
            carga=api('jornadas/',{'fecha':hoy,'turno':'NOCHE','sector':demo['sector'],'puntos':demo['puntos']}).json()['id']
            api('jornadas/%s/asignar/'%carga,{'personal':[demo['op']],'responsable':demo['op']})
            api('jornadas/%s/confirmar/'%carga,{})
            api('jornadas/%s/abrir/'%carga,{})
            script=Path(__file__).resolve().parent.parent/'gestion-residuos-dsu/backend/scripts/carga.py'
            run=subprocess.run([sys.executable,str(script),'--url',base.rstrip('/'),'--usuarios','12','--segundos','60',
                '--usuario','supervisor','--clave','Residuos.2026','--jornada',str(carga),
                '--operario',demo['operario'],'--clave-operario','Residuos.2026'],capture_output=True,text=True,encoding='utf8',
                creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            (out.parent/'carga_12_usuarios.txt').write_text(run.stdout+run.stderr,encoding='utf8')
            assert run.returncode==0,run.stdout[-1500:]+run.stderr[-1000:]
        for ruta in rutas:
            page.goto(base+ruta,wait_until='networkidle')
            page.locator('main').wait_for(timeout=45000)
            assert not page.get_by_role('button',name='Ingresar',exact=True).count()
            if user=='directivo' and ruta=='usuarios':
                assert page.get_by_text('Sin acceso',exact=True).count()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
            page.screenshot(path=str(out/(user+'-'+ruta+'.png')),full_page=True)
            resultados.append({'usuario':user,'ruta':ruta,'resultado':'APROBADO'})
        assert not errores,errores
        context.close()
    browser.close()
(out/'resultados.json').write_text(json.dumps({'fecha_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'entorno':'Chrome headless contra PostgreSQL sintético y API/Vite locales', 'casos':resultados,'flujo_integrado_api':flujo},ensure_ascii=False,indent=2),encoding='utf8')
print('Login y %s pantallas aprobadas.' %len(resultados))
