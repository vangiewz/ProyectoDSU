"""Estado sin modelo como fixture reversible, solo clúster GUI sintético."""
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent.parent
RUN=ROOT/'auditoria_gui/runtime'
meta=json.loads((RUN/'servicios.json').read_text(encoding='utf8'))
port=int(meta['pg_port'])
assert meta['web'].startswith('http://127.0.0.1:') and 1024<port<65536
os.environ.update(DATABASE_URL=f'postgresql://dsu_gui@127.0.0.1:{port}/postgres',DJANGO_SETTINGS_MODULE='config.settings',SECRET_KEY='qa-local-aislada-sin-valor-productivo')
sys.path.insert(0,str(ROOT/'gestion-residuos-dsu/backend'))
import django
django.setup()
from django.db import connection,transaction
from apps.prediction.models import ModeloEntrenado

assert connection.settings_dict['HOST']=='127.0.0.1' and connection.settings_dict['USER']=='dsu_gui'
with transaction.atomic():
    if sys.argv[1]=='preparar':
        assert not ModeloEntrenado.objects.filter(estado='EN_CURSO').exists()
        ids=list(ModeloEntrenado.objects.filter(vigente=True).values_list('pk',flat=True))
        assert len(ids)==1
        (RUN/'vigente_fixture.json').write_text(json.dumps(ids),encoding='utf8')
        ModeloEntrenado.objects.filter(pk__in=ids).update(vigente=False)
    elif sys.argv[1]=='restaurar':
        ids=json.loads((RUN/'vigente_fixture.json').read_text(encoding='utf8'))
        assert not ModeloEntrenado.objects.filter(vigente=True).exists()
        assert ModeloEntrenado.objects.filter(pk__in=ids,estado='APROBADO').update(vigente=True)==1
    else:raise RuntimeError('Modo de fixture desconocido')
print('Fixture de modelo local: '+sys.argv[1])
