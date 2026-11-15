from pathlib import Path
from docx import Document
from PIL import Image,ImageOps,ImageDraw
import io,json
root=Path.cwd(); out=root/'docs/auditoria-2026-10-28'; folder=out/'figuras';folder.mkdir(exist_ok=True)
d=Document(root/'docs/Documento_Taller_de_Grado_I_Grupo_8.docx'); cap='portada'; rows=[]
for p in d.paragraphs:
 if p.style.name=='Caption': cap=p.text
 for blip in p._p.xpath('.//a:blip'):
  rid=blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
  if rid:
   part=d.part.related_parts[rid]; im=Image.open(io.BytesIO(part.blob)).convert('RGB'); idx=len(rows)
   im.save(folder/f'{idx:03}.png'); rows.append({'i':idx,'caption':cap,'size':im.size})
for start in range(0,len(rows),12):
 sheet=Image.new('RGB',(1600,1400),'#ddd'); draw=ImageDraw.Draw(sheet)
 for k,row in enumerate(rows[start:start+12]):
  im=Image.open(folder/f"{row['i']:03}.png"); im.thumbnail((390,410)); x=(k%4)*400;y=(k//4)*465
  sheet.paste(im,(x+(400-im.width)//2,y+32));draw.text((x+6,y+3),f"{row['i']:03} {row['caption'][:51]}",fill='black')
 sheet.save(folder/f'plancha-{start//12:02}.jpg')
(out/'figuras.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Figuras extraídas:',len(rows))
