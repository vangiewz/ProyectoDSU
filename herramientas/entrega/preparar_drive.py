"""Prepara carpetas específicas para actualizar el Drive académico sin secretos."""
from pathlib import Path
import hashlib,json,os,shutil,zipfile,collections,csv
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Entregables/Drive_Organizado_20261119'
CANON=ROOT/'revision_documental_final/entrega'
BLOCKED={'.git','.vercel','.venv','venv','node_modules','dist','build','.dart_tool','.gradle','__pycache__','.pytest_cache','.ruff_cache','.claude','.codex','respaldos','modelos','staticfiles','.pbi','graphify-out','.cache','.impeccable'}
def safe(p):
 return not any(x in BLOCKED for x in p.parts) and not p.name.startswith('.env') and p.name not in {'local.properties','key.properties'} and p.suffix.lower() not in {'.pem','.key','.jks','.keystore','.pyc','.log','.err'}
def files(folder):
 for directory,dirs,names in os.walk(folder):
  dirs[:]=sorted(d for d in dirs if d not in BLOCKED)
  for name in sorted(names):yield Path(directory)/name

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def copy(src,dest):
 target=OUT/dest;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
def tree(src,dest):
 for p in sorted(src.rglob('*')):
  if p.is_file():copy(p,Path(dest)/p.relative_to(src))
for ext in ['pdf','docx']:copy(CANON/f'Documento_Software_2_DSU_Entrega.{ext}',f'01_Documento/Documento_Software_2_DSU.{ext}')
for folder,name in [('02_PAPS','02_PAPS.pdf'),('03_Calidad','03_SQAP.pdf'),('04_Manual_de_Usuario','04_Manual_de_Usuario.pdf')]:copy(ROOT/'Entregables/Material_Drive'/name,folder+'/'+name)
copy(ROOT/'gestion-residuos-dsu/frontend/docs/MANUAL_USUARIO.md','04_Manual_de_Usuario/MANUAL_USUARIO_WEB.md')
for p in (ROOT/'auditoria_gui/capturas').glob('auth-ROUTE-*.png'):copy(p,'05_Capturas_del_sistema/'+p.name)
tree(CANON/'diagramas_y_figuras','06_Diagramas_UML/Figuras')
tree(CANON/'modelos','06_Diagramas_UML/Modelos_EA')
copy(CANON/'matriz_fuentes_diagramas.json','06_Diagramas_UML/matriz_fuentes_diagramas.json')
tree(CANON/'pruebas','07_Pruebas/Resultados')
tree(ROOT/'auditoria_movil','07_Pruebas/Movil')
parts=CANON/'evidencias/Evidencias_GUI_DSU_Residata.zip.partes';m=json.loads((parts/'manifest.json').read_text(encoding='utf-8'))
videos=OUT/'07_Pruebas/Resultados/Evidencias_GUI_DSU_Residata.zip';videos.parent.mkdir(parents=True,exist_ok=True)
with videos.open('wb') as dest:
 for row in m['partes']:
  p=parts/row['archivo'];assert digest(p)==row['sha256']
  with p.open('rb') as f:shutil.copyfileobj(f,dest)
assert digest(videos)==m['sha256']
groups={
 **dict.fromkeys(['auth','auth_extra','auth_negative','crossrole','permissions'],'Acceso_y_Permisos'),
 **dict.fromkeys(['administration','catalogs'],'Administracion_y_Catalogos'),
 **dict.fromkeys(['analytics','etl_concurrent','etl_repeat'],'Analitica_y_Procesos'),
 **dict.fromkeys(['operations'],'Operacion_en_Campo'),
 **dict.fromkeys(['prediction','prediction_negative','model_absent','model_concurrent'],'Prediccion'),
 **dict.fromkeys(['corporativo','corporate'],'Sitio_Corporativo'),
 **dict.fromkeys(['final_checks','final_edit','race'],'Validaciones_Adicionales')}
