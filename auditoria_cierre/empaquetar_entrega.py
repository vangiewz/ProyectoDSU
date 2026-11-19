"""Paquete académico local: lista explícita de recursos, hashes y verificación de secretos privados."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'auditoria_cierre/08_paquete_entrega'
OUT.mkdir(exist_ok=True)
def copiar(src,dest):
    dest=OUT/dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/src,dest)

for ext in ['docx','pdf']:
    copiar('Entregables/Software_2/Documento_Software_2_DSU.'+ext,'01_documento/Documento_Software_2_DSU.'+ext)
for name in ['02_PAPS.pdf','03_SQAP.pdf','04_Manual_de_Usuario.pdf']:
    copiar('Entregables/Material_Drive/'+name,'02_manuales/'+name)
copiar('sitio-residata/pitch/Residata_pitch.pdf','03_pitch/Residata_pitch.pdf')
for p in (ROOT/'DocumentoSoftware2/recursos/sitio').glob('marketing-*.png'):
    copiar(p.relative_to(ROOT),'04_marketing/'+p.name)
for name in ['02_matriz_13_requisitos.md','03_matriz_funcional.md','matriz_trazabilidad.json','06_despliegue_y_operacion.md',
             '07_pendientes_externos.md','09_auditoria_final.md','guion_defensa.md','04_bitacora_cambios.md']:
    copiar('auditoria_cierre/'+name,'05_control/'+name)
for p in (ROOT/'auditoria_cierre/legal').glob('*'):
    if p.is_file():copiar(p.relative_to(ROOT),'06_legal/'+p.name)
for name in ['pruebas/pytest.xml','pruebas_linux/pytest.xml','pruebas_ci/pytest.xml',
             'pruebas/caja_blanca_secuencias.json','qa_url/resumen.json','movil/resultados.json','qa_url/azure_disponibilidad.txt']:
    copiar('docs/auditoria-fase-final/'+name,'07_pruebas/historicas/'+name)
for p in (ROOT/'auditoria_cierre/05_ejecuciones_pruebas').rglob('*'):
    if not p.is_file() or any(part.startswith('.') for part in p.relative_to(ROOT/'auditoria_cierre/05_ejecuciones_pruebas').parts):continue
    # Capturas y reportes; se excluyen datos, dumps, render de cientos de páginas y logs privados de procesos.
    if p.suffix in ['.xml','.json','.txt'] and p.name not in ['api_demo.txt','vite_demo.txt','pg_ctl.txt','reproduccion_antes.txt']:
        copiar(p.relative_to(ROOT),'07_pruebas/'+str(p.relative_to(ROOT/'auditoria_cierre/05_ejecuciones_pruebas')))

excluded={'.venv','node_modules','__pycache__','.pytest_cache','.ruff_cache','.vercel','.git','dist','staticfiles','modelos','respaldos'}
with zipfile.ZipFile(OUT/'08_codigo_fuente_sin_secretos.zip','w',zipfile.ZIP_DEFLATED) as z:
    for folder in ['gestion-residuos-dsu/backend','gestion-residuos-dsu/frontend','sitio-residata']:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or any(part in excluded for part in p.relative_to(ROOT).parts):continue
            if p.name.startswith('.env') and p.name!='.env.example':continue
            if p.suffix in ['.log','.dump','.joblib','.pyc'] or p.name.startswith('~$'):continue
            z.write(p,p.relative_to(ROOT))
    for p in (ROOT/'auditoria_cierre').glob('*.py'):z.write(p,p.relative_to(ROOT))
    for name in ['.github/workflows/ci.yml','DocumentoSoftware2/finanzas.py','DocumentoSoftware2/recursos/finanzas.json',
                 'DocumentoSoftware2/paps.md','DocumentoSoftware2/capitulos.md','DocumentoSoftware2/estimaciones.json']:
        z.write(ROOT/name,name)
    for p in (ROOT/'DocumentoSoftware2/recursos/web').glob('finanzas_*.png'):z.write(p,p.relative_to(ROOT))

(OUT/'LEER_PRIMERO.md').write_text('''# Entrega local de DSU y Residata

El documento incluye trece capítulos. Los resultados y limitaciones están en 05_control/09_auditoria_final.md. No se ha publicado esta versión: el titular realizará la publicación. Las URLs/QR de Residata respondieron HTTP 200 en la reverificación, pero su contenido es anterior: la actualización local está pendiente de publicación.

01_documento: Word/PDF académico. 02_manuales: PAPS, SQAP y manual por rol extraídos. 03_pitch: propuesta financiera. 04_marketing: material diseñado, no campaña ejecutada. 05_control: matrices, guion y pendientes. 06_legal: borradores sin firmas ni registros ficticios. 07_pruebas: evidencias con su entorno. 08_codigo_fuente_sin_secretos.zip: código sin .env real ni historial Git.

Para reproducir el código: usar Python 3.12 en backend y Node >=22.22 en frontend; instalar las dependencias declaradas. Copiar .env.example a una configuración privada y proporcionar valores por canal seguro. El paquete NO contiene la conexión privada. No ejecutar seed ni pruebas con escritura sobre Neon compartido. Usar el runner aislado con PostgreSQL 18 local; navegador de pruebas requiere Playwright/Chrome. Docker/CI son otra opción descrita en el repositorio.

El respaldo privado del trabajo previo queda fuera de este paquete. No se incluyen dumps de base, perfiles personales ni credenciales. No se declara aceptación institucional, registro empresarial, ventas, facturación habilitada ni certificación de calidad.
''',encoding='utf8')

privados=[]
for line in (ROOT/'gestion-residuos-dsu/backend/.env').read_text(encoding='utf8').splitlines():
    if '=' in line:
        key,value=line.split('=',1)
        if key in ['SECRET_KEY','DATABASE_URL','RESPALDO_DATABASE_URL','POWERBI_PASSWORD'] and len(value)>12:
            privados.append((key,value.encode('utf8')))

def verificar(name,contenido):
    for key,value in privados:
        if value in contenido:raise RuntimeError('Secreto privado detectado en '+name+' ('+key+')')

manifest=[]
for p in OUT.rglob('*'):
    if not p.is_file() or p.name=='manifest_sha256.json':continue
    contenido=p.read_bytes();verificar(str(p.relative_to(OUT)),contenido)
    if p.suffix in ['.zip','.docx']:
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():verificar(str(p.relative_to(OUT))+':'+n,z.read(n))
    if p.suffix=='.pdf':
        import pymupdf
        with pymupdf.open(p) as pdf:verificar(str(p.relative_to(OUT)), '\n'.join(pg.get_text() for pg in pdf).encode('utf8'))
    manifest.append({'archivo':str(p.relative_to(OUT)),'bytes':len(contenido),'sha256':hashlib.sha256(contenido).hexdigest()})
(OUT/'manifest_sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Paquete verificado:',len(manifest),'archivos; sin coincidencias con secretos privados del .env.')
