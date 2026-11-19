"""Extrae los requisitos vigentes y enlaza pruebas concretas sin convertir cobertura parcial en aceptación."""
import json
from pathlib import Path
import re
import runpy
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'auditoria_cierre'
with zipfile.ZipFile(ROOT/'docs/Documento_Taller_de_Grado_I_Grupo_8.docx') as z:
    e=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
ps=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in e.findall('.//w:p',ns)]
catalog=runpy.run_path(str(ROOT/'generador/fase2/datos.py'))['CU']
tests=list(ET.parse(OUT/'05_ejecuciones_pruebas/regresion_final.xml').getroot().iter('testcase'))
groups={
    'accounts':('usuarios,roles,permisos,auth','Admin.tsx; Login.tsx','accounts/models; accounts/views; accounts/permissions'),
    'campus':('sectores,puntos,contenedores','Maestros.tsx; MapaCampus.tsx','campus/models; campus/serializers; campus/views'),
    'catalogs':('unidades,tipos-residuo,periodos,parametros','Maestros.tsx; Sistema.tsx','catalogs/models; catalogs/views'),
    'operations':('vehiculos,jornadas,registros,incidencias','Jornadas.tsx; Campo.tsx; Registros.tsx','operations/models; operations/services; operations/views'),
    'analytics':('etl,analitica,reportes','Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx','analytics/models; analytics/services; analytics/views'),
    'prediction':('modelos,predicciones,recomendaciones','Modelo.tsx; Prediccion.tsx; Recomendaciones.tsx','prediction/models; prediction/services; prediction/views'),
    'audit':('bitacora','Admin.tsx','audit/models; audit/services; audit/views'),
}
def app(n):
    if n<=3:return 'accounts'
    if n in [4,5,7]:return 'campus'
    if n in [6,25]:return 'catalogs'
    if 8<=n<=14:return 'operations'
    if 15<=n<=21 or n==27:return 'analytics'
    if 22<=n<=24:return 'prediction'
    return 'audit'
rows=[]
for n in range(1,28):
    rf='RF'+str(n);idx=ps.index(rf);a=app(n)
    casos=[f"CU{c['n']}" for c in catalog if rf in re.findall(r'RF\d+',c['rf'])]
    # Enlaces de pruebas por dominio; no se presume que prueben todas las cláusulas del RF.
    apps=[a] if a in ['accounts','operations','analytics','prediction'] else ['accounts','operations','analytics']
    files=sorted(set(t.attrib['classname'].replace('.','/')+'.py' for t in tests if any(t.attrib['classname'].startswith('apps.'+x+'.tests.') for x in apps)))
    rows.append({'rf':rf,'nombre':ps[idx+1],'casos_uso':casos,'app':a,'api':'/api/{'+groups[a][0]+'}/',
        'pantallas':groups[a][1],'fuentes':'gestion-residuos-dsu/backend/apps/'+groups[a][2],
        'pruebas_relacionadas':files,'estado':'Implementado; cobertura relacionada aprobada, no aceptación integral del RF'})
text='''# Matriz funcional y de trazabilidad del cierre

Fuente de requisitos: docs/Documento_Taller_de_Grado_I_Grupo_8.docx, capítulo 4, extraído del XML vigente. Fuente de CU: generador/fase2/datos.py. Evidencia: regresion_final.xml y demo_ui/resultados.json. Todas las apps comparten PostgreSQL en Neon en el piloto; las pruebas nuevas usan PostgreSQL local sintético. No se atribuye autoría individual.

Los archivos de pruebas relacionados son evidencia de dominio: NO implican cobertura de cada cláusula de un RF. Cada resultado JUnit conserva su testcase exacto y la matriz JSON permite consultarlo.

|RF|Nombre oficial|CU|API|Pantallas|Estado|
|---|---|---|---|---|---|
'''
for r in rows:text+='|'+ '|'.join([r['rf'],r['nombre'],', '.join(r['casos_uso']),r['api'],r['pantallas'],r['estado']])+'|\n'
text+='\n## Requisitos no funcionales y capacidad\n\n|ID|Texto oficial|Evidencia y alcance|Estado|\n|---|---|---|---|\n'
no_func=[]
for idx,s in enumerate(ps):
    if not re.fullmatch(r'(RNF|RTR|RCM)\d+',s):continue
    if any(x['id']==s for x in no_func):continue
    descripcion=ps[idx+2]
    estado='PARCIAL';ev='Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.'
    if s.startswith('RTR') or s in ['RCM3','RCM5','RCM7','RCM8']:
        ev='rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.'
        estado='CUMPLE EN ENTORNO LOCAL'
    if s in ['RNF4','RCM1','RCM2']:
        ev='carga_12_usuarios.txt: 12 hilos, 60 s, 531 peticiones sin errores y 156 vaciados confirmados/persistidos; identidades compartidas de prueba. No mide la VM productiva.'
        estado='CUMPLE EN ENTORNO LOCAL'
    if s=='RNF23':ev='test_etl_convierte_cantidades_sin_error_binario; conversión persistida Decimal, floats solo para estadísticas.'
    if s=='RNF26':ev='Power BI: vistas/modelo disponibles y lectura SQL comprobada previamente; publicación/enlace/RLS pendientes.'
    if s=='RNF12':ev='scripts/respaldo.sh y restauracion.json sintética; copia externa y recuperación productiva no demostradas.'
    if s in ['RNF14','RNF15','RNF16','RNF25']:ev='JUnit accounts/acceso/roles/bitácora y capturas de Directivo sin acceso.'
    if s=='RNF5':ev='Hilos web y separación de modelos: riesgo de interrupción al reiniciar; no hay cola durable.'
    if s in ['RNF18','RNF19']:ev='Chrome aislado y perfiles móviles históricos; no se acredita toda la matriz de navegadores/equipos.'
    if s=='RNF8':ev='Interfaz Campo implementada; cuatro interacciones no instrumentadas de nuevo en todas las variantes.'
    text+='|'+ '|'.join([s,descripcion.replace('|','/'),ev,estado])+'|\n'
    no_func.append({'id':s,'descripcion':descripcion,'evidencia':ev,'estado':estado})
(OUT/'03_matriz_funcional.md').write_text(text,encoding='utf8')
(OUT/'matriz_trazabilidad.json').write_text(json.dumps({'rf':rows,'no_funcionales':no_func,'testcases_junit':[t.attrib for t in tests]},ensure_ascii=False,indent=2),encoding='utf8')
print('Matriz:',len(rows),'RF y',len(no_func),'requisitos no funcionales/rendimiento/capacidad.')
