"""Ensambla el sitio estático: paginas/*.html (cuerpo) + cabecera y pie comunes -> raíz.
Uso: python construir.py   (Vercel publica los .html resultantes; no hay build remoto)."""
from pathlib import Path
import json, re, html

R = Path(__file__).parent
SITIO = 'https://residata-bolivia.vercel.app'
MENU = [('index.html', 'Producto'), ('planes.html', 'Planes'), ('novedades.html', 'Novedades'),
        ('soporte.html', 'Soporte'), ('contacto.html', 'Contacto')]

def cabecera(actual):
    items = ''.join(f'<li><a href="{h}"{" aria-current=page" if h == actual else ""}>{t}</a></li>' for h, t in MENU)
    return f'''<a class="salta" href="#contenido">Saltar al contenido</a>
<header class="cabecera"><div class="fila">
  <a class="marca" href="index.html" aria-label="Residata, inicio"><b>RESIDATA</b><span>S.R.L. · Santa Cruz</span></a>
  <button class="asistente-cab" type="button" data-abrir-asistente aria-controls="asistente">Asistente</button>
  <button class="abrir-menu" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
  <nav aria-label="Principal"><ul class="menu" id="menu">{items}<li><a class="acceso" href="https://dsu-uagrm.vercel.app/">Acceso clientes</a></li></ul></nav>
</div></header>'''

PIE = '''<p class="cierre" aria-hidden="true"><span>Gracias por su visita</span><span class="barras"></span><span>Residata S.R.L.</span></p>
<footer class="pie-sitio"><div class="marco">
  <div><h3>Residata S.R.L.</h3><p>Software de gestión de residuos sólidos con predicción de generación. Santa Cruz de la Sierra, Bolivia. Sociedad en constitución.</p><p><a href="mailto:rekteado@gmail.com">rekteado@gmail.com</a></p></div>
  <div><h3>Producto</h3><ul><li><a href="index.html#como-funciona">Cómo funciona</a></li><li><a href="index.html#pronostico">Pronóstico</a></li><li><a href="planes.html">Planes y precios</a></li><li><a href="https://dsu-uagrm.vercel.app/">Acceso clientes</a></li></ul></div>
  <div><h3>Ayuda</h3><ul><li><a href="soporte.html">Soporte</a></li><li><a href="soporte.html#estado">Estado del servicio</a></li><li><a href="novedades.html">Novedades</a></li><li><a href="feed.xml">RSS</a></li></ul></div>
  <div><h3>Legal</h3><ul><li><a href="terminos.html">Términos y condiciones</a></li><li><a href="privacidad.html">Privacidad</a></li><li><a href="contacto.html">Contacto</a></li></ul></div>
</div></footer>'''

def pagina(nombre, cuerpo):
    m = re.match(r'<!--\s*titulo:(.*?)\|\s*descripcion:(.*?)-->\s*', cuerpo, re.S)
    titulo, desc = (x.strip() for x in m.groups()); cuerpo = cuerpo[m.end():]
    cuerpo = cuerpo.replace('{{calendario}}', (R / 'calendario.json').read_text(encoding='utf-8'))
    if '{{novedades}}' in cuerpo:
        meses = 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split()
        lis = ''
        for e in json.loads((R / 'novedades.json').read_text(encoding='utf-8')):
            a, m, d = e['fecha'].split('-')
            cambios = ''.join(f'<li>{html.escape(c)}</li>' for c in e['cambios'])
            lis += f'<li id="v{e["version"]}"><div><time datetime="{e["fecha"]}">{int(d)} de {meses[int(m)-1]} de {a}</time><span class="version">{e["version"]}</span><span class="estampa">Publicada</span></div><div><h3>{html.escape(e["titulo"])}</h3><ul>{cambios}</ul></div></li>'
        cuerpo = cuerpo.replace('{{novedades}}', lis)
    return f'''<!doctype html>
<html lang="es-BO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#17191c">
<link rel="canonical" href="{SITIO}/{'' if nombre == 'index.html' else nombre}">
<meta property="og:title" content="{html.escape(titulo)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{SITIO}/{nombre}"><meta property="og:image" content="{SITIO}/img/og.png">
<link rel="icon" href="img/icono.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Novedades de Residata" href="{SITIO}/feed.xml">
<link rel="preload" href="fonts/Doto.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/BarlowCondensed-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
<script src="js/site.js" defer></script>
</head>
<body>
{cabecera(nombre)}
<main id="contenido">
{cuerpo}
</main>
{PIE}
</body>
</html>
'''

for f in sorted((R / 'paginas').glob('*.html')):
    (R / f.name).write_text(pagina(f.name, f.read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
    print(f.name)

# RSS de novedades, generado desde las mismas entradas que la página
entradas = json.loads((R / 'novedades.json').read_text(encoding='utf-8'))
from email.utils import format_datetime
from datetime import datetime, timezone, timedelta
items = ''
for e in entradas:
    fecha = datetime.strptime(e['fecha'], '%Y-%m-%d').replace(hour=12, tzinfo=timezone(timedelta(hours=-4)))
    desc = ' '.join(e['cambios'])
    items += f'''  <item><title>{html.escape(e['version'] + ' — ' + e['titulo'])}</title><link>{SITIO}/novedades.html#v{e['version']}</link><guid>{SITIO}/novedades.html#v{e['version']}</guid><pubDate>{format_datetime(fecha)}</pubDate><description>{html.escape(desc)}</description></item>\n'''
(R / 'feed.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
  <title>Novedades de Residata</title><link>{SITIO}/novedades.html</link><description>Versiones y cambios de la plataforma Residata</description><language>es-bo</language>
  <atom:link href="{SITIO}/feed.xml" rel="self" type="application/rss+xml"/>
{items}</channel></rss>
''', encoding='utf-8', newline='\n')
print('feed.xml')
