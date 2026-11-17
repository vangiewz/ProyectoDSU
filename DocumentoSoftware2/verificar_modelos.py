"""Verificación estructural y render de la edición con modelos."""
from pathlib import Path
import hashlib, json, re, zipfile
from collections import Counter
import pypdfium2 as pdfium
from pypdf import PdfReader
from PIL import Image, ImageDraw
from docx import Document

root=Path(__file__).resolve().parent; repo=root.parent
qa=repo/'tmp/software2_diagramas'; qa.mkdir(exist_ok=True)
manifest=json.loads((root/'recursos/manifest_figuras.json').read_text(encoding='utf8'))
doc=Document(root/'Documento_Software_2_DSU_con_diagramas.docx')
assert len(doc.inline_shapes)==136
assert len(manifest)==135 and [x['figura'] for x in manifest]==list(range(1,136))
assert len({x['sha256'] for x in manifest})==135
with zipfile.ZipFile(repo/'docs/Documento_Taller_de_Grado_I_Grupo_8.docx') as z:
    hashes={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
new=[x for x in manifest if 'grupo' in x]
assert len(new)==132 and all(x['sha256'] in hashes for x in new)
for prefix in ['fase2/c5_cu','fase2/c6_cu']:
    ids=sorted(int(re.search(r'cu(\d+)',x['fuente'])[1]) for x in manifest if prefix in x['fuente'])
    assert ids==list(range(1,35)), (prefix,ids)
pdf=PdfReader(qa/'revision.pdf'); d=pdfium.PdfDocument(qa/'revision.pdf')
info=[]; issues=[]
for i,p in enumerate(pdf.pages):
    text=p.extract_text(); nums=[int(n) for n in re.findall(r'Figura\s+(\d+)\.',text)]
    page=d[i]; objects=list(page.get_objects())
    imgs=[o for o in objects if o.type==3]
    if nums and not imgs: issues.append({'pagina':i+1,'error':'Rótulo sin imagen','figuras':nums})
    if len(text.strip())<12: issues.append({'pagina':i+1,'error':'Página casi vacía'})
    if '¡Error!' in text or 'Error! Bookmark' in text: issues.append({'pagina':i+1,'error':'Campo roto'})
    for ob in imgs:
        x0,y0,x1,y1=ob.get_bounds()
        if x0<20 or y0<25 or x1>float(p.mediabox.width)-20 or y1>float(p.mediabox.height)-25:
            issues.append({'pagina':i+1,'error':'Imagen fuera de márgenes','caja':[x0,y0,x1,y1]})
    im=page.render(scale=1.3).to_pil(); im.save(qa/f'pagina-{i+1:03d}.png')
    info.append(dict(pagina=i+1,figuras=nums,imagenes=len(imgs),caracteres=len(text),inicio=text[:110],fin=text[-120:],ancho=float(p.mediabox.width),alto=float(p.mediabox.height)))
    page.close()
for start in range(0,len(info),12):
    sheet=Image.new('RGB',(1800,2240),'#dddddd'); draw=ImageDraw.Draw(sheet)
    for k,item in enumerate(info[start:start+12]):
        im=Image.open(qa/f"pagina-{item['pagina']:03d}.png"); im.thumbnail((580,510))
        x=(k%3)*600+(600-im.width)//2;y=(k//3)*560+35
        sheet.paste(im,(x,y));draw.text(((k%3)*600+12,(k//3)*560+9),f"Pagina {item['pagina']}  Figuras {item['figuras']}",fill='black')
    sheet.save(qa/f'plancha-{start//12+1:02d}.png')
figs=[n for x in info for n in x['figuras']]
assert sorted(figs)==list(range(1,136)), Counter(figs)
report=dict(paginas=len(info),figuras=135,diagramas=134,diagramas_nuevos=132,
    identicos_a_taller=len(new),incidencias=issues,paginacion=info)
(qa/'auditoria.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='paginacion'},ensure_ascii=True))
