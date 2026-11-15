from pathlib import Path
import pypdfium2 as pdfium,json
from PIL import Image,ImageDraw
out=Path('docs/auditoria-2026-10-28'); doc=pdfium.PdfDocument(out/'vigente.pdf'); print('Páginas PDF:',len(doc),flush=True)
texts=[];meta=[]
folder=out/'paginas';folder.mkdir(exist_ok=True)
for start in range(0,len(doc),20):
 sheet=Image.new('RGB',(1500,1740),'#ccc'); draw=ImageDraw.Draw(sheet)
 for k in range(min(20,len(doc)-start)):
  p=doc[start+k];t=p.get_textpage().get_text_range();texts.append(t);meta.append({'page':start+k+1,'chars':len(t)})
  im=p.render(scale=.46).to_pil().convert('RGB');im.thumbnail((290,395));x=k%5*300;y=k//5*435
  sheet.paste(im,(x+(300-im.width)//2,y+22));draw.text((x+6,y+3),str(start+k+1),fill='black');p.close()
 sheet.save(folder/f'plancha-{start//20:02}.jpg')
(out/'paginas.txt').write_text('\n'.join(f'\n=== PÁGINA PDF {i+1} ===\n{t}' for i,t in enumerate(texts)),encoding='utf-8')
(out/'paginas.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print('Páginas con poco texto:',[r for r in meta if r['chars']<40])
