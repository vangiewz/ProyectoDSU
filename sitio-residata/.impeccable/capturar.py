import sys
from playwright.sync_api import sync_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765/'
with sync_playwright() as p:
    b=p.chromium.launch(channel='chrome')
    for nombre,w,h in [('desktop',1440,900),('mobile',390,844)]:
        pg=b.new_page(viewport={'width':w,'height':h}, device_scale_factor=1)
        errores=[]; pg.on('console', lambda m: errores.append(m.text) if m.type=='error' else None); pg.on('pageerror', lambda e: errores.append(str(e)))
        for ruta in ['index.html','planes.html','soporte.html','novedades.html','contacto.html','terminos.html']:
            pg.goto(BASE+ruta, wait_until='networkidle'); pg.wait_for_timeout(1500)
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(1200); pg.evaluate("window.scrollTo(0,0)")
            ancho=pg.evaluate("document.documentElement.scrollWidth")
            pg.screenshot(path=f'.impeccable/review/{nombre}{"" if ruta=="index.html" else "-"+ruta[:-5]}.png', full_page=True)
            print(nombre, ruta, 'scrollWidth', ancho)
        if nombre=='desktop':
            pg.goto(BASE+'index.html', wait_until='networkidle'); pg.click('.asistente-boton'); pg.wait_for_timeout(300)
            pg.fill('#pregunta','¿Necesitan sensores?'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
            pg.click('text=Hablar con una persona'); pg.wait_for_timeout(300)
            pg.screenshot(path='.impeccable/review/desktop-asistente.png')
        print('errores', errores)
    b.close()
