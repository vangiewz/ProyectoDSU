"""Navegación local y capturas, navegador efímero sin perfil personal ni envío de formularios."""
import datetime as dt
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "auditoria_cierre/05_ejecuciones_pruebas/sitio"
OUT.mkdir(parents=True, exist_ok=True)


class Silencioso(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Silencioso, directory=str(ROOT / "sitio-residata/dist")))
Thread(target=server.serve_forever, daemon=True).start()
base = "http://127.0.0.1:%s/" % server.server_port
resultados = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, channel="chrome")
        for ancho in [1440, 390]:
            page = browser.new_page(viewport={"width": ancho, "height": 900})
            # Ningún formulario, recurso remoto o sondeo del sitio sale del entorno de prueba.
            page.route("**/*", lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
            errores = []
            page.on("pageerror", lambda error: errores.append(str(error)))
            for path in ["", "planes.html", "contacto.html", "soporte.html", "terminos.html", "privacidad.html", "marketing/", "pitch/"]:
                response = page.goto(base + path, wait_until="networkidle")
                assert response.status == 200, (path, response.status)
                assert page.locator("h1").count() > 0, path
                sin_desborde = page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                assert sin_desborde, (path, ancho)
                if path in ["", "planes.html", "marketing/", "pitch/"]:
                    page.screenshot(path=str(OUT / ((path.replace('/', '-').replace('.html', '') or 'inicio') + '-%s.png' % ancho)), full_page=True)
                resultados.append(dict(ruta=path or "/", ancho=ancho, http=response.status, sin_desborde=sin_desborde))
            assert not errores, errores
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
    (OUT / "resultados.json").write_text(json.dumps(dict(fecha_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        entorno="Chrome headless, publicación local; sin enviar formularios", casos=resultados), ensure_ascii=False, indent=2), encoding="utf8")
print("Sitio local: %s recorridos HTTP/UI aprobados." % len(resultados))
