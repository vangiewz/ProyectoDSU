from pathlib import Path
from docx import Document
import json,hashlib
root=Path.cwd(); out=root/'docs/auditoria-2026-10-28'
p=root/'docs/Documento_Taller_de_Grado_I_Grupo_8.docx'; d=Document(p)
lines=[]; headings=[]; images=[]
for i,b in enumerate(d.element.body):
 text=' | '.join(t.text for t in b.iter() if t.tag.endswith('}t') and t.text)
 if text: lines.append(f'[{i}] {text}')
for p0 in d.paragraphs:
 if p0.style.name.startswith(('Heading','Title','Título')): headings.append(p0.text)
(out/'texto.txt').write_text('\n'.join(lines),encoding='utf-8')
(out/'titulos.txt').write_text('\n'.join(headings),encoding='utf-8')
print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest()); print('Párrafos',len(d.paragraphs),'Tablas',len(d.tables),'Imágenes',len(d.inline_shapes))
base=Document(root/'docs/versiones/2026-10-19_1632_cap1-7.docx')
a=[p.text for p in base.paragraphs]; b=[p.text for p in d.paragraphs]
import difflib
(out/'diferencias-con-19oct.txt').write_text('\n'.join(difflib.unified_diff(a,b,fromfile='19oct',tofile='vigente',n=2)),encoding='utf-8')
print('Comparación texto párrafos igual:',a==b)
