"""Correspondencia de los ocho paquetes con archivos y tablas reales.

Cada subsistema se organiza por los nodos del despliegue (cliente en Vercel,
API en Azure VM, PostgreSQL en Neon), como el ejemplo de la lámina del
capítulo 8 p. 9, sin introducir capas, archivos ni servidores inexistentes.
"""
import ast
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'generador/fase2'))
import datos as D

APPS = ROOT / 'gestion-residuos-dsu/backend/apps'
SRC = ROOT / 'gestion-residuos-dsu/frontend/src'
CAPAS = ['views', 'serializers', 'services', 'models']
VISTAS_BI = ['bi_hechos_residuos', 'bi_jornadas', 'bi_incidencias', 'bi_puntos', 'bi_predicciones', 'bi_recomendaciones']
OSM = dict(nombre='OpenStreetMap', desde='cliente', etiqueta='HTTPS 443: teselas')
POWERBI_DATOS = dict(nombre='Microsoft Power BI', desde='olap', etiqueta='PostgreSQL/TLS 5432: rol de solo lectura')
POWERBI_INFORME = dict(nombre='Microsoft Power BI', desde='cliente', etiqueta='HTTPS 443: informe insertado')

# servidor: capa -> ['app/archivo.py']; oltp/olap: tablas y vistas de Neon.
SUBSISTEMAS = [
    dict(n=1, cliente=['pages/Login.tsx', 'pages/Admin.tsx'],
         servidor=dict(views=['accounts/auth.py', 'accounts/user.py', 'accounts/role.py'],
                       serializers=['accounts/user.py', 'accounts/role.py'], services=[],
                       models=['accounts/user.py']),
         oltp=['accounts_user', 'accounts_user_groups', 'accounts_user_user_permissions', 'auth_group',
               'auth_group_permissions', 'auth_permission'], olap=[], externos=[],
         texto='La autenticación emite y renueva tokens JWT. Las vistas de usuarios y roles administran las cuentas y los grupos de Django; el permiso RolePermission comprueba las autorizaciones y el alcance territorial. La interfaz consulta los permisos del usuario, pero la API vuelve a validarlos en cada petición.'),
    dict(n=2, cliente=['pages/Maestros.tsx', 'components/Mapa.tsx'],
         servidor=dict(views=['campus/sector.py', 'campus/punto_recoleccion.py', 'campus/contenedor.py',
                              'catalogs/tipo_residuo.py', 'catalogs/unidad_medida.py'],
                       serializers=['campus/sector.py', 'campus/punto_recoleccion.py', 'campus/contenedor.py',
                                    'catalogs/tipo_residuo.py', 'catalogs/unidad_medida.py'], services=[],
                       models=['campus/sector.py', 'campus/punto_recoleccion.py', 'campus/contenedor.py',
                               'catalogs/tipo_residuo.py', 'catalogs/unidad_medida.py']),
         oltp=['campus_sector', 'campus_puntorecoleccion', 'campus_contenedor', 'catalogs_tiporesiduo',
               'catalogs_unidadmedida'], olap=[], externos=[OSM],
         texto='La gestión topológica relaciona sectores, puntos y contenedores. Los formularios utilizan los catálogos de tipos de residuo y unidades del módulo catalogs. La API valida coordenadas, permisos y bajas lógicas. Esta correspondencia comparte código entre paquetes sin introducir otra aplicación o base de datos.'),
    dict(n=3, cliente=['pages/Campo.tsx', 'pages/Registros.tsx'],
         servidor=dict(views=['operations/jornada.py', 'operations/registro_residuo.py', 'operations/incidencia.py'],
                       serializers=['operations/visita.py', 'operations/registro_residuo.py', 'operations/incidencia.py'],
                       services=['operations/visita.py'],
                       models=['operations/registro_residuo.py', 'operations/incidencia.py', 'operations/jornada.py']),
         oltp=['operations_registroresiduo', 'operations_incidencia', 'operations_jornadapunto'], olap=[], externos=[],
         texto='El registro de vaciados se recibe como acción de la jornada y delega las reglas de atención del punto al módulo de servicios visita.py. El histórico y las incidencias tienen vistas propias. Las cantidades se validan y persisten con su usuario y unidad; las modificaciones quedan registradas en la bitácora.'),
    dict(n=4, cliente=['pages/Jornadas.tsx', 'pages/Campo.tsx'],
         servidor=dict(views=['operations/jornada.py', 'operations/vehiculo.py'],
                       serializers=['operations/jornada.py', 'operations/vehiculo.py'],
                       services=['operations/jornada.py', 'operations/visita.py'],
                       models=['operations/jornada.py', 'operations/vehiculo.py']),
         oltp=['operations_jornada', 'operations_jornadapunto', 'operations_jornada_personal',
               'operations_jornada_vehiculos', 'operations_vehiculo'], olap=[], externos=[],
         texto='La logística utiliza el mismo módulo operations que el registro de residuos. El servicio jornada.py controla asignación, confirmación, apertura y cierre; visita.py atiende u omite puntos. Las validaciones impiden superposición de personal o vehículos y transiciones incompatibles con el estado de la jornada.'),
    dict(n=5, cliente=['pages/Tablero.tsx', 'pages/Sistema.tsx'],
         servidor=dict(views=['analytics/ejecucion_etl.py', 'analytics/analitica.py'],
                       serializers=['analytics/ejecucion_etl.py'],
                       services=['analytics/etl.py', 'analytics/indicadores.py'],
                       models=['analytics/ejecucion_etl.py', 'analytics/hecho_residuo.py',
                               'analytics/registro_descartado.py']),
         oltp=['analytics_ejecucionetl', 'analytics_registrodescartado', 'operations_registroresiduo'],
         olap=['analytics_hechoresiduo'] + VISTAS_BI,
         externos=[POWERBI_DATOS, POWERBI_INFORME],
         texto='El proceso ETL transforma los registros operativos y alimenta HechoResiduo sin modificar los datos de origen. Los indicadores se calculan sobre ese plano analítico. Power BI consulta las vistas bi_* con acceso de solo lectura y su informe se presenta en el tablero por HTTPS; su publicación y actualización requieren verificación en el servicio.'),
    dict(n=6, cliente=['pages/MapaCampus.tsx', 'components/Mapa.tsx'],
         servidor=dict(views=['analytics/analitica.py', 'prediction/lote_prediccion.py'], serializers=[],
                       services=['analytics/indicadores.py', 'prediction/prediccion.py'],
                       models=['analytics/hecho_residuo.py', 'campus/punto_recoleccion.py', 'prediction/prediccion.py']),
         oltp=['campus_puntorecoleccion', 'prediction_prediccion'], olap=['analytics_hechoresiduo'], externos=[OSM],
         texto='El mapa observado consulta los agregados analíticos y combina sus resultados con los puntos georreferenciados. La capa proyectada utiliza el servicio de predicción. Leaflet representa las capas y el navegador solicita las teselas a OpenStreetMap por HTTPS; ningún servicio de teselas accede a la base de datos institucional.'),
    dict(n=7, cliente=['pages/Modelo.tsx', 'pages/Prediccion.tsx', 'pages/Recomendaciones.tsx'],
         servidor=dict(views=['prediction/modelo_entrenado.py', 'prediction/lote_prediccion.py', 'prediction/recomendacion.py'],
                       serializers=['prediction/modelo_entrenado.py', 'prediction/lote_prediccion.py',
                                    'prediction/recomendacion.py'],
                       services=['prediction/datos.py', 'prediction/entrenamiento.py', 'prediction/prediccion.py',
                                 'prediction/recomendaciones.py'],
                       models=['prediction/modelo_entrenado.py', 'prediction/lote_prediccion.py',
                               'prediction/prediccion.py', 'prediction/recomendacion.py']),
         oltp=['prediction_modeloentrenado', 'prediction_loteprediccion', 'prediction_prediccion',
               'prediction_recomendacion'], olap=['analytics_hechoresiduo'], externos=[],
         artefacto='modelo-{pk}.joblib',
         texto='El entrenamiento usa hechos depurados, separa cronológicamente entrenamiento y prueba y registra métricas y versiones. La publicación selecciona el modelo vigente. La inferencia produce cantidades con margen de error y recomendaciones sujetas a decisión humana. El artefacto serializado se conserva en ModeloEntrenado y se recupera en una copia local modelo-{pk}.joblib para su ejecución.'),
    dict(n=8, cliente=['pages/Sistema.tsx', 'pages/Reportes.tsx'],
         servidor=dict(views=['audit/audit_log.py', 'catalogs/parametros.py', 'catalogs/periodo_academico.py',
                              'analytics/reportes.py'],
                       serializers=['audit/audit_log.py', 'catalogs/parametros.py', 'catalogs/periodo_academico.py'],
                       services=['audit/bitacora.py', 'analytics/reportes.py'],
                       models=['audit/audit_log.py', 'catalogs/parametros.py', 'catalogs/periodo_academico.py']),
         oltp=['audit_auditlog', 'catalogs_parametrossistema', 'catalogs_periodoacademico'],
         olap=['analytics_hechoresiduo'], externos=[],
         texto='Este paquete transversal reúne configuración, auditoría y reportes, implementados en catalogs, audit y analytics. El trigger de PostgreSQL impide modificar o borrar la bitácora. Los reportes se construyen en el servidor y se descargan como Excel o PDF; esa respuesta binaria complementa el intercambio JSON de la API.'),
]


