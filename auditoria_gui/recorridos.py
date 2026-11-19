"""Playwright visible: toda escritura del producto se hace con controles del DOM.

Credencial exclusivamente en DSU_GUI_PASSWORD. Estados JWT en runtime excluido.
No usa page.request, fetch, llamadas API ni ORM para ejecutar los recorridos.
"""
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import time
from playwright.sync_api import sync_playwright, expect

OUT = Path(__file__).resolve().parent
RUN = OUT/'runtime'
BASE = json.loads((RUN/'servicios.json').read_text(encoding='utf8'))['web']
PASS = os.environ['DSU_GUI_PASSWORD']
ROLES = ['supervisor','operario1','operario2','directivo','administrativo']
PHASE = sys.argv[1]
STAMP = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
RESULTS, LOGS, DOM = [], [], []
CURRENT = ''
for d in ['capturas','resultados','inventario_dom','descargas','videos']: (OUT/d).mkdir(exist_ok=True)

def clean(s):
    return str(s).replace(PASS,'[OMITIDO]')

def inventory(p, role):
    if p.is_closed(): return
    controls=p.locator('main button, main a, main input, main select, main textarea, nav a').evaluate_all("els=>els.map(e=>({tag:e.tagName,tipo:e.type||'',texto:(e.tagName==='INPUT'?'':e.textContent||'').trim().slice(0,250),aria:e.getAttribute('aria-label'),placeholder:e.getAttribute('placeholder'),disabled:e.disabled||false,href:e.tagName==='A'?e.getAttribute('href'):null}))")
    DOM.append(dict(rol=role,ruta=p.url.replace(BASE,''),controles=controls))

def shot(p, name):
    # Nunca capturar el valor visible de un campo de contraseña.
    path=OUT/'capturas'/(PHASE+'-'+STAMP+'-'+name+'.png')
    p.screenshot(path=str(path),full_page=True)
    return str(path.relative_to(OUT))

def case(id, title, role, p, fn, cu=None):
    global CURRENT
    CURRENT=id
    start=time.monotonic()
    row=dict(id=id,titulo=title,rol=role,cu=cu or [],inicio_utc=dt.datetime.now(dt.timezone.utc).isoformat(),interfaz=True)
    try:
        detail=fn()
        row.update(estado='APROBADO',detalle=json.loads(clean(json.dumps(detail,ensure_ascii=False))) if isinstance(detail,(dict,list)) else clean(detail or 'Aserciones de interfaz satisfechas'))
    except Exception as e:
        row.update(estado='FALLIDO',detalle=clean(str(e) or repr(e))[:2400])
    try:
        row['evidencia']=shot(p,id)
        inventory(p,role)
    except Exception as e: row['error_evidencia']=clean(e)[:200]
    row['segundos']=round(time.monotonic()-start,2)
    RESULTS.append(row)
    save()
    print(id,row['estado'],str(row['detalle'])[:160],flush=True)
    return row['estado']=='APROBADO'

