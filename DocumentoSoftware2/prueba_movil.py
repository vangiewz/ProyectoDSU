"""Prueba funcional móvil del sistema desplegado (cap. 9): emula dispositivos reales con Playwright
(viewport, densidad, tacto y user agent), inicia sesión por rol y recorre las pantallas de campo y
supervisión. Guarda capturas y resultados en docs/auditoria-fase-final/movil/. Uso: python prueba_movil.py"""
import json, sys, time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

APP = 'https://dsu-uagrm.vercel.app'
CLAVE = sys.argv[1] if len(sys.argv) > 1 else 'Residuos.2026'
OUT = Path(__file__).resolve().parents[1] / 'docs/auditoria-fase-final/movil'; OUT.mkdir(parents=True, exist_ok=True)
CASOS = [  # (usuario, ruta, texto que debe aparecer)
    ('operario1', 'campo', None), ('supervisor', 'jornadas', 'Jornadas'), ('supervisor', 'predicciones', 'Predicción'),
    ('supervisor', 'mapa', 'Mapa del campus'), ('directivo', 'tablero', 'Tablero de gestión'), ('supervisor', 'reportes', 'Reportes')]
resultados = []
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for disp in ['iPhone 13', 'Pixel 7']:
        sesiones = {}
        for usuario, ruta, esperado in CASOS:
            if usuario not in sesiones:
                ctx = b.new_context(**p.devices[disp]); pg = ctx.new_page()
                t0 = time.perf_counter(); pg.goto(APP, wait_until='networkidle')
                pg.locator('input').nth(0).fill(usuario); pg.locator('input[type=password]').fill(CLAVE)
                pg.locator('button[type=submit]').tap()
                pg.locator('input[type=password]').wait_for(state='detached', timeout=45000)
                sesiones[usuario] = (pg, round(time.perf_counter() - t0, 2))
            pg, t_login = sesiones[usuario]
            t0 = time.perf_counter(); pg.goto(f'{APP}/{ruta}', wait_until='networkidle'); t_carga = round(time.perf_counter() - t0, 2)
            pg.wait_for_timeout(800)
            ancho = pg.evaluate('document.documentElement.scrollWidth'); vista = pg.viewport_size['width']
            texto = pg.inner_text('body')
            ok = ancho <= vista and (esperado is None or esperado in texto) and 'Ingresar al sistema' not in texto
            archivo = f"{disp.replace(' ', '_')}-{ruta}-{usuario}.png"; pg.screenshot(path=OUT / archivo)
            resultados.append({'dispositivo': disp, 'usuario': usuario, 'ruta': ruta, 'login_s': t_login, 'carga_s': t_carga,
                               'ancho_documento': ancho, 'ancho_vista': vista, 'sin_desborde': ancho <= vista, 'resultado': 'Aprobado' if ok else 'Fallido', 'captura': archivo})
            print(resultados[-1])
    b.close()
(OUT / 'resultados.json').write_text(json.dumps({'fecha': datetime.now().astimezone().isoformat(timespec='seconds'), 'casos': resultados}, indent=2, ensure_ascii=False), encoding='utf-8')
