"""Pruebas por URL con servicios externos (cap. 9): Mozilla HTTP Observatory, Qualys SSL Labs,
Google Lighthouse (perfil móvil) y validador HTML del W3C. Guarda respuestas originales y un resumen
en docs/auditoria-fase-final/qa_url/. Uso: python qa_url.py"""
import json, subprocess, time, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'docs/auditoria-fase-final/qa_url'
OUT.mkdir(parents=True, exist_ok=True)
SITIOS = {
    'sitio': 'https://residata-bolivia.vercel.app/',
    'app': 'https://dsu-uagrm.vercel.app/',
    'api': 'https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com/api/',
}
UA = {'User-Agent': 'qa-url-proyecto-academico/1.0'}

def get(url, data=None):
    req = urllib.request.Request(url, data=data, headers=UA, method='POST' if data is not None else 'GET')
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

def observatory(host):
    return get('https://observatory-api.mdn.mozilla.net/api/v2/scan?host=' + host, data=b'')

def ssllabs(host):
    base = 'https://api.ssllabs.com/api/v3/analyze?host=' + host
    d = get(base + '&startNew=on&all=done')
    while d.get('status') not in ('READY', 'ERROR'):
        time.sleep(20); d = get(base + '&all=done')
    return d

def w3c(url):
    return get('https://validator.w3.org/nu/?out=json&doc=' + urllib.parse.quote(url, safe=''))

def lighthouse(url, nombre):
    archivo = OUT / f'lighthouse-{nombre}.json'
    subprocess.run(['npx', '--yes', 'lighthouse@12', url, '--quiet', '--output=json', f'--output-path={archivo}',
                    '--chrome-flags=--headless=new', '--form-factor=mobile', '--throttling-method=simulate'],
                   check=True, shell=True)
    d = json.loads(archivo.read_text(encoding='utf-8'))
    return {k: round(v['score'] * 100) for k, v in d['categories'].items()}

resumen = {'fecha': datetime.now().astimezone().isoformat(timespec='seconds'), 'resultados': {}}
for nombre, url in SITIOS.items():
    host = urllib.parse.urlparse(url).hostname; r = {}
    try:
        o = observatory(host); (OUT / f'observatory-{nombre}.json').write_text(json.dumps(o, indent=2), encoding='utf-8')
        r['observatory'] = {'grado': o.get('grade'), 'puntaje': o.get('score'), 'pruebas_fallidas': o.get('tests_failed'), 'pruebas_superadas': o.get('tests_passed')}
    except Exception as e: r['observatory'] = {'error': str(e)}
    if nombre != 'app':  # app y sitio comparten el certificado y la terminación TLS de Vercel
        try:
            s = ssllabs(host); (OUT / f'ssllabs-{nombre}.json').write_text(json.dumps(s, indent=2), encoding='utf-8')
            r['ssllabs'] = [{'ip': ep.get('ipAddress'), 'grado': ep.get('grade'), 'advertencias': ep.get('hasWarnings')} for ep in s.get('endpoints', [])]
        except Exception as e: r['ssllabs'] = {'error': str(e)}
    if nombre != 'api':
        try:
            v = w3c(url); (OUT / f'w3c-{nombre}.json').write_text(json.dumps(v, indent=2, ensure_ascii=False), encoding='utf-8')
            msgs = v.get('messages', [])
            r['w3c'] = {'errores': sum(m['type'] == 'error' for m in msgs), 'advertencias': sum(m.get('subType') == 'warning' for m in msgs),
                        'detalle': [m['message'] for m in msgs if m['type'] == 'error'][:8]}
        except Exception as e: r['w3c'] = {'error': str(e)}
        try: r['lighthouse_movil'] = lighthouse(url, nombre)
        except Exception as e: r['lighthouse_movil'] = {'error': str(e)}
    resumen['resultados'][nombre] = {'url': url, **r}
    print(nombre, json.dumps(r, ensure_ascii=False))
(OUT / 'resumen.json').write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding='utf-8')