def save():
    (OUT/'resultados'/f'{PHASE}-{STAMP}.json').write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'inventario_dom'/f'{PHASE}-{STAMP}.json').write_text(json.dumps(DOM,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'resultados'/f'consola-{PHASE}-{STAMP}.json').write_text(json.dumps(LOGS,ensure_ascii=False,indent=2),encoding='utf8')

def goto(p, path):
    p.goto(BASE+path,wait_until='domcontentloaded')
    expect(p.locator('main')).to_be_visible()

def click(p, text, exact=True):
    p.get_by_role('button',name=text,exact=exact).click()
    p.wait_for_timeout(250)

def field(p, text): return p.get_by_label(re.compile('^'+re.escape(text)))
def fill(p, text, value): field(p,text).fill(str(value))
def select(p, text, label): field(p,text).select_option(label=label)
def choose_prefix(p,label,prefix):
    option=field(p,label).locator('option').filter(has_text=re.compile('^'+re.escape(prefix)+' ·')).first
    option.wait_for(state='attached');field(p,label).select_option(label=option.text_content())

def visible(p,text): expect(p.get_by_text(text,exact=False).first).to_be_visible()

def login(p, role):
    p.goto(BASE,wait_until='domcontentloaded')
    if p.get_by_label('Usuario',exact=True).count():
        p.get_by_label('Usuario',exact=True).fill(role)
        p.get_by_label('Contraseña',exact=True).fill(PASS)
        click(p,'Ingresar')
        expect(p.locator('main')).to_be_visible(timeout=15000)

def context(browser, role, reuse=True, viewport=None):
    state=RUN/(role+'.json')
    kw=dict(viewport=viewport or {'width':1440,'height':1000},record_video_dir=str(OUT/'videos'/PHASE),record_video_size={'width':1280,'height':800},accept_downloads=True)
    if reuse and state.exists():kw['storage_state']=str(state)
    ctx=browser.new_context(**kw)
    ctx.add_init_script("document.addEventListener('click',e=>{const t=e.target.closest('button,a');if(t)console.debug('__QA_CLICK__'+JSON.stringify({ruta:location.pathname,texto:(t.getAttribute('aria-label')||t.textContent||'').trim().slice(0,180),tipo:t.getAttribute('role')||t.tagName}));},true)")
    p=ctx.new_page(); p.set_default_timeout(10000); p.set_default_navigation_timeout(30000)
    p.on('pageerror',lambda e: LOGS.append(dict(rol=role,tipo='pageerror',mensaje=clean(e))))
    p.on('console',lambda e: LOGS.append(dict(rol=role,caso=CURRENT,tipo=e.type,mensaje=clean(e.text)[:600])) if e.type in ['error','warning'] or e.text.startswith('__QA_CLICK__') else None)
    p.on('response',lambda r: LOGS.append(dict(rol=role,tipo='http',estado=r.status,ruta=r.url.split('?')[0].replace(BASE,''))) if r.status>=400 else None)
    return ctx,p

def auth(browser):
    for role in ROLES:
        ctx,p=context(browser,role,False)
        def good():
            login(p,role)
            assert '/'+('campo' if role.startswith('operario') else 'tablero' if role=='directivo' else 'jornadas') in p.url
            return 'Inicio correcto y pantalla inicial del rol'
        if case('AUTH-'+role,'Ingreso y navegación de '+role,role,p,good,[1]):
            nav=p.locator('nav[aria-label="Principal"] a').evaluate_all('es=>es.map(e=>({ruta:e.getAttribute("href"),nombre:e.textContent.trim()}))')
            (OUT/'resultados'/('menu-'+role+'.json')).write_text(json.dumps(nav,ensure_ascii=False,indent=2),encoding='utf8')
            routes=json.loads((OUT/'pantallas.json').read_text(encoding='utf8'))
            allowed={x['ruta'] for x in nav}
            for r in routes:
                path=r['ruta']
                if ':id' in path: continue
                def route(path=path):
                    goto(p,path)
                    denied=path not in allowed and path!='/jornadas/nueva'
                    if path=='/jornadas/nueva':denied=role not in ['supervisor','administrativo']
                    if denied:visible(p,'Sin acceso')
                    else:
                        assert p.get_by_text('Sin acceso',exact=True).count()==0
                        assert p.get_by_text('Esta pantalla tuvo un problema',exact=False).count()==0
                    return ('Rechazado por rol' if denied else 'Pantalla autorizada cargada')+'; acceso URL directa'
                case('ROUTE-'+role+'-'+path.strip('/').replace('/','-'),'Acceso directo '+path,role,p,route)
            def persist():
                p.reload(wait_until='domcontentloaded');expect(p.locator('main')).to_be_visible()
                assert p.get_by_label('Usuario',exact=True).count()==0
            case('AUTH-reload-'+role,'Sesión persiste al recargar',role,p,persist,[1])
            ctx.storage_state(path=str(RUN/(role+'.json')))
            def logout():
                click(p,'Cerrar sesión')
                expect(p.get_by_label('Usuario',exact=True)).to_be_visible()
                p.go_back(wait_until='domcontentloaded')
                expect(p.get_by_label('Usuario',exact=True)).to_be_visible()
                assert not p.evaluate("Boolean(localStorage.getItem('dsu.sesion'))")
            case('AUTH-logout-'+role,'Logout, almacenamiento vacío y Atrás protegido',role,p,logout,[2])
        ctx.close()
    ctx,p=context(browser,'negativo',False)
    def bad():
        p.goto(BASE,wait_until='domcontentloaded')
        expect(p.get_by_role('button',name='Ingresar',exact=True)).to_be_disabled()
        expect(p.get_by_label('Usuario',exact=True)).to_be_visible()
        p.get_by_label('Usuario',exact=True).fill('qa_inexistente')
        p.get_by_label('Contraseña',exact=True).fill('incorrecta')
        click(p,'Ingresar');visible(p,'incorrectos')
        p.get_by_label('Contraseña',exact=True).clear()
    case('AUTH-invalid','Campos vacíos y credenciales incorrectas','anónimo',p,bad,[1])
    ctx.close()

def catalogs(browser):
    role=os.environ.get('DSU_GUI_CATALOG_ROLE','administrativo')
    ctx,p=context(browser,role,False)
    login(p,role)
    suffix=STAMP[-6:]
    fixtures={}
    def enter(path,tab=None):
        goto(p,path)
        if tab:p.get_by_role('tab',name=tab,exact=True).click();p.wait_for_timeout(300)
    def write(values):
        for k,v in values.items():
            loc=field(p,k)
            if isinstance(v,tuple):loc.select_option(label=v[0])
            elif isinstance(v,bool):loc.set_checked(v)
            else:loc.fill(str(v))
    specs=[
        ('sector','/sectores',None,{'Código':'QA'+suffix,'Nombre':'Sector GUI '+suffix,'Tipo':('Facultad',),'Supervisor responsable':('Sara Supervisora',),'Descripción':'Sector sintético GUI'},'Nombre','Sector GUI editado '+suffix,5),
        ('unidad','/tipos-residuo','Unidades de medida',{'Nombre':'Unidad GUI '+suffix,'Símbolo':'q'+suffix,'Magnitud':('Peso (base kg)',),'Factor de conversión a la base':'0.001'},'Nombre','Unidad GUI editada '+suffix,8),
        ('tipo','/tipos-residuo','Tipos de residuo',{'Nombre':'Residuo GUI '+suffix,'Clasificación':('Reciclable',),'Es aprovechable':True,'Unidad de medida':('Kilogramo (kg)',),'Descripción':'Prueba ñ á < > &'},'Descripción','Descripción GUI modificada',8),
        ('vehiculo','/vehiculos',None,{'Placa':'Q'+suffix,'Descripción':'Vehículo GUI '+suffix,'Capacidad (kg)':'100.25','Condición':('Operativo',)},'Descripción','Vehículo GUI editado '+suffix,13),
        ('periodo','/tipos-residuo','Periodos académicos',{'Nombre':'QA-'+suffix,'Inicio':str(2030+int(suffix)%1000)+'-01-01','Fin':str(2030+int(suffix)%1000)+'-06-30'},'Nombre','QA-editado-'+suffix,31),
        ('punto','/puntos',None,{'Sector':('QA'+suffix+' · Sector GUI editado '+suffix,),'Código':'PQA'+suffix,'Nombre o referencia corta':'Punto GUI '+suffix,'Cómo llegar':'Ingreso de pruebas','Latitud':'-17.78','Longitud':'-63.19','Capacidad estimada (kg)':'120.25','Condición operativa':('Operativo',)},'Nombre o referencia corta','Punto GUI editado '+suffix,6),
        ('contenedor','/contenedores',None,{'Punto de recolección':('PQA'+suffix+' · Punto GUI editado '+suffix,),'Código':'CQA'+suffix,'Tipo de contenedor':'Turril QA','Capacidad (L)':'200.25','Fecha de instalación':'2026-11-19','Estado':('Bueno',),'Observación':'Sintético GUI'},'Observación','Contenedor inspeccionado GUI',7),
        ('usuario','/usuarios',None,{'Nombre de usuario':'qa_gui_'+suffix,'Nombres':'Persona QA','Apellidos':'Sintética','Correo':'qa@example.invalid','Teléfono':'12345','Operativo':True,'Contraseña':PASS},'Apellidos','Actualizada QA',3),
    ]
    if role=='supervisor':
        specs=[x for x in specs if x[0] in ['punto','contenedor','vehiculo']]
        next(x for x in specs if x[0]=='punto')[3]['Sector']=('FICCT · Facultad de Ciencias de la Computación y Telecomunicaciones',)
        def scope():
            goto(p,'/sectores');visible(p,'FICCT');assert p.get_by_role('button',name='Nuevo',exact=True).count()==0
            return 'Supervisor consulta sus sectores; crear sectores se reserva a Administrador, según permisos vigentes'
        case('SUP-sectores','Consulta territorial y ausencia de alta no autorizada',role,p,scope,[5])
    for entity,path,tab,values,editk,editv,cu in specs:
        def flow(entity=entity,path=path,tab=tab,values=values,editk=editk,editv=editv):
            enter(path,tab);click(p,'Nuevo')
            inventory(p,role)
            click(p,'Guardar')
            expect(p.get_by_role('heading',name='Nuevo registro')).to_be_visible()
            write(values);click(p,'Guardar')
            visible(p,'Cambios guardados')
            key=values.get('Código',values.get('Placa',values.get('Nombre de usuario',values.get('Símbolo',values.get('Nombre')))))
            if p.get_by_label('Buscar',exact=True).count():
                p.get_by_label('Buscar',exact=True).fill(key);p.wait_for_timeout(500)
            row=p.locator('tbody tr').filter(has_text=key).first
            expect(row).to_be_visible();row.get_by_role('button',name='Editar',exact=True).click()
            write({editk:editv});click(p,'Guardar');visible(p,'Cambios guardados')
            if key==values.get(editk):key=editv
            p.reload(wait_until='domcontentloaded')
            if tab:p.get_by_role('tab',name=tab,exact=True).click();p.wait_for_timeout(300)
            if p.get_by_label('Buscar',exact=True).count():p.get_by_label('Buscar',exact=True).fill(key);p.wait_for_timeout(350)
            row=p.locator('tbody tr').filter(has_text=key).first
            expect(row).to_be_visible()
            if entity=='periodo':
                fixtures[entity]=dict(key=key,values=values)
                return 'Vacíos rechazados; alta, edición y persistencia. Periodo no ofrece baja lógica en la interfaz.'
            if entity=='contenedor':
                for state in ['De baja','Bueno']:
                    row=p.locator('tbody tr').filter(has_text=key).first
                    row.get_by_role('button',name='Editar',exact=True).click();select(p,'Estado',state);click(p,'Guardar');visible(p,'Cambios guardados')
                    p.reload(wait_until='domcontentloaded');expect(p.locator('tbody tr').filter(has_text=key).first).to_be_visible()
                fixtures[entity]=dict(key=key,values=values)
                return 'Alta, edición, búsqueda; estados De baja y Bueno persistidos. No tiene is_active.'
            if entity=='punto':p.once('dialog',lambda d:d.accept('Baja sintética QA'))
            row.get_by_role('button',name='Desactivar',exact=True).click();visible(p,'Registro desactivado')
            if p.get_by_label('Estado',exact=True).count():p.get_by_label('Estado',exact=True).select_option(label='Inactivos');p.wait_for_timeout(400)
            row=p.locator('tbody tr').filter(has_text=key).first
            row.get_by_role('button',name='Activar',exact=True).click();visible(p,'Registro reactivado')
            enter(path,tab)
            if p.get_by_label('Buscar',exact=True).count():p.get_by_label('Buscar',exact=True).fill(key);p.wait_for_timeout(350)
            expect(p.locator('tbody tr').filter(has_text=key).first).to_be_visible()
            fixtures[entity]=dict(key=key,values={k:v for k,v in values.items() if k!='Contraseña'})
            return 'Vacíos rechazados; alta, edición, búsqueda, baja lógica, reactivación y persistencia tras recarga'
        case('CRUD-'+entity,'Formulario y ciclo CRUD '+entity,role,p,flow,[cu])
    (RUN/('fixtures_gui.json' if role=='administrativo' else 'fixtures_gui_supervisor.json')).write_text(json.dumps(fixtures,ensure_ascii=False,indent=2),encoding='utf8')
    # Límites y duplicados se comprueban mediante el formulario, sin peticiones directas.
    for entity,path,tab,values,editk,editv,cu in specs:
        if entity not in fixtures:continue
        def duplicate(path=path,tab=tab,values=values):
            enter(path,tab);click(p,'Nuevo');write(values);click(p,'Guardar')
            expect(p.get_by_role('heading',name='Nuevo registro')).to_be_visible()
            assert p.get_by_text('Cambios guardados',exact=False).count()==0
            if tab!='Periodos académicos':visible(p,'existe')
        case('DUP-'+entity,'Duplicado rechazado '+entity,role,p,duplicate,[cu])
    ctx.storage_state(path=str(RUN/(role+'.json')));ctx.close()

def auth_extra(browser):
    ctx,p=context(browser,'administrativo',False);login(p,'administrativo')
    def route():
        goto(p,'/jornadas/nueva');visible(p,'Guardar planificación')
        assert p.get_by_text('Sin acceso',exact=True).count()==0
        return 'Corrección del oráculo de prueba: Administrador tiene operations.add_jornada; no es un defecto del producto'
    case('ROUTE-administrativo-jornadas-nueva','Planificación autorizada para Administrador','administrativo',p,route)
    def refresh():
        old=p.evaluate("JSON.parse(localStorage.getItem('dsu.sesion')).access")
        p.wait_for_timeout(65000)
        goto(p,'/usuarios')
        visible(p,'Usuarios')
        assert old!=p.evaluate("JSON.parse(localStorage.getItem('dsu.sesion')).access")
        return 'Tras 65 s, access JWT de 1 minuto renovado automáticamente; pantalla conserva autenticación'
    case('AUTH-refresh','Expiración real y renovación de sesión','administrativo',p,refresh,[1])
    def expired():
        p.evaluate("localStorage.setItem('dsu.sesion',JSON.stringify({access:'expirado-qa',refresh:'invalido-qa'}))")
        p.reload(wait_until='domcontentloaded');expect(p.get_by_label('Usuario',exact=True)).to_be_visible()
        return 'Inyección local de sesión inválida: regreso a ingreso, sin datos protegidos'
    case('AUTH-expired','Sesión no renovable vuelve al ingreso','administrativo',p,expired,[1,2])
    def bad():
        expect(p.get_by_role('button',name='Ingresar',exact=True)).to_be_disabled()
        p.get_by_label('Usuario',exact=True).fill('qa_inexistente')
        p.get_by_label('Contraseña',exact=True).fill('incorrecta')
        click(p,'Ingresar');visible(p,'incorrectos');p.get_by_label('Contraseña',exact=True).clear()
    case('AUTH-invalid','Campos vacíos bloqueados y credenciales incorrectas rechazadas','anónimo',p,bad,[1])
    ctx.close()

def auth_negative(browser):
    ctx,p=context(browser,'anónimo',False)
    def bad():
        p.goto(BASE,wait_until='domcontentloaded')
        expect(p.get_by_role('button',name='Ingresar',exact=True)).to_be_disabled()
        p.get_by_label('Usuario',exact=True).fill('qa_inexistente')
        p.get_by_label('Contraseña',exact=True).fill('incorrecta')
        click(p,'Ingresar');visible(p,'incorrectos');p.get_by_label('Contraseña',exact=True).clear()
    case('AUTH-invalid','Vacíos bloqueados e ingreso incorrecto rechazado','anónimo',p,bad,[1]);ctx.close()

def analytics(browser):
    ca,a=context(browser,'administrativo',False);login(a,'administrativo')
    for n in [1,2]:
        def etl(n=n):
            goto(a,'/procesos');click(a,'Ejecutar ahora');visible(a,'Proceso iniciado')
            expect(a.get_by_role('button',name='Ejecutar ahora',exact=True)).to_be_enabled(timeout=180000)
            row=a.locator('tbody tr').first
            text=row.inner_text()
            assert 'Fallida' not in text and 'En curso' not in text
            if n==2:
                expect(row).to_contain_text('Sin registros nuevos',timeout=20000)
                text=row.inner_text()
            a.reload(wait_until='domcontentloaded');expect(a.locator('tbody tr').first).to_have_text(re.compile(re.escape(text)),use_inner_text=True)
            return 'Ejecución '+str(n)+': '+text
        case('ETL-'+str(n),'ETL desde UI y reintento incremental','administrativo',a,etl,[20])
    ca.close()
    cd,p=context(browser,'directivo',False);login(p,'directivo')
    def dashboard():
        goto(p,'/tablero');visible(p,'Total recolectado')
        field(p,'Desde').fill('2026-10-01');field(p,'Hasta').fill('2026-11-19')
        select(p,'Sector',next(x for x in field(p,'Sector').locator('option').all_text_contents() if x.startswith('FICCT ·')))
        select(p,'Tipo de residuo','Orgánico');p.wait_for_timeout(500)
        visible(p,'Por sector');click(p,'Restablecer filtros')
        return 'Indicadores con combinación fecha/sector/tipo y restablecimiento'
    case('A-tablero','Indicadores y filtros del directivo','directivo',p,dashboard,[21])
    def compare():
        goto(p,'/tablero');p.get_by_role('tab',name='Comparar periodos',exact=True).click()
        p.get_by_label('Desde',exact=True).nth(0).fill('2026-09-01');p.get_by_label('Hasta',exact=True).nth(0).fill('2026-09-30')
        p.get_by_label('Desde',exact=True).nth(1).fill('2026-10-01');p.get_by_label('Hasta',exact=True).nth(1).fill('2026-10-31')
        for label in ['Sector','Punto','Tipo de residuo']:
            select(p,'Comparar por',label);expect(p.locator('tbody tr').first).to_be_visible();inventory(p,'directivo')
        return 'Comparación septiembre/octubre: sector, punto y tipo con tablas no vacías'
    case('A-comparar','Comparación y tendencias','directivo',p,compare,[22])
    def power():
        goto(p,'/tablero');p.get_by_role('tab',name='Power BI',exact=True).click();visible(p,'El informe de Power BI aún no está publicado')
        assert p.locator('iframe').count()==0
        return 'Ausencia de configuración informada; informe remoto no comprobado'
    case('A-powerbi','Power BI sin configuración responde correctamente','directivo',p,power,[21])
    def maptest():
        goto(p,'/mapa');expect(p.locator('.leaflet-container')).to_be_visible()
        p.get_by_role('radio',name='Marcadores',exact=True).click()
        markers=p.locator('path.leaflet-interactive');expect(markers.first).to_be_visible();markers.first.click(force=True)
        expect(p.locator('.leaflet-popup')).to_be_visible();shot(p,'A-popup-mapa')
        p.get_by_role('radio',name='Mapa de calor',exact=True).click()
        expect(p.locator('canvas.leaflet-heatmap-layer')).to_be_visible()
        select(p,'Sector',next(x for x in field(p,'Sector').locator('option').all_text_contents() if x.startswith('FICCT ·')))
        select(p,'Tipo de residuo','Orgánico');p.wait_for_timeout(500)
        expect(p.locator('path.leaflet-interactive')).to_have_count(3)
        click(p,'Restablecer filtros')
        return 'Marcadores, popup, mapa de calor, filtros combinados y restablecimiento'
    case('A-mapa','Mapa interactivo observado','directivo',p,maptest,[23,24,25])
    for kind in ['Generación por sector','Generación por tipo de residuo','Cumplimiento de jornadas','Incidencias registradas','Indicadores del periodo','Generación proyectada']:
        def report(kind=kind):
            goto(p,'/reportes');p.get_by_role('radio',name=re.compile('^'+re.escape(kind))).click()
            if kind!='Generación proyectada':fill(p,'Desde','2026-10-01');fill(p,'Hasta','2026-11-19')
            expect(p.get_by_role('button',name='Excel',exact=True)).to_be_enabled()
            p.wait_for_timeout(500)
            rows=p.locator('main tbody tr').evaluate_all("es=>es.map(e=>Array.from(e.querySelectorAll('td')).map(c=>c.textContent.trim()))")
            downloaded=[]
            for label,ext in [('Excel','xlsx'),('PDF','pdf')]:
                with p.expect_download() as event:click(p,label)
                target=OUT/'descargas'/(re.sub(r'[^a-zA-Z0-9]+','-',kind)+'-'+STAMP+'.'+ext)
                event.value.save_as(str(target));assert target.stat().st_size>300
                assert target.read_bytes().startswith(b'%PDF' if ext=='pdf' else b'PK')
                downloaded.append(str(target.relative_to(OUT)))
            return dict(filas_ui=rows,archivos=downloaded,limite='Correspondencia de celdas se verifica por separado sobre los archivos descargados')
        case('REP-'+re.sub(r'[^a-zA-Z0-9]+','-',kind),'Vista y descarga Excel/PDF: '+kind,'directivo',p,report,[33,34])
    cd.close()

def race(browser):
    ctx,p=context(browser,'directivo',False);login(p,'directivo')
    def late():
        held=[]
        ctx.route('**/api/reportes/generacion-sector/**',lambda r:held.append(r))
        goto(p,'/reportes');p.get_by_role('radio',name=re.compile('^Generación proyectada')).click()
        expect(p.get_by_role('heading',name='Generación proyectada por punto',exact=True)).to_be_visible()
        assert held,'No se retuvo la petición anterior'
        for route in list(held):route.continue_()
        p.wait_for_timeout(1500)
        expect(p.get_by_role('heading',name='Generación proyectada por punto',exact=True)).to_be_visible()
        assert p.get_by_role('heading',name='Generación por sector',exact=True).count()==0
        return 'Respuesta anterior liberada después de la nueva; no reemplaza la selección actual'
    case('RACE-reportes','Respuesta atrasada no mezcla tipos de reporte','directivo',p,late,[33,34])
    ctx.close()

def etl_repeat(browser):
    ctx,p=context(browser,'administrativo',False);login(p,'administrativo')
    def repeat():
        goto(p,'/procesos');click(p,'Ejecutar ahora')
        expect(p.locator('tbody tr').first).to_contain_text('Sin registros nuevos',timeout=30000)
        p.reload(wait_until='domcontentloaded');expect(p.locator('tbody tr').first).to_contain_text('Sin registros nuevos')
        return 'Ejecución incremental repetida sin datos nuevos: cero registros, sin duplicación'
    case('ETL-2','Repetición sin registros nuevos','administrativo',p,repeat,[20]);ctx.close()

def etl_concurrent(browser):
    c1,a=context(browser,'administrativo',False);login(a,'administrativo')
    c2,b=context(browser,'administrativo',False);login(b,'administrativo')
    def execute():
        goto(a,'/procesos');goto(b,'/procesos')
        a.get_by_role('button',name='Ejecutar ahora',exact=True).click(no_wait_after=True)
        b.get_by_role('button',name='Ejecutar ahora',exact=True).click(no_wait_after=True)
        visible(a,'Proceso iniciado');visible(b,'curso')
        shot(b,'ETL-segunda-sesion')
        expect(a.get_by_role('button',name='Ejecutar ahora',exact=True)).to_be_enabled(timeout=120000)
        a.reload(wait_until='domcontentloaded')
        row=a.locator('tbody tr').first
        expect(row).to_contain_text('1999',timeout=15000)
        assert '2000' in row.inner_text()
        return 'Dos sesiones gráficas; 2000 entradas de fixture procesadas, 1999 duplicados; segundo inicio bloqueado en curso'
    case('ETL-concurrencia-duplicados','ETL concurrente y duplicados visibles','administrativo',a,execute,[20])
    c2.close();c1.close()

def prediction_negative(browser):
    ca,a=context(browser,'administrativo',False);login(a,'administrativo')
    def nomodel():
        goto(a,'/predicciones');click(a,'Generar predicción');visible(a,'modelo vigente')
        return 'Solicitud sin modelo vigente rechazada mediante mensaje de interfaz'
    case('ML-sin-modelo','Inferencia sin modelo disponible','administrativo',a,nomodel,[28])
    for label,value,expected in [('Registros mínimos para entrenar','999999','se necesitan al menos'),('R² mínimo para publicar','1','umbral')]:
        def rejected(label=label,value=value,expected=expected):
            goto(a,'/parametros');old=field(a,label).input_value();fill(a,label,value);click(a,'Guardar parámetros');visible(a,'Parámetros guardados')
            try:
                goto(a,'/modelo');click(a,'Entrenar');visible(a,'Entrenamiento iniciado')
                expect(a.get_by_role('button',name='Entrenar',exact=True)).to_be_enabled(timeout=240000)
                a.reload(wait_until='domcontentloaded');expect(a.locator('tbody tr').first).to_contain_text('RECHAZADO')
                a.locator('tbody tr').first.click();visible(a,expected)
                assert a.get_by_role('button',name='Publicar esta versión',exact=True).count()==0
                shot(a,'ML-rechazo-'+value)
            finally:
                goto(a,'/parametros');fill(a,label,old);click(a,'Guardar parámetros');visible(a,'Parámetros guardados')
            return 'Rechazo comprobado; parámetro original restituido por UI'
        case('ML-rechazo-'+value,'Modelo rechazado con '+label,'administrativo',a,rejected,[26])
    def hyper():
        goto(a,'/modelo');fill(a,'Número de árboles','9');click(a,'Entrenar')
        assert not field(a,'Número de árboles').evaluate('(e)=>e.checkValidity()')
        fill(a,'Número de árboles','501');click(a,'Entrenar');assert not field(a,'Número de árboles').evaluate('(e)=>e.checkValidity()')
        return 'Límites n_estimators 9/501 bloqueados por validación nativa (rango 10..500)'
    case('ML-hiper-limites','Hiperparámetros fuera de rango','administrativo',a,hyper,[26]);ca.close()

def model_absent(browser):
    ctx,p=context(browser,'administrativo',False);login(p,'administrativo')
    def missing():
        goto(p,'/predicciones');click(p,'Generar predicción');visible(p,'No existe un modelo publicado vigente')
        return 'Fixture reversible sin vigente; inferencia solicitada con formulario rechazada con indicación para entrenar/publicar'
    case('ML-sin-modelo','Inferencia con fixture sin modelo vigente','administrativo',p,missing,[28]);ctx.close()

def model_concurrent(browser):
    c1,a=context(browser,'administrativo',False);login(a,'administrativo')
    c2,b=context(browser,'administrativo',False);login(b,'administrativo')
    def train():
        goto(a,'/modelo');goto(b,'/modelo');fill(a,'Número de árboles','200')
        a.get_by_role('button',name='Entrenar',exact=True).click(no_wait_after=True)
        b.get_by_role('button',name='Entrenar',exact=True).click(no_wait_after=True)
        visible(b,'Ya hay un entrenamiento en curso');shot(b,'ML-conflicto-segunda-sesion')
        expect(a.get_by_role('button',name='Entrenar',exact=True)).to_be_enabled(timeout=240000)
        a.reload(wait_until='domcontentloaded');expect(a.locator('tbody tr').first).to_contain_text('VIGENTE')
        previous=a.locator('tbody tr').filter(has_text='v3')
        previous.get_by_role('button',name='Publicar esta versión',exact=True).click();visible(a,'es ahora la vigente')
        return 'Dos sesiones gráficas; inicio concurrente rechazado, primer entrenamiento termina; versión v3 restaurada por botón Publicar'
    case('ML-concurrencia','Entrenamientos simultáneos y reversión de versión','administrativo',a,train,[26,27]);c2.close();c1.close()

def crossrole(browser):
    for role in ['supervisor','administrativo','directivo']:
        ctx,p=context(browser,role,False);login(p,role)
        def board():
            goto(p,'/tablero');visible(p,'Total recolectado')
            select(p,'Periodo académico','2-2026');expect(field(p,'Desde')).to_be_disabled();expect(field(p,'Hasta')).to_be_disabled()
            choose_prefix(p,'Sector','FICCT');select(p,'Tipo de residuo','Orgánico');visible(p,'Por sector')
            for figure in p.locator('figure').all():
                figure.get_by_role('button',name='Ver tabla',exact=True).click();expect(figure.locator('table')).to_be_visible()
                figure.get_by_role('button',name='Ver gráfico',exact=True).click()
            click(p,'Restablecer filtros')
            p.locator('figure').filter(has_text='Por sector').first.locator('ul button').first.click()
            assert field(p,'Sector').input_value()!=''
            click(p,'Restablecer filtros');p.locator('figure').filter(has_text='Puntos de mayor generación').first.locator('ul button').first.click()
            expect(p).to_have_url(re.compile('/historico\\?'));visible(p,'Histórico de residuos')
            expect(p.locator('tbody tr').first).to_be_visible()
            goto(p,'/tablero');p.get_by_role('tab',name='Comparar periodos',exact=True).click()
            for i in [0,1]:p.get_by_label('Desde',exact=True).nth(i).fill('2026-09-01' if i==0 else '2026-10-01');p.get_by_label('Hasta',exact=True).nth(i).fill('2026-09-30' if i==0 else '2026-10-31')
            for mode in ['Sector','Punto','Tipo de residuo']:select(p,'Comparar por',mode);expect(p.locator('tbody tr').first).to_be_visible()
            return 'Periodo académico, fechas bloqueadas, filtros, cuatro gráficos/tablas, clic de sector y punto a histórico; comparación por tres dimensiones'
        case('CR-tablero-'+role,'Tablero interactivo y comparación por rol',role,p,board,[12,21,22])
        def mapflow():
            goto(p,'/mapa');choose_prefix(p,'Sector','FICCT');choose_prefix(p,'Punto','FICCT-P1');select(p,'Tipo de residuo','Orgánico')
            p.get_by_role('radio',name='Marcadores',exact=True).click();expect(p.locator('path.leaflet-interactive')).to_have_count(1)
            p.locator('path.leaflet-interactive').first.click(force=True);expect(p.locator('.leaflet-popup')).to_be_visible()
            p.get_by_role('radio',name='Mapa de calor',exact=True).click();expect(p.locator('canvas.leaflet-heatmap-layer')).to_be_visible()
            p.get_by_role('radio',name='Proyectada',exact=True).click();visible(p,'solo se aplica el sector')
            expect(p.locator('path.leaflet-interactive')).to_have_count(3)
            p.get_by_role('radio',name='Marcadores',exact=True).click();p.locator('path.leaflet-interactive').first.click(force=True)
            expect(p.locator('.leaflet-popup')).to_be_visible();visible(p,'±')
            return 'Mapa observado filtrado a un punto; calor, marcadores/popup; capa proyectada por sector con margen'
        case('CR-mapa-'+role,'Cartografía observada y proyectada por rol',role,p,mapflow,[23,24,25])
        def predictionflow():
            goto(p,'/predicciones')
            for invalid in ['0','31']:
                fill(p,'Horizonte (días)',invalid);click(p,'Generar predicción');assert not field(p,'Horizonte (días)').evaluate('(e)=>e.checkValidity()')
            fill(p,'Horizonte (días)','30' if role=='supervisor' else '1');choose_prefix(p,'Sector','FICCT');click(p,'Generar predicción');visible(p,'Modelo v');visible(p,'±')
            p.reload(wait_until='domcontentloaded');visible(p,'Modelo v')
            goto(p,'/recomendaciones');p.get_by_role('radio',name='Todas',exact=True).click();expect(p.locator('main')).to_contain_text('Modelo v')
            if role=='directivo':assert p.get_by_role('button',name='Aceptar',exact=True).count()==0
            return 'Horizontes 0/31 bloqueados, límite '+('30' if role=='supervisor' else '1')+' generado y persistido; consulta recomendaciones'
        case('CR-prediccion-'+role,'Inferencia y consulta de recomendaciones por rol',role,p,predictionflow,[28,29])
        def reportflow():
            goto(p,'/reportes');p.get_by_role('radio',name=re.compile('^Generación proyectada')).click()
            expect(p.get_by_role('heading',name='Generación proyectada por punto',exact=True)).to_be_visible()
            expect(p.get_by_role('button',name='Excel',exact=True)).to_be_enabled()
            rows=p.locator('main tbody tr').evaluate_all("es=>es.map(e=>Array.from(e.querySelectorAll('td')).map(c=>c.textContent.trim()))")
            assert len(rows)>=12
            files=[]
            for label,ext in [('Excel','xlsx'),('PDF','pdf')]:
                with p.expect_download() as event:click(p,label)
                target=OUT/'descargas'/('proyectado-'+role+'-'+STAMP+'.'+ext);event.value.save_as(str(target));files.append(str(target.relative_to(OUT)))
            return dict(filas_ui=rows,archivos=files)
        case('CR-reporte-'+role,'Reporte proyectado no vacío y descargas por rol',role,p,reportflow,[33,34])
        if role=='administrativo':
            def accept():
                goto(p,'/recomendaciones')
                expect(p.get_by_role('button',name='Aceptar',exact=True).first).to_be_visible()
                p.get_by_label('Motivo de la decisión',exact=True).first.fill('Decisión administrativa GUI '+STAMP)
                p.get_by_role('button',name='Aceptar',exact=True).first.click();visible(p,'ACEPTADA')
                p.reload(wait_until='domcontentloaded');p.get_by_role('radio',name='Todas',exact=True).click();visible(p,'Decisión administrativa GUI '+STAMP)
            case('CR-resolver-administrativo','Administrador resuelve recomendación autorizada',role,p,accept,[30])
        ctx.close()

def final_checks(browser):
    ctx,a=context(browser,'administrativo',False);login(a,'administrativo')
    future=(dt.date.today()+dt.timedelta(days=3)).isoformat()
    def plan():
        goto(a,'/jornadas/nueva');fill(a,'Fecha',future);select(a,'Turno','Noche');choose_prefix(a,'Sector','FCEE')
        a.get_by_role('button',name=re.compile('^FCEE-P1')).click();fill(a,'Indicaciones','Plan admin GUI '+STAMP);click(a,'Guardar planificación')
        expect(a).to_have_url(re.compile('/jornadas/\\d+$'));jid=int(a.url.rsplit('/',1)[1])
        click(a,'Asignar cuadrilla');a.get_by_label('Óscar Operario',exact=True).check();select(a,'Responsable de la jornada','Óscar Operario')
        a.get_by_label('DSU-001 · Camioneta de recolección',exact=True).check();click(a,'Guardar asignación');visible(a,'Cuadrilla y vehículos asignados')
        click(a,'Confirmar y publicar');visible(a,'Jornada confirmada');a.reload(wait_until='domcontentloaded');visible(a,'CONFIRMADA')
        assert a.get_by_role('button',name='Abrir jornada',exact=True).count()==0
        (RUN/'jornada_futura.json').write_text(json.dumps(jid),encoding='utf8')
        return 'Administrador planifica, asigna y confirma; no puede abrir ni registrar campo'
    case('FINAL-plan-admin','Planificación y asignación por Administrador','administrativo',a,plan,[14,15]);ctx.close()
    c,p=context(browser,'operario1',False);login(p,'operario1')
    def date():
        jid=json.loads((RUN/'jornada_futura.json').read_text(encoding='utf8'));goto(p,'/campo?jornada='+str(jid));click(p,'Abrir jornada');visible(p,'fecha planificada')
    case('FINAL-fecha','Apertura futura rechazada','operario1',p,date,[16]);c.close()
    for width in [1440,820,390]:
        c,p=context(browser,'administrativo',False,{'width':width,'height':900});login(p,'administrativo')
        def responsive():
            if width<1024:
                click(p,'Abrir menú');p.get_by_role('link',name='Usuarios',exact=True).click()
            else:p.get_by_role('link',name='Usuarios',exact=True).click()
            click(p,'Nuevo');fill(p,'Nombres','Prueba responsive');click(p,'Cancelar')
            assert p.get_by_role('heading',name='Nuevo registro',exact=True).count()==0
            assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            goto(p,'/jornadas');click(p,'Página siguiente');click(p,'Página anterior')
            return 'Menú, navegación, formulario, cancelar, paginación; sin desborde de página'
        case('FINAL-responsive-'+str(width),'Interacciones a '+str(width)+' px','administrativo',p,responsive,[3,19]);c.close()

def final_edit(browser):
    c,p=context(browser,'supervisor',False);login(p,'supervisor')
    def edit():
        jid=json.loads((RUN/'jornada_futura.json').read_text(encoding='utf8'))
        for target in ['FCET','FCEE']:
            goto(p,'/jornadas/'+str(jid));p.get_by_role('link',name='Editar planificación',exact=True).click()
            choose_prefix(p,'Sector',target);expect(p.get_by_role('button',name='Guardar cambios de planificación',exact=True)).to_be_disabled()
            p.get_by_role('button',name=re.compile('^'+target+'-P1')).click();click(p,'Guardar cambios de planificación')
            p.reload(wait_until='domcontentloaded');visible(p,target+'-P1');visible(p,'CONFIRMADA')
        return 'Jornada confirmada editada en dos sectores; ruta anterior vaciada, nueva ruta persistida; se conserva estado confirmado'
    case('J-crear-FICCT','Planificación y cambio de sector con ruta persistida','supervisor',p,edit,[14]);c.close()

def prediction(browser):
    ca,a=context(browser,'administrativo',False);login(a,'administrativo')
    for n in [1,2]:
        def train(n=n):
            goto(a,'/modelo');fill(a,'Número de árboles','100' if n==1 else '120')
            click(a,'Entrenar');visible(a,'Entrenamiento iniciado')
            expect(a.get_by_role('button',name='Entrenar',exact=True)).to_be_enabled(timeout=240000)
            visible(a,'VIGENTE');visible(a,'Coef. de determinación R²')
            row=a.locator('tbody tr').first;assert 'VIGENTE' in row.inner_text()
            a.reload(wait_until='domcontentloaded');visible(a,'VIGENTE')
            return 'Entrenamiento '+str(n)+' completado, métricas visibles y versión vigente persiste'
        case('ML-entrenar-'+str(n),'Entrenamiento y evaluación desde UI','administrativo',a,train,[26])
    def rollback():
        goto(a,'/modelo')
        row=a.locator('tbody tr').filter(has=a.get_by_role('button',name='Publicar esta versión',exact=True)).last
        chosen=row.locator('td').first.inner_text()
        row.get_by_role('button',name='Publicar esta versión',exact=True).click();visible(a,'es ahora la vigente')
        a.reload(wait_until='domcontentloaded');assert 'VIGENTE' in a.locator('tbody tr').filter(has_text=chosen).inner_text()
        return 'Reversión a '+chosen+' persistida'
    case('ML-revertir','Publicar versión anterior del modelo','administrativo',a,rollback,[27])
    ca.close()
    cs,s=context(browser,'supervisor',False);login(s,'supervisor')
    def predict():
        goto(s,'/predicciones');fill(s,'Horizonte (días)','7');click(s,'Generar predicción')
        visible(s,'Modelo v');visible(s,'±')
        s.reload(wait_until='domcontentloaded');visible(s,'Modelo v')
        return 'Lote de siete días solicitado por UI; versión y margen, persistencia al recargar'
    case('ML-predecir','Inferencia y alertas con incertidumbre','supervisor',s,predict,[28])
    def resolve():
        goto(s,'/recomendaciones')
        expect(s.get_by_role('button',name='Aceptar',exact=True).first).to_be_visible()
        s.get_by_role('button',name='Aceptar',exact=True).first.click();visible(s,'Indique el motivo')
        s.get_by_label('Motivo de la decisión',exact=True).first.fill('Aceptada GUI '+STAMP)
        s.get_by_role('button',name='Aceptar',exact=True).first.click();visible(s,'ACEPTADA')
        s.get_by_label('Motivo de la decisión',exact=True).first.fill('Descartada GUI '+STAMP)
        s.get_by_role('button',name='Descartar',exact=True).first.click();visible(s,'DESCARTADA')
        s.reload(wait_until='domcontentloaded');s.get_by_role('radio',name='Todas',exact=True).click()
        visible(s,'Aceptada GUI '+STAMP);visible(s,'Descartada GUI '+STAMP)
        return 'Aceptar/descarte con motivo obligatorio; decisiones persistidas y visibles en Todas'
    case('ML-resolver','Consulta y resolución de recomendaciones','supervisor',s,resolve,[29,30])
    cs.close()

def administration(browser):
    ca,p=context(browser,'administrativo',False);login(p,'administrativo')
    fixtures=json.loads((RUN/'fixtures_gui.json').read_text(encoding='utf8'))
    def find(entity,path,tab=None):
        goto(p,path)
        if tab:p.get_by_role('tab',name=tab,exact=True).click()
        key=fixtures[entity]['key']
        if p.get_by_label('Buscar',exact=True).count():p.get_by_label('Buscar',exact=True).fill(key)
        row=p.locator('tbody tr').filter(has_text=key).first
        row.get_by_role('button',name='Editar',exact=True).click()
    checks=[('punto','/puntos',None,'Capacidad estimada (kg)',[0,-1]),('contenedor','/contenedores',None,'Capacidad (L)',[0,-1]),
        ('unidad','/tipos-residuo','Unidades de medida','Factor de conversión a la base',[0,-1]),('vehiculo','/vehiculos',None,'Capacidad (kg)',[0,-1])]
    for entity,path,tab,label,vals in checks:
        if entity not in fixtures:continue
        for value in vals:
            def invalid(entity=entity,path=path,tab=tab,label=label,value=value):
                find(entity,path,tab);old=field(p,label).input_value();fill(p,label,value)
                with p.expect_response(lambda r:'/api/' in r.url and r.request.method=='PATCH') as response:click(p,'Guardar')
                status=response.value.status
                try:
                    assert status==400,'Validación esperada 400; respuesta '+str(status)
                    expect(p.locator('form')).to_be_visible()
                    assert p.get_by_text('Cambios guardados',exact=False).count()==0
                finally:
                    if status<300:
                        find(entity,path,tab);fill(p,label,old);click(p,'Guardar');visible(p,'Cambios guardados')
                return 'Rechazado por validación del campo; HTTP '+str(status)
            case('LIM-'+entity+'-'+str(value),'Capacidad/factor no positivo '+entity+' '+str(value),'administrativo',p,invalid,[6 if entity=='punto' else 7 if entity=='contenedor' else 8 if entity=='unidad' else 13])
    def geo():
        find('punto','/puntos');fill(p,'Latitud','-18');click(p,'Guardar');visible(p,'fuera del área')
        fill(p,'Latitud','-17.7757001');click(p,'Guardar');visible(p,'6 decimales')
        fill(p,'Latitud','-17.95');fill(p,'Longitud','-63.35');click(p,'Guardar');visible(p,'Cambios guardados')
        find('punto','/puntos');expect(field(p,'Latitud')).to_have_value('-17.950000')
        fill(p,'Latitud','-17.78');fill(p,'Longitud','-63.19');click(p,'Guardar');visible(p,'Cambios guardados')
        return 'Exterior rechazado, precisión >6 rechazada, esquina mínima BBOX aceptada y persistida; ubicación QA restituida'
    if 'punto' in fixtures:case('LIM-geografia','Geografía y precisión de coordenadas','administrativo',p,geo,[6])
    def length():
        find('sector','/sectores');fill(p,'Código','X'*21);click(p,'Guardar');visible(p,'20 caracteres')
        fill(p,'Código',fixtures['sector']['key']);fill(p,'Nombre','X'*121);click(p,'Guardar');visible(p,'120 caracteres')
        fill(p,'Nombre','QA ñ á & <texto> '+STAMP);click(p,'Guardar');visible(p,'Cambios guardados')
        p.reload(wait_until='domcontentloaded');visible(p,'QA ñ á & <texto> '+STAMP)
        assert p.locator('main script').count()==0
        return 'Longitud máxima+1 rechazada; caracteres acentuados y HTML se conservan como texto'
    if 'sector' in fixtures:case('LIM-longitud','Longitudes y caracteres especiales de sector','administrativo',p,length,[5])
    def roleflow():
        goto(p,'/roles');click(p,'Nuevo rol');fill(p,'Nombre del rol','QA GUI '+STAMP)
        choices=p.locator('label').filter(has_text=re.compile(r'Can view sector$',re.I))
        if not choices.count():
            raise AssertionError('No se encontró permiso de consulta sector; revisar inventario de etiquetas')
        choices.first.locator('input[type=checkbox]').check();click(p,'Guardar rol');visible(p,'Rol guardado')
        p.reload(wait_until='domcontentloaded');p.locator('tbody tr').filter(has_text='QA GUI '+STAMP).click()
        expect(field(p,'Nombre del rol')).to_have_value('QA GUI '+STAMP)
        fill(p,'Nombre del rol','QA GUI editado '+STAMP);click(p,'Guardar rol');visible(p,'Rol guardado')
        find('usuario','/usuarios');p.get_by_label('Operativo',exact=True).uncheck()
        p.get_by_label('QA GUI editado '+STAMP,exact=True).check();click(p,'Guardar');visible(p,'Cambios guardados')
        fixtures['rol']={'nombre':'QA GUI editado '+STAMP}
        (RUN/'fixtures_gui.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2),encoding='utf8')
        return 'Rol sintético creado, permiso de consulta, edición y asignación a usuario sintético; cuentas originales intactas'
    if 'usuario' in fixtures:case('ADM-rol','Crear y editar rol sintético, asignarlo a usuario','administrativo',p,roleflow,[4,3])
    def params():
        goto(p,'/parametros');label='Tolerancia sobre la capacidad del punto';old=field(p,label).input_value()
        for v in ['0','6']:
            fill(p,label,v);click(p,'Guardar parámetros');visible(p,'fuera del rango')
        for v in ['1','5',old]:
            fill(p,label,v);click(p,'Guardar parámetros');visible(p,'Parámetros guardados')
            p.reload(wait_until='domcontentloaded');assert float(field(p,label).input_value())==float(v)
        fill(p,'Enlace del informe de Power BI','https://example.invalid/report');click(p,'Guardar parámetros');visible(p,'app.powerbi.com')
        fill(p,'Enlace del informe de Power BI','');click(p,'Guardar parámetros');visible(p,'Parámetros guardados')
        return 'Tolerancia 0/6 rechazadas; límites 1/5 persistidos, valor original restituido; dominio Power BI inválido rechazado'
    case('ADM-parametros','Parámetros y validaciones con persistencia','administrativo',p,params,[31])
    def audit():
        goto(p,'/bitacora');select(p,'Operación','actualizar')
        select(p,'Módulo','Catálogos');expect(p.locator('tbody tr').first).to_be_visible()
        p.locator('tbody tr').first.click();visible(p,'Valores anteriores');visible(p,'Valores nuevos')
        assert p.get_by_role('button',name=re.compile('Editar|Eliminar|Borrar')).count()==0
        return 'Actualización de parámetros visible con antes/después y sin controles de modificación'
    case('ADM-bitacora','Auditoría de cambios reales de GUI','administrativo',p,audit,[32])
    ca.close()

def permissions(browser):
    fixtures=json.loads((RUN/'fixtures_gui.json').read_text(encoding='utf8'))
    username=fixtures['usuario']['key']
    ca,a=context(browser,'administrativo',False);login(a,'administrativo')
    cu,u=context(browser,username,False)
    def synthetic():
        login(u,username);goto(u,'/sectores')
        assert 'rol' in fixtures,'El rol sintético todavía no fue asignado'
        visible(u,fixtures['rol']['nombre'])
        visible(u,'Sectores y facultades')
        assert u.locator('tbody tr').count()==0
        assert u.get_by_role('button',name='Nuevo',exact=True).count()==0
        assert u.get_by_role('button',name='Editar',exact=True).count()==0
        goto(u,'/usuarios');visible(u,'Sin acceso')
        return 'Rol sintético habilita el módulo de sectores; sin rol territorial no recibe registros; sin alta/edición ni acceso a usuarios'
    case('PERM-sintetico','Permisos del rol creado aplicados al nuevo usuario',username,u,synthetic,[4])
    def disabled():
        goto(a,'/usuarios');a.get_by_label('Buscar',exact=True).fill(username)
        row=a.locator('tbody tr').filter(has_text=username).first
        row.get_by_role('button',name='Desactivar',exact=True).click();visible(a,'Registro desactivado')
        u.reload(wait_until='domcontentloaded');expect(u.get_by_label('Usuario',exact=True)).to_be_visible()
        u.get_by_label('Usuario',exact=True).fill(username);u.get_by_label('Contraseña',exact=True).fill(PASS);click(u,'Ingresar');visible(u,'desactivada')
        shot(u,'PERM-cuenta-inactiva')
        a.get_by_label('Estado',exact=True).select_option(label='Inactivos')
        row=a.locator('tbody tr').filter(has_text=username).first;row.get_by_role('button',name='Activar',exact=True).click();visible(a,'Registro reactivado')
        click(u,'Ingresar');expect(u.locator('main')).to_be_visible()
        return 'Baja sintética revoca sesión existente e impide ingreso; reactivación recupera acceso'
    case('PERM-inactivo','Sesión revocada y login de usuario desactivado',username,u,disabled,[1,3])
    def offline():
        goto(a,'/vehiculos');a.get_by_label('Buscar',exact=True).fill(fixtures['vehiculo']['key'])
        a.locator('tbody tr').filter(has_text=fixtures['vehiculo']['key']).get_by_role('button',name='Editar',exact=True).click()
        fill(a,'Descripción','Pendiente sin red '+STAMP)
        ca.set_offline(True)
        try:
            click(a,'Guardar');visible(a,'Sin conexión con el servidor')
            expect(field(a,'Descripción')).to_have_value('Pendiente sin red '+STAMP)
            shot(a,'PERM-sin-conexion')
        finally:ca.set_offline(False)
        click(a,'Guardar');visible(a,'Cambios guardados')
        a.reload(wait_until='domcontentloaded');a.get_by_label('Buscar',exact=True).fill(fixtures['vehiculo']['key']);visible(a,'Pendiente sin red '+STAMP)
        click(a,'Cerrar sesión');login(a,'administrativo');goto(a,'/vehiculos');a.get_by_label('Buscar',exact=True).fill(fixtures['vehiculo']['key']);visible(a,'Pendiente sin red '+STAMP)
        return 'Sin red conserva formulario y mensaje claro; reintento guarda una vez y persiste tras logout/login'
    case('PERM-conexion','Error de conexión, reintento y persistencia entre sesiones','administrativo',a,offline,[13])
    def rolesmissing():
        goto(a,'/roles');click(a,'Nuevo rol')
        inventory(a,'administrativo')
        assert a.locator('label').filter(has_text=re.compile('Can view modelo entrenado',re.I)).count()>0,'El editor de roles no ofrece permisos del módulo prediction'
    case('PERM-prediction','Editor ofrece permisos de todos los módulos','administrativo',a,rolesmissing,[4])
    cu.close();ca.close()

def operations(browser):
    cs,s=context(browser,'supervisor',False);login(s,'supervisor')
    journeys=[]
    field_roles=os.environ.get('DSU_GUI_OPERADORES','operario1,operario2').split(',')
    today=dt.date.today().isoformat()
    shift=os.environ.get('DSU_GUI_TURNO','Tarde')
    for code in ['FICCT','FCET']:
        def plan(code=code):
            goto(s,'/jornadas/nueva')
            fill(s,'Fecha',today);select(s,'Turno',shift)
            options=field(s,'Sector').locator('option').all_text_contents()
            choose_prefix(s,'Sector',code)
            fill(s,'Indicaciones','Recorrido GUI '+STAMP)
            for point in [1,2,3]:s.get_by_role('button',name=re.compile('^'+code+'-P'+str(point))).click()
            click(s,'Bajar '+code+'-P1');click(s,'Subir '+code+'-P1')
            click(s,'Quitar '+code+'-P3');s.get_by_role('button',name=re.compile('^'+code+'-P3')).click()
            click(s,'Guardar planificación')
            expect(s).to_have_url(re.compile(r'/jornadas/\d+$'))
            jid=int(s.url.rsplit('/',1)[1]);journeys.append(jid)
            s.reload(wait_until='domcontentloaded');visible(s,'PLANIFICADA');visible(s,'Recorrido GUI '+STAMP)
            click(s,'Confirmar y publicar');visible(s,'responsable antes de confirmar')
            if code=='FICCT':
                for target in ['FCET','FICCT']:
                    s.get_by_role('link',name='Editar planificación',exact=True).click()
                    expect(s.get_by_role('heading',name='Editar planificación',exact=True)).to_be_visible()
                    choose_prefix(s,'Sector',target)
                    expect(s.get_by_role('button',name='Guardar cambios de planificación',exact=True)).to_be_disabled()
                    for point in ([1] if target=='FCET' else [1,2,3]):s.get_by_role('button',name=re.compile('^'+target+'-P'+str(point))).click()
                    click(s,'Guardar cambios de planificación');expect(s).to_have_url(re.compile(r'/jornadas/\d+$'))
                    s.reload(wait_until='domcontentloaded');visible(s,target+'-P1')
            return dict(jornada=jid,fecha=today,turno=shift,sector=code,ruta='3 puntos, reordenada y persistida')
        case('J-crear-'+code,'Planificar y reordenar ruta '+code,'supervisor',s,plan,[14])
    if len(journeys)!=2:cs.close();return
    (RUN/'jornadas_gui.json').write_text(json.dumps(journeys),encoding='utf8')
    # Dos sesiones gráficas tienen abierto el mismo recurso disponible antes de guardar.
    c2,t=context(browser,'supervisor',False);login(t,'supervisor')
    def prepare(p,jid):
        goto(p,'/jornadas/'+str(jid));click(p,'Asignar cuadrilla')
        p.get_by_label('Óscar Operario',exact=True).check()
        select(p,'Responsable de la jornada','Óscar Operario')
        p.get_by_label('DSU-001 · Camioneta de recolección',exact=True).check()
    def conflict():
        prepare(s,journeys[0]);prepare(t,journeys[1])
        # Ambos formularios ya seleccionaron el mismo recurso; dos clics enviados sin esperar red.
        s.get_by_role('button',name='Guardar asignación',exact=True).click(no_wait_after=True)
        t.get_by_role('button',name='Guardar asignación',exact=True).click(no_wait_after=True)
        visible(s,'Cuadrilla y vehículos asignados')
        visible(t,'asignad')
        assert t.get_by_role('heading',name='Asignar cuadrilla y vehículos').count()==1
        shot(t,'J-conflicto-segunda-sesion')
        return 'Dos contextos gráficos; primer guardado aceptado, segundo rechazado, formulario conserva los datos'
    case('J-concurrencia','Reservas incompatibles en dos sesiones gráficas','supervisor',s,conflict,[15])
    def assign2():
        t.get_by_label('Óscar Operario',exact=True).uncheck()
        t.get_by_label('Olga Operaria',exact=True).check();select(t,'Responsable de la jornada','Olga Operaria')
        click(t,'Guardar asignación');visible(t,'Ya asignados en este turno')
        t.get_by_label('DSU-001 · Camioneta de recolección',exact=True).uncheck()
        t.get_by_label('DSU-002 · Carrito eléctrico',exact=True).check();click(t,'Guardar asignación')
        visible(t,'Cuadrilla y vehículos asignados')
        t.reload(wait_until='domcontentloaded');visible(t,'Olga Operaria')
    case('J-asignar2','Asignación alternativa válida y persistencia','supervisor',t,assign2,[15])
    for p,jid in [(s,journeys[0]),(t,journeys[1])]:
        def confirm(p=p,jid=jid):
            goto(p,'/jornadas/'+str(jid));click(p,'Confirmar y publicar');visible(p,'Jornada confirmada')
            p.reload(wait_until='domcontentloaded');visible(p,'CONFIRMADA')
        case('J-confirmar-'+str(jid),'Confirmar planificación publicada','supervisor',p,confirm,[14,16])
    c2.close()
    contexts=[]
    for idx,role in enumerate(field_roles):
        co,p=context(browser,role,False,{'width':390 if idx==0 else 820,'height':900});contexts.append(co)
        jid=journeys[idx];code=['FICCT','FCET'][idx]
        def openj():
            login(p,role);goto(p,'/campo?jornada='+str(jid));click(p,'Abrir jornada')
            visible(p,'¿Qué residuo retira?');p.reload(wait_until='domcontentloaded');visible(p,'¿Qué residuo retira?')
        if not case('J-abrir-'+role,'Operativo abre su jornada desde campo',role,p,openj,[16]):continue
        if idx==0:
            def premature():
                goto(s,'/jornadas/'+str(jid));click(s,'Cerrar jornada');fill(s,'Observaciones finales','Intento prematuro QA');click(s,'Cerrar definitivamente')
                visible(s,'Puntos sin registro ni motivo');s.reload(wait_until='domcontentloaded');visible(s,'EN EJECUCIÓN')
            case('J-cierre-prematuro','Cierre con paradas pendientes rechazado','supervisor',s,premature,[18])
        def report():
            click(p,'Incidencia');click(p,'Desborde');select(p,'Gravedad','Alta');fill(p,'Qué pasó','Incidencia GUI '+role+' '+STAMP)
            click(p,'Enviar incidencia');visible(p,'Incidencia reportada')
        case('I-reportar-'+role,'Reportar incidencia en campo',role,p,report,[10])
        def register():
            click(p,'Orgánico');fill(p,'Cantidad de orgánico','-1');expect(p.get_by_role('button',name='Registrar vaciado',exact=True)).to_be_disabled()
            fill(p,'Cantidad de orgánico','0');expect(p.get_by_role('button',name='Registrar vaciado',exact=True)).to_be_disabled()
            fill(p,'Cantidad de orgánico','9999');click(p,'Registrar vaciado');visible(p,'excede')
            fill(p,'Cantidad de orgánico','1.25');click(p,'Agregar otro tipo en esta parada')
            click(p,'Papel y cartón');fill(p,'Cantidad de papel y cartón','2.5');click(p,'Observaciones');fill(p,'Observaciones','Registro GUI '+role+' '+STAMP)
            click(p,'Registrar vaciado');visible(p,code+'-P1 registrado')
            p.reload(wait_until='domcontentloaded');visible(p,'ATENDIDO')
            return 'Negativo y cero bloqueados; dos tipos, cantidades decimales, observación; recarga confirma atendido'
        case('R-vaciado-'+role,'Registro multirresiduo con persistencia',role,p,register,[9])
        def zero():
            click(p,'Sin residuos');visible(p,'visita sin residuos');p.reload(wait_until='domcontentloaded');visible(p,'SIN RESIDUOS')
        case('R-sin-'+role,'Visita sin generación',role,p,zero,[9,16])
        def omit():
            click(p,'No pude');expect(p.get_by_role('button',name='Confirmar omisión',exact=True)).to_be_disabled()
            click(p,'Acceso bloqueado');click(p,'Confirmar omisión');visible(p,'omitido')
            p.reload(wait_until='domcontentloaded');visible(p,'OMITIDO');visible(p,'Todos los puntos tienen registro')
        case('R-omitir-'+role,'Omisión justificada y recorrido completo',role,p,omit,[17])
        def outside():
            goto(p,'/campo?jornada='+str(journeys[1-idx]));visible(p,'No se encontró el registro solicitado')
            assert p.get_by_role('button',name='Registrar vaciado',exact=True).count()==0
        if role.startswith('operario'):case('S-alcance-'+role,'Operativo no accede a jornada ajena por URL',role,p,outside,[16])
        co.storage_state(path=str(RUN/(role+'.json')))
    def attend():
        goto(s,'/incidencias')
        for role in field_roles:
            row=s.locator('tbody tr').filter(has_text='Incidencia GUI '+role+' '+STAMP)
            row.get_by_role('button',name='Atender',exact=True).click()
            expect(row.get_by_role('button',name='Asentar',exact=True)).to_be_disabled()
            row.get_by_placeholder('Acción adoptada').fill('Resuelto GUI '+role+' '+STAMP)
            row.get_by_role('button',name='Asentar',exact=True).click();visible(s,'Incidencia atendida')
        select(s,'Estado','Atendidas');s.reload(wait_until='domcontentloaded');select(s,'Estado','Atendidas')
        [visible(s,'Resuelto GUI '+r+' '+STAMP) for r in field_roles]
    case('I-atender','Supervisor atiende incidencias de ambos operativos','supervisor',s,attend,[11])
    for jid in journeys:
        def closej(jid=jid):
            goto(s,'/jornadas/'+str(jid));visible(s,'Consolidado');visible(s,'3,75')
            click(s,'Cerrar jornada');fill(s,'Observaciones finales','Cierre GUI '+STAMP);click(s,'Cerrar definitivamente');visible(s,'Jornada cerrada.')
            s.reload(wait_until='domcontentloaded');visible(s,'CERRADA');visible(s,'Cierre GUI '+STAMP)
            assert s.get_by_role('button',name='Cerrar jornada',exact=True).count()==0
            goto(s,'/jornadas/'+str(jid)+'/editar');visible(s,'no puede modificarse')
        case('J-cerrar-'+str(jid),'Cierre, consolidado y bloqueo de nuevos registros','supervisor',s,closej,[18,19])
    def history():
        goto(s,'/historico');fill(s,'Punto','FICCT-P1');fill(s,'Desde',today);fill(s,'Hasta',today)
        visible(s,'Registro GUI '+field_roles[0]+' '+STAMP);visible(s,'1,25');visible(s,'2,5')
        s.reload(wait_until='domcontentloaded');fill(s,'Punto','FICCT-P1');visible(s,'Registro GUI '+field_roles[0]+' '+STAMP)
    case('R-historico','Buscar y filtrar residuos registrados gráficamente','supervisor',s,history,[12])
    for co in contexts:co.close()
    cs.close()

def main():
    sys.stdout.reconfigure(encoding='utf8')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='chrome',headless=False,slow_mo=60)
        try:
            if PHASE=='auth':auth(browser)
            else: globals()[PHASE](browser)
        finally:
            save()
            try: browser.close()
            except Exception: pass

if __name__=='__main__': main()
