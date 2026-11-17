"""Cabecera JWT solo para el objetivo aislado; nunca imprime la credencial."""
import json
import os
from pathlib import Path


def zap_started(zap, target):
    if not os.environ.get('ZAP_AUTH_HEADER_VALUE'):
        return
    zap.replacer.add_rule(description='Autenticacion de auditoria aislada', enabled=True,
                          matchtype='REQ_HEADER', matchregex=False, matchstring='Authorization',
                          replacement=os.environ['ZAP_AUTH_HEADER_VALUE'], url=target.rstrip('/') + '/.*')
    # Sembrar endpoints de lectura explícitos: el spider de una API JSON no
    # garantiza descubrir las mismas rutas que un navegador autenticado.
    respuestas=[]
    for path in ['', 'auth/me/', 'puntos/', 'sectores/', 'registros/', 'jornadas/',
                 'predicciones/', 'recomendaciones/']:
        url=target+path
        result=zap.core.send_request('GET '+url+' HTTP/1.1\r\nHost: '+os.environ['ZAP_AUTH_HEADER_SITE']+'\r\nAccept: application/json\r\n\r\n', followredirects=False)
        respuestas.append(dict(ruta=path or '/',estado=result[0]['responseHeader'].split('\r\n')[0]))
    Path('/zap/wrk/autenticacion_verificada.json').write_text(json.dumps(respuestas,indent=2),encoding='utf-8')
    assert any(x['ruta']=='puntos/' and '200' in x['estado'] for x in respuestas), 'ZAP no accedió autenticado a puntos'