def ruta(capa, item):
    app, archivo = item.split('/')
    return APPS / app / capa / archivo


def tablas_reales():
    esquema = json.loads((ROOT / 'generador/fase2/esquema.json').read_text(encoding='utf-8'))
    vistas = set()
    for mig in APPS.glob('*/migrations/*.py'):
        vistas |= set(re.findall(r'VIEW (?:IF NOT EXISTS )?(bi_[a-z_]+)', mig.read_text(encoding='utf-8')))
    return {x['tabla'] for x in esquema}, vistas


def dependencias(spec):
    """Dependencias reales entre capas dibujadas, leídas de los imports."""
    dibujadas = {c for c in CAPAS if spec['servidor'][c]}
    deps = set()
    for capa in dibujadas:
        for item in spec['servidor'][capa]:
            app = item.split('/')[0]
            for nodo in ast.walk(ast.parse(ruta(capa, item).read_text(encoding='utf-8'))):
                if not isinstance(nodo, ast.ImportFrom):
                    continue
                mod = nodo.module or ''
                if nodo.level == 2:  # from ..x import a / from .. import x
                    origen = app
                    destinos = [mod.split('.')[0]] if mod else [a.name for a in nodo.names]
                elif nodo.level == 0 and mod.startswith('apps.'):
                    partes = mod.split('.')
                    origen = partes[1]
                    destinos = [partes[2]] if len(partes) > 2 else [a.name for a in nodo.names]
                else:
                    continue
                for dest in destinos:
                    if dest in dibujadas and dest != capa and any(
                            x.split('/')[0] == origen for x in spec['servidor'][dest]):
                        deps.add((capa, dest))
    return sorted(deps, key=lambda d: (CAPAS.index(d[0]), CAPAS.index(d[1])))


def validar():
    assert [s['n'] for s in SUBSISTEMAS] == [p['n'] for p in D.PAQUETES]
    tablas, vistas = tablas_reales()
    assert set(VISTAS_BI) <= vistas, vistas
    for s in SUBSISTEMAS:
        for name in s['cliente']:
            assert (SRC / name).is_file(), name
        assert set(s['servidor']) == set(CAPAS), s['n']
        for capa in CAPAS:
            for item in s['servidor'][capa]:
                assert ruta(capa, item).is_file(), str(ruta(capa, item))
        for t in s['oltp'] + s['olap']:
            assert t in tablas or t in vistas, (s['n'], t)
        assert dependencias(s), s['n']


if __name__ == '__main__':
    validar()
    for s in SUBSISTEMAS:
        print(s['n'], dependencias(s))
    print('8 subsistemas: archivos, tablas, vistas y dependencias verificados')
