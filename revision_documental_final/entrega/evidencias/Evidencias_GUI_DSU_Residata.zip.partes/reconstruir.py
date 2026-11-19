from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent;m=json.loads((r/'manifest.json').read_text(encoding='utf8'));p=r.parent/m['original']
if p.exists():
 assert p.stat().st_size==m['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],'El destino existente difiere; conservarlo antes de reconstruir.'
 print('Archivo existente verificado:',p.name)
else:
 temp=p.with_suffix(p.suffix+'.reconstruyendo')
 with temp.open('wb') as out:
  for part in m['partes']:
   data=(r/part['archivo']).read_bytes()
   assert len(data)==part['bytes'] and hashlib.sha256(data).hexdigest()==part['sha256'],'Parte alterada'
   out.write(data)
 assert temp.stat().st_size==m['bytes'] and hashlib.sha256(temp.read_bytes()).hexdigest()==m['sha256'],'Hash final incorrecto'
 temp.rename(p);print('Reconstruido y verificado:',p.name)
