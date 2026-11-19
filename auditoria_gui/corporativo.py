"""Sitio local en Chrome visible. Ninguna solicitud externa se transmite."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import datetime as dt
import json
import re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'auditoria_gui/corporativo'
OUT.mkdir(exist_ok=True)
STAMP=dt.datetime.now().strftime('%Y%m%d-%H%M%S')
RESULTS=[]

class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT/'sitio-residata/dist')))
Thread(target=server.serve_forever,daemon=True).start()
BASE=f'http://127.0.0.1:{server.server_port}/'

def case(p,id,fn):
    row=dict(id=id,inicio_utc=dt.datetime.now(dt.timezone.utc).isoformat(),entorno='Sitio local, Chrome visible; conexiones externas interceptadas')
    try:row.update(estado='APROBADO',detalle=fn() or 'Aserciones gráficas satisfechas')
    except Exception as e:row.update(estado='FALLIDO',detalle=str(e)[:2000])
    target=OUT/(STAMP+'-'+id+'.png');p.screenshot(path=str(target),full_page=True);row['evidencia']=target.name
    RESULTS.append(row);(OUT/('resultados-'+STAMP+'.json')).write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2),encoding='utf8')
    print(id,row['estado'],str(row['detalle'])[:140],flush=True)

try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(channel='chrome',headless=False,slow_mo=80)
    for width in [1440,820,390]:
        ctx=browser.new_context(viewport={'width':width,'height':900},record_video_dir=str(ROOT/'auditoria_gui/videos/corporativo'))
        external=[];errors=[]
        ctx.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else (external.append(dict(metodo=route.request.method,url=route.request.url.split('?')[0])),route.abort())[1])
        p=ctx.new_page();p.set_default_timeout(10000)
        p.on('pageerror',lambda e:errors.append(str(e)))
        for f in sorted((ROOT/'sitio-residata/dist').rglob('*.html')):
            rel=f.relative_to(ROOT/'sitio-residata/dist').as_posix()
            if rel=='404.html':continue
            def pageflow(rel=rel):
                p.goto(BASE+rel,wait_until='domcontentloaded');expect(p.locator('h1')).to_be_visible()
                assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Desborde horizontal'
                for img in p.locator('img').all():
                    img.scroll_into_view_if_needed()
                    p.wait_for_function('(img)=>img.complete&&img.naturalWidth>0',arg=img.element_handle(),timeout=10000)
                p.evaluate('scrollTo(0,0)')
                if width<1024 and p.locator('.abrir-menu').is_visible():
                    p.locator('.abrir-menu').click();expect(p.locator('.abrir-menu')).to_have_attribute('aria-expanded','true')
                    p.locator('.abrir-menu').click();expect(p.locator('.abrir-menu')).to_have_attribute('aria-expanded','false')
                for details in p.locator('details').all():
                    if details.get_attribute('open') is None:details.locator('summary').click()
                    expect(details.locator('p').first).to_be_visible()
                local_links=p.locator('a[href]').evaluate_all("es=>es.map(e=>({texto:e.textContent.trim(),href:e.getAttribute('href')}))")
                return dict(ruta=rel,ancho=width,enlaces=local_links,errores_js=list(errors))
            case(p,re.sub(r'[^a-zA-Z0-9]+','-',rel)+'-'+str(width),pageflow)
        def contact():
            p.goto(BASE+'contacto.html?plan=campus',wait_until='domcontentloaded')
            expect(p.get_by_label('Motivo',exact=True)).to_have_value('Cotización del plan Campus')
            p.get_by_role('button',name='Enviar mensaje',exact=True).click()
            assert not p.locator('form').first.evaluate('(f)=>f.checkValidity()')
            for label,value in [('Nombre','Persona QA'),('Cargo','Evaluación'),('Institución','Institución sintética'),('Correo','qa@example.invalid'),('Mensaje','Prueba local sin envío externo')]:p.get_by_label(label,exact=True).fill(value)
            p.get_by_role('button',name='Enviar mensaje',exact=True).click();expect(p.get_by_text('No se pudo enviar',exact=False)).to_be_visible()
            expect(p.get_by_label('Mensaje',exact=True)).to_have_value('Prueba local sin envío externo')
            return 'Preselección Campus, vacíos rechazados y error de envío controlado; petición externa abortada, sin correo real'
        case(p,'contacto-validacion-error-'+str(width),contact)
        def calendar():
            p.goto(BASE,wait_until='domcontentloaded');slider=p.locator('input[type=range]')
            expect(slider).to_be_visible();slider.focus();slider.press('Home');first=slider.get_attribute('aria-valuetext');slider.press('End');last=slider.get_attribute('aria-valuetext')
            assert first!=last
            return dict(inicio=first,fin=last,control='Teclado en deslizador de calendario')
        case(p,'calendario-'+str(width),calendar)
        (OUT/('red-'+str(width)+'-'+STAMP+'.json')).write_text(json.dumps(dict(solicitudes_bloqueadas=external,errores_js=errors),ensure_ascii=False,indent=2),encoding='utf8')
        ctx.close()
    browser.close()
finally:server.shutdown();server.server_close()
