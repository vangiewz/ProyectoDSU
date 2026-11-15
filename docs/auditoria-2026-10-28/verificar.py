from pathlib import Path
from docx import Document
import re,json,sys,hashlib
import pypdfium2 as pdfium
root=Path.cwd(); out=root/'docs/auditoria-2026-10-28'; d=Document(root/'docs/Documento_Taller_de_Grado_I_Grupo_8.docx'); old=Document(root/'docs/versiones/2026-10-19_1632_cap1-7.docx')
# Exclude indices: compare from Introducción after index tables, using style headings.
def body(doc):
 blocks=list(doc.element.body); start=next(i for i,b in enumerate(blocks) if ''.join(b.itertext())=='!IMPOSSIBLE') if False else None
 for i,b in enumerate(blocks):
  ts=''.join(t.text or '' for t in b.iter() if t.tag.endswith('}t'))
  if ts=='Introducción': start=i;break
 return [''.join(t.text or '' for t in b.iter() if t.tag.endswith('}t')) for b in blocks[start:]]
print('Texto cuerpo y tablas igual al 19/10:',body(d)==body(old))
head=[p.text for p in d.paragraphs if p.style.name.startswith('Heading')]
for prefix in ['5.4.','6.2.','7.5.']:
 ids=[int(m[1]) for h in head if h.startswith(prefix) and (m:=re.search(r'CU(\d+)\.',h))];print(prefix,len(ids),'faltantes',sorted(set(range(1,39))-set(ids)))
caps=[p.text for p in d.paragraphs if p.style.name=='Caption']
for kind,count in [('Figura',198),('Tabla',154)]:
 nums=[int(m[1]) for c in caps if (m:=re.match(kind+r'\s+(\d+)',c))];print(kind,len(nums),'faltantes',sorted(set(range(1,count+1))-set(nums)),'duplicados',[i for i in set(nums) if nums.count(i)>1])
print('Marcadores error:',[p.text for p in d.paragraphs if re.search(r'Error!|¡Error!|TODO|TBD|pendiente',p.text,re.I)][:8])
print('Tablas CU:',sum(1 for t in d.tables if t.cell(0,0).text=='Caso de Uso'))
book=pdfium.PdfDocument(out/'vigente.pdf')
for n in [158,190,242,246,252,269,280,335]:
 p=book[n-1];p.render(scale=1.8).to_pil().save(out/'paginas'/f'pagina-{n}.png')
needles=['primera fase del proyecto','base de datos en producción','única desnormalización','tamaños','7.2.6. Clases de control','5.4.20. CU20','5.4.29. CU29','5.4.30. CU30']
for needle in needles:
 found=[]
 for i in range(35,len(book)):
  if needle.lower() in book[i].get_textpage().get_text_range().lower(): found.append(i+1)
 print(needle,found)
