"""Contrasta archivos realmente descargados por UI; no genera reportes por API."""
import ast
import datetime as dt
import json
from pathlib import Path
import re
from decimal import Decimal, ROUND_HALF_UP
import fitz
from openpyxl import load_workbook

OUT=Path(__file__).resolve().parent
MONTHS=['ene','feb','mar','abr','may','jun','jul','ago','sept','oct','nov','dic']

def same(ui,value):
    if value is None:return ui in ['','—']
    if isinstance(value,dt.datetime):value=value.date()
    if isinstance(value,dt.date):return ui==f'{value.day:02} {MONTHS[value.month-1]} {value.year}'
    if isinstance(value,(int,float,Decimal)):
        try:return abs(Decimal(ui.replace('.','').replace(',','.'))-Decimal(str(value)))<=Decimal('.005')
        except Exception:return False
    return str(value)==ui

results=[]
for file in sorted((OUT/'resultados').glob('*.json')):
    if file.name.startswith('consola'):continue
    data=json.loads(file.read_text(encoding='utf8'))
    if not isinstance(data,list):continue
    for row in data:
        if not isinstance(row,dict) or row.get('estado')!='APROBADO':continue
        detail=row.get('detalle')
        if isinstance(detail,str):
            try:detail=ast.literal_eval(detail)
            except Exception:continue
        if not isinstance(detail,dict) or 'archivos' not in detail:continue
        ui=detail['filas_ui']
        if ui and not isinstance(ui[0],list):continue
        files=[OUT/Path(x.replace('\\','/')) for x in detail['archivos']]
        xlsx=next(x for x in files if x.suffix=='.xlsx')
        pdf=next(x for x in files if x.suffix=='.pdf')
        wb=load_workbook(xlsx,data_only=False)
        ws=wb.active
        actual=[list(r) for r in ws.iter_rows(min_row=8,values_only=True)]
        cells=[]
        for i,(a,b) in enumerate(zip(ui,actual)):
            for j,(uv,xv) in enumerate(zip(a,b)):
                if not same(uv,xv):cells.append(dict(fila=i+8,columna=j+1,interfaz=uv,xlsx=str(xv)))
        count_equal=len(ui)==len(actual)
        formulas=[c.coordinate for rowcells in ws.iter_rows() for c in rowcells if c.data_type=='f']
        document=fitz.open(pdf);text='\n'.join(p.get_text() for p in document)
        title=str(ws['A3'].value or '')
        pdf_header=title in text
        # Las columnas largas se abrevian en PDF; controlar cifras de cada fila y título.
        missing=[]
        compact=''.join(text.split())
        for i,values in enumerate(actual):
            for j,value in enumerate(values):
                if isinstance(value,(float,Decimal)):
                    n=f'{value:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
                    # El PDF puede mostrar floats con un decimal; Decimal se emite con dos.
                    alternatives=[n,n.rstrip('0').rstrip(','),f'{value:,.1f}'.replace(',','X').replace('.',',').replace('X','.')]
                    if not any(x in compact for x in alternatives):missing.append(dict(fila=i+8,columna=j+1,valor=value))
        image=OUT/'descargas'/(pdf.stem+'-pagina1.png')
        document[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(image)
        results.append(dict(caso=row['id'],ejecucion=file.name,xlsx=xlsx.name,pdf=pdf.name,filas_ui=len(ui),filas_xlsx=len(actual),celdas_discrepantes=cells,
            formulas_inesperadas=formulas,pdf_paginas=len(document),titulo_pdf_coincide=pdf_header,cifras_no_localizadas_pdf=missing,
            estado='APROBADO' if count_equal and not cells and not formulas and pdf_header and not missing else 'FALLIDO'))
(OUT/'descargas/verificacion.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
for x in results:print(x['caso'],x['estado'],'filas',x['filas_ui'],'discrepancias',len(x['celdas_discrepantes']),'PDF',len(x['cifras_no_localizadas_pdf']))
