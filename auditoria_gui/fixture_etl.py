"""Prepara entradas duplicadas sintéticas; su procesamiento se prueba desde GUI."""
import json
import os
from pathlib import Path
import sys
from decimal import Decimal

ROOT=Path(__file__).resolve().parent.parent
meta=json.loads((ROOT/'auditoria_gui/runtime/servicios.json').read_text(encoding='utf8'))
port=int(meta['pg_port'])
assert meta['web'].startswith('http://127.0.0.1:') and 1024<port<65536
os.environ.update(DATABASE_URL=f'postgresql://dsu_gui@127.0.0.1:{port}/postgres',DJANGO_SETTINGS_MODULE='config.settings',SECRET_KEY='qa-local-aislada-sin-valor-productivo')
sys.path.insert(0,str(ROOT/'gestion-residuos-dsu/backend'))
import django
django.setup()
from django.db import connection
from django.utils import timezone
from apps.operations.models import Jornada, RegistroResiduo
from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import TipoResiduo
from apps.accounts.models import User

assert connection.settings_dict['HOST']=='127.0.0.1' and connection.settings_dict['USER']=='dsu_gui'
point=PuntoRecoleccion.objects.get(codigo='FICCT-P1')
j=Jornada.objects.filter(sector=point.sector,estado='CERRADA').order_by('-pk').first()
tipo=TipoResiduo.objects.get(nombre='Orgánico')
time=timezone.now().replace(second=0,microsecond=0)
tag='FIXTURE GUI DUPLICADOS '+time.isoformat()
assert not RegistroResiduo.objects.filter(observaciones=tag).exists()
RegistroResiduo.objects.bulk_create([RegistroResiduo(jornada=j,punto=point,tipo_residuo=tipo,unidad=tipo.unidad,cantidad=Decimal('0.005'),fecha_hora=time,registrado_por=User.objects.get(username='operario1'),observaciones=tag) for _ in range(2000)])
(ROOT/'auditoria_gui/fixture_etl.json').write_text(json.dumps(dict(origen='Preparación por ORM, exclusivamente PostgreSQL dsu_gui local; no cuenta como operación GUI',registros=2000,duplicados_esperados=1999,tag=tag),ensure_ascii=False,indent=2),encoding='utf8')
print('Preparadas 2000 entradas sintéticas duplicadas en PostgreSQL local; procesar desde GUI.')
