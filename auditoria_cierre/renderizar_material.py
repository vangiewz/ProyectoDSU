"""Exporta pitch y piezas en navegador efímero; produce capturas verificables de la versión local."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'sitio-residata')))
Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:%s/'%server.server_port
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,channel='chrome')
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.goto(base+'pitch/',wait_until='networkidle')
        page.pdf(path=str(ROOT/'sitio-residata/pitch/Residata_pitch.pdf'),print_background=True,prefer_css_page_size=True)
        for i,slide in enumerate(page.locator('.lamina').all(),1):
            slide.screenshot(path=str(ROOT/('DocumentoSoftware2/recursos/pitch/lamina-%02d.png'%i)))
        page.goto(base+'marketing/',wait_until='networkidle')
        for selector,name in [('#post-kilos','post-kilos'),('#post-sensores','post-sensores'),('#banner','banner')]:
            if page.locator(selector).count():
                page.locator(selector).screenshot(path=str(ROOT/('DocumentoSoftware2/recursos/sitio/marketing-'+name+'.png')))
        browser.close()
finally:server.shutdown();server.server_close()
print('Pitch PDF y láminas de la versión local exportados.')
