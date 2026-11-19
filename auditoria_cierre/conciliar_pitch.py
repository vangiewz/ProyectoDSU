"""Concilia contenido financiero del pitch a partir del JSON; no altera precios ni registra inversiones."""
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
f=json.loads((ROOT/'DocumentoSoftware2/recursos/finanzas.json').read_text(encoding='utf8'))
p=ROOT/'sitio-residata/pitch/index.html'
t=p.read_text(encoding='utf8')
def num(n):return f'{n:,.0f}'.replace(',',' ')
t=re.sub(r'ronda de Bs [\d ]+\.', 'ronda propuesta de Bs '+num(f['financiamiento']['monto_solicitado'])+'.',t)
t=re.sub(r'Buscamos Bs [\d ]+', 'Buscamos Bs '+num(f['financiamiento']['monto_solicitado']),t)
t=re.sub(r'<div><b>[\d,]+</b><span>clientes Campus para el equilibrio', '<div><b>'+str(f['equilibrio']['clientes']).replace('.',',')+'</b><span>clientes Campus para el equilibrio',t)
t=re.sub(r'<b(?: style="[^"]*")?>Bs [\d ]+(?:mil)?</b><span>VAN al 15 %', '<b style="font-size:2rem">Bs '+num(f['van'])+'</b><span>VAN al 15 %',t)
t=re.sub(r'<b>[\d,]+ %</b><span>TIR', '<b>'+str(f['tir']).replace('.',',')+' %</b><span>TIR operativa',t)
t=t.replace('TIR operativa operativa','TIR operativa')
section=re.search(r'(<section class="lamina clara" aria-label="La ronda">)(.*?)(</section>)',t,re.S)
body=section.group(2)
body=re.sub(r'<tbody>.*?</tbody>', '<tbody>'+''.join('<tr><td>'+u['destino']+'</td><td class="n">'+num(u['bs'])+'</td></tr>' for u in f['uso_fondos'])+'</tbody>',body,flags=re.S)
body=re.sub(r'equilibrio operativo con [\d,.]+ clientes', 'equilibrio operativo con '+str(f['equilibrio']['clientes']).replace('.',',')+' clientes',body)
body=body.replace('Capital semilla no reembolsable: concurso', 'Alternativa por verificar, sin adjudicación: concurso')
body=body.replace('Fideicomiso de Capital Semilla del BDP para el resto, a cinco años.', 'FOCASE/BDP: elegibilidad, tasa y servicio de deuda pendientes; no equivalen a aporte de capital.')
t=t[:section.start(2)]+body+t[section.end(2):]
t=t.replace('En producción desde el 18/11/2026','Piloto técnico desplegado; empresa en constitución')
t=t.replace('El plan Inicial sin costo deja medir una sede; la predicción y el mapa se pagan.', 'Propuesta por validar: Inicial gratuito y planes Campus/Red. Cuotas automáticas y contratación no implementadas en el piloto.')
t=t.replace('Precios con impuestos de ley incluidos.', 'Precios propuestos; facturación no habilitada.')
t=t.replace('Supuestos: IVA 13 %', 'Supuestos: 50 % anual a 10 meses y 50 % mensual; IVA 13 %')
t=t.replace('que diseñaron, programaron, probaron y desplegaron el sistema completo.', 'responsables del proyecto compartido. La autoría individual del código previo a la unificación no es verificable con el Git disponible.')
p.write_text(t,encoding='utf8')
print('Pitch conciliado con recursos/finanzas.json; pendiente regenerar PDF y verificar formato.')
