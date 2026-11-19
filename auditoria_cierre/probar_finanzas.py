"""Comprobaciones reproducibles de fórmula y conciliación, sin validar demanda ni asesoría fiscal."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parent.parent
m=runpy.run_path(str(ROOT/'DocumentoSoftware2/finanzas.py'))
f=json.loads((ROOT/'DocumentoSoftware2/recursos/finanzas.json').read_text(encoding='utf8'))
assert m['proyeccion']()==f['anios']
assert sum(u['bs'] for u in f['uso_fondos'])==f['financiamiento']['monto_solicitado']
assert round(sum(a['flujo']/1.15**a['anio'] for a in f['anios']))==f['van']
assert -min(a['acumulado'] for a in f['anios'])==f['financiamiento']['deficit_maximo']
assert abs(sum(a['flujo']/(1+f['tir']/100)**a['anio'] for a in f['anios'])) < 1000
todo_mensual=m['proyeccion']({'fraccion_clientes_anuales':0})
todo_anual=m['proyeccion']({'fraccion_clientes_anuales':1})
assert todo_anual[0]['ingreso_bruto'] < f['anios'][0]['ingreso_bruto'] < todo_mensual[0]['ingreso_bruto']
assert f['escenarios']['conservador']['van']<f['escenarios']['base']['van']<f['escenarios']['optimista']['van']
out=ROOT/'auditoria_cierre/05_ejecuciones_pruebas/finanzas.json'
out.write_text(json.dumps({'resultado':'APROBADO','comprobaciones':7,'modelo':'mitad mensual y mitad anual a diez meses',
    'capital_propuesto':f['financiamiento']['monto_solicitado'],'van':f['van'],'tir_operativa':f['tir'],
    'limite':'No acredita ventas, aceptación de precios ni retorno garantizado'},ensure_ascii=False,indent=2),encoding='utf8')
print('7 comprobaciones financieras aprobadas.')
