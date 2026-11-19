"""QA técnico de todas las páginas y render de muestras para inspección visual humana."""
import hashlib
import json
from pathlib import Path
import re

import pymupdf

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'auditoria_cierre/05_ejecuciones_pruebas/pdf'
OUT.mkdir(exist_ok=True)
file=ROOT/'Entregables/Software_2/Documento_Software_2_DSU.pdf'
docx=ROOT/'Entregables/Software_2/Documento_Software_2_DSU.docx'
with pymupdf.open(file) as pdf:
    covers={};blank=[];outside=[];broken=[]
    for i,p in enumerate(pdf):
        t=p.get_text();m=re.findall(r'CAPÍTULO (\d+):',t)
        if len(m)==1 and 'Estudiantes:' in t:covers[int(m[0])]=i+1
        if len(t.strip())<10:blank.append(i+1)
        if any(s in t for s in ['Error! Bookmark','¡Error! Marcador']):broken.append(i+1)
        assert any(abs(p.rect.width-w)<2 and abs(p.rect.height-h)<2 for w,h in [(612,792),(792,612)]),(i+1,'Tamaño no carta')
        rectangles=[b[:4] for b in p.get_text('blocks')]
        for im in p.get_images(full=True):rectangles.extend(p.get_image_rects(im[0]))
        for rect in rectangles:
            if rect[0]<-1 or rect[1]<-1 or rect[2]>p.rect.width+1 or rect[3]>p.rect.height+1:outside.append(i+1)
    assert set(covers)==set(range(1,14)),covers
    assert not blank and not outside and not broken,(blank,outside,broken)
    samples=sorted(set([1,2]+list(covers.values())+[n+1 for n in covers.values()]+[
        i+1 for i,p in enumerate(pdf) if 'Matriz de conexiones:' in p.get_text()][:3]))
    for n in samples:pdf[n-1].get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False).save(OUT/('pagina-%03d.png'%n))
    result=dict(paginas=len(pdf),caratulas=covers,paginas_vacias=blank,elementos_fuera_pagina=outside,campos_rotos=broken,
        renderizadas=samples,pdf_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),docx_sha256=hashlib.sha256(docx.read_bytes()).hexdigest(),
        metodo='Word nativo a PDF, comprobaciones de todas las páginas y render PyMuPDF; inspección visual representativa')
    (OUT/'revision.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))
