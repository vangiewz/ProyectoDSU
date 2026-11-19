"""Capturas del sistema desplegado (Vercel + API en Azure) con los usuarios demo.
Uso: python capturar_produccion.py  ->  recursos/prod/<ruta>-<rol>-<ancho>.png"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
APP='https://dsu-uagrm.vercel.app'; OUT=Path(__file__).parent/'recursos/prod'
CLAVE=sys.argv[1] if len(sys.argv)>1 else 'Residuos.2026'
PLAN={'supervisor':[('tablero',1440),('mapa',1440),('predicciones',1440),('recomendaciones',1440),('jornadas',1440),('reportes',1440),('tablero',390)],
      'operario1':[('campo',390)],'directivo':[('tablero',1440)],'admin_login':[]}
with sync_playwright() as p:
    b=p.chromium.launch(channel='chrome')
    pg=b.new_page(viewport={'width':1440,'height':900}); pg.goto(APP,wait_until='networkidle')
    pg.screenshot(path=OUT/'login-1440.png')
    for user,rutas in PLAN.items():
        if not rutas: continue
        ctx=b.new_context(viewport={'width':1440,'height':900}); pg=ctx.new_page(); pg.goto(APP,wait_until='networkidle')
        pg.locator('input').nth(0).fill(user); pg.locator('input[type=password]').fill(CLAVE); pg.keyboard.press('Enter')
        pg.locator('input[type=password]').wait_for(state='detached', timeout=45000); pg.wait_for_load_state('networkidle')
        for ruta,w in rutas:
            pg.set_viewport_size({'width':w,'height':900 if w>400 else 844})
            pg.goto(f'{APP}/{ruta}',wait_until='networkidle'); pg.wait_for_timeout(2500)
            if ruta in ('tablero','mapa'):  # el histórico demo termina en octubre de 2026
                fechas=pg.locator('input[type=date]')
                if fechas.count()>=2:
                    fechas.nth(0).fill('2026-03-01'); fechas.nth(1).fill('2026-10-05'); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(3000)
            f=OUT/f'{ruta}-{user}-{w}.png'; pg.screenshot(path=f,full_page=True); print(f.name)
        ctx.close()
    b.close()