counts=collections.Counter();rows=[]
with zipfile.ZipFile(videos) as z:
 for info in z.infolist():
  if not info.filename.lower().endswith('.webm'):continue
  category=groups[info.filename.split('/')[-2]];counts[category]+=1
  name=f'{counts[category]:02d}_Recorrido.webm';dest=OUT/'07_Pruebas/Videos'/category/name
  dest.parent.mkdir(parents=True,exist_ok=True)
  with z.open(info) as source,dest.open('wb') as target:shutil.copyfileobj(source,target)
  rows.append([category,name,info.filename])
assert len(rows)==66
with (OUT/'07_Pruebas/Videos/INDICE_VIDEOS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['Categoria','Archivo','Ruta_original_evidencia']);writer.writerows(rows)
code=OUT/'08_Codigo_Fuente/Codigo_Fuente_DSU.zip';code.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(code,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for folder in ['gestion-residuos-dsu/backend','gestion-residuos-dsu/frontend','gestion-residuos-dsu/movil','sitio-residata','herramientas','despliegue']:
  for p in files(ROOT/folder):
   if safe(p.relative_to(ROOT)):z.write(p,p.relative_to(ROOT).as_posix())
 z.write(ROOT/'.github/workflows/ci.yml','.github/workflows/ci.yml')
 for name in ['README.md','AGENTS.md','CLAUDE.md','.gitignore','.gitattributes']:z.write(ROOT/name,name)
with zipfile.ZipFile(code) as z:
 assert z.testzip() is None
 assert not any(Path(p).name.startswith('.env') or '.vercel/' in p or 'local.properties' in p for p in z.namelist())
copy(ROOT/'Entregables/Material_Drive/09_Android/DSU_Campo_Android_Demo.apk','09_App_Android/DSU_Campo_Android_Demo.apk')
copy(ROOT/'gestion-residuos-dsu/movil/README.md','09_App_Android/LEEME_ANDROID.md')
copy(ROOT/'Entregables/Material_Drive/10_Marketing/Folleto_Residata.pdf','10_Marketing_y_Pitch/Folletos/Folleto_Residata.pdf')
for p in (ROOT/'DocumentoSoftware2/recursos/sitio').glob('marketing-*.png'):copy(p,'10_Marketing_y_Pitch/Piezas/'+p.name)
copy(ROOT/'sitio-residata/pitch/Residata_pitch.pdf','10_Marketing_y_Pitch/Pitch/Residata_pitch.pdf')
tree(CANON/'defensa','11_Defensa')
tree(ROOT/'Entregables/Material_Drive/08_Respaldo','12_Respaldo_Documental')
(OUT/'00_LEEME.md').write_text('''# DSU y Residata - material vigente al 19/11/2026

01_Documento: PDF para imprimir y Word editable del cierre canónico. El nombre de Drive se conserva; el contenido es la versión Entrega.
02_PAPS: plan del proyecto. 03_Calidad: SQAP. 04_Manual_de_Usuario: manual PDF y fuente por rol.
05_Capturas_del_sistema: pantallas por rol. 06_Diagramas_UML: figuras y modelos EA.
07_Pruebas: resultados, límites de la revisión y 66 videos de pruebas dentro del ZIP de evidencias. No es un video comercial narrado.
08_Codigo_Fuente: código de backend, web, sitio y Flutter, sin .env ni configuraciones personales.
09_App_Android: APK demo ARM64 y guía. GPS y dictado para reportar incidencias a Azure; sin fotos ni cola offline.
10_Marketing_y_Pitch: folleto, piezas digitales y presentación. 11_Defensa: guías y preguntas. 12_Respaldo_Documental: cartas, carátulas firmadas y QR preservados.

El documento académico no se modificó para añadir el complemento móvil. El manual y los estándares están en su capítulo 12, sección 3.9.3 y anexo I, respectivamente. Las métricas y sus límites se mantienen en las evidencias. Las configuraciones privadas no forman parte del material compartido.
''',encoding='utf-8')
manifest={p.relative_to(OUT).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='MANIFIESTO_SHA256.json'}
(OUT/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Carpetas preparadas:',len([p for p in OUT.iterdir() if p.is_dir()]),'; archivos:',len(manifest))
print(OUT)
