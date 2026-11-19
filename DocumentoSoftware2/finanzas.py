"""Modelo financiero de Residata S.R.L. (cap. 8 estudio de mercado, cap. 11 puesta en marcha, cap. 13 financiamiento).
Reproducible: python finanzas.py -> recursos/finanzas.json y gráficos en recursos/web/.
Tarifas de nube consultadas el 18/11/2026: Azure Retail Prices API, AWS Price List API y páginas oficiales de GCP.
Los supuestos comerciales (clientes, precios, sueldos) se declaran en SUPUESTOS y se publican con el resultado."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
TC = 11.67           # Bs por USD, BCB 14–16/11/2026 (mismo valor que el cap. 10 de Taller)
H = 730              # horas por mes

# ---------------------------------------------------------------- nube (2 vCPU, 4 GB, 32 GB SSD, IPv4)
NUBE = [
    dict(proveedor='Microsoft Azure (adoptado)', region='Mexico Central', vm='B2als v2', vm_h=0.0414, disco='SSD Premium P4 32 GB', disco_mes=5.807412, ip_h=0.005,
         fuente='Azure Retail Prices API'),
    dict(proveedor='Amazon Web Services', region='São Paulo (sa-east-1)', vm='t3.medium', vm_h=0.0672, disco='EBS gp3 32 GB', disco_mes=0.152 * 32, ip_h=0.005,
         fuente='AWS Price List API'),
    dict(proveedor='Google Cloud', region='São Paulo (southamerica-east1)', vm='e2-medium', vm_h=0.0531852, disco='PD balanceado 32 GB', disco_mes=0.000205479 * H * 32, ip_h=0.005,
         fuente='cloud.google.com, páginas de precios de Compute Engine, discos y red'),
]
for n in NUBE:
    n['vm_mes'] = round(n['vm_h'] * H, 2); n['disco_mes'] = round(n['disco_mes'], 2); n['ip_mes'] = round(n['ip_h'] * H, 2)
    n['total_usd'] = round(n['vm_mes'] + n['disco_mes'] + n['ip_mes'], 2); n['total_bs'] = round(n['total_usd'] * TC, 2)

AZ = NUBE[0]['total_usd']
PLATAFORMA = [  # costo mensual de operar la plataforma con un cliente (USD)
    ('Azure: VM, disco e IP de la API', AZ, 'Azure Retail Prices API'),
    ('Neon Launch: 100 CU-h y 2 GB', round(0.106 * 100 + 0.35 * 2, 2), 'neon.com/pricing'),
    ('Vercel Pro: un puesto (uso comercial)', 20.0, 'vercel.com/pricing'),
    ('Azure Monitor: disponibilidad de la API, 5 840 ejecuciones', round(5840 * 0.00055, 2), 'Azure Retail Prices API (USD 0,00055 por ejecución)'),
]
PLAT_USD = round(sum(x[1] for x in PLATAFORMA), 2)

# ---------------------------------------------------------------- mercado
MERCADO = dict(
    municipios=343, municipios_relleno=43, universidades_ceub=15, universidades_privadas=33,
    fuentes=['Diagnóstico Nacional de la Gestión Integral de Residuos Sólidos (MMAyA, 2025) e Inventario Nacional de Botaderos, citados por Correo del Sur (2026)',
             'Comité Ejecutivo de la Universidad Boliviana (CEUB), universidades del sistema',
             'Decretos de jerarquización de 33 universidades privadas (eju.tv)'])
PRECIO = {'Campus': 2900, 'Red': 7500}           # Bs por mes, impuestos incluidos
IMPL = {'Campus': 9000, 'Red': 18000}             # Bs pago único
TAM = (MERCADO['municipios'] * PRECIO['Red'] + (MERCADO['universidades_ceub'] + MERCADO['universidades_privadas']) * PRECIO['Campus']) * 12
SAM = (MERCADO['municipios_relleno'] * PRECIO['Red'] + (MERCADO['universidades_ceub'] + MERCADO['universidades_privadas']) * PRECIO['Campus']) * 12

# ---------------------------------------------------------------- supuestos de la proyección
SUPUESTOS = dict(
    clientes_fin_de_anio={'Campus': [2, 5, 9, 13, 17], 'Red': [1, 2, 4, 6, 8]},
    iva=0.13, it=0.03, iue=0.25, cargas_sociales=0.1671, aguinaldo=13 / 12, tasa_descuento=0.15,
    personal_mensual=[  # (rol, Bs/mes, años activos 1..5)
        ('Fundador: dirección y desarrollo', [4500, 7000, 9000, 9000, 9000]),
        ('Fundador: desarrollo y calidad', [4500, 7000, 9000, 9000, 9000]),
        ('Agente de soporte', [0, 3500, 3500, 3500, 3500]),
        ('Desarrollador adicional', [0, 0, 0, 9000, 9000])],
    marketing_anual=[18000, 24000, 30000, 30000, 30000],
    contador_mensual=700,
    constitucion=[('SEPREC: matrícula y gaceta', 647), ('SENAPI: búsqueda de signo PI-112', 75),
                  ('SENAPI: registro de programa de ordenador y gaceta', 210), ('Escritura de constitución (honorario notarial estimado)', 2000)],
    clientes_por_vm=8, neon_por_cliente_usd=round(0.106 * 50 + 0.35 * 2, 2))


def proyeccion():
    s = SUPUESTOS; anios = []
    prev = {'Campus': 0, 'Red': 0}
    for a in range(5):
        fin = {p: s['clientes_fin_de_anio'][p][a] for p in PRECIO}
        prom = {p: (prev[p] + fin[p]) / 2 for p in PRECIO}
        nuevos = {p: fin[p] - prev[p] for p in PRECIO}
        bruto_sus = sum(prom[p] * PRECIO[p] * 12 for p in PRECIO)
        bruto_impl = sum(nuevos[p] * IMPL[p] for p in PRECIO)
        bruto = bruto_sus + bruto_impl
        neto = bruto * (1 - s['iva'])
        it = bruto * s['it']
        clientes = sum(fin.values()); prom_total = sum(prom.values())
        vms = max(1, -(-clientes // s['clientes_por_vm']))
        nube = (PLAT_USD + (vms - 1) * AZ + prom_total * s['neon_por_cliente_usd']) * TC * 12
        personal = sum(m[a] for _, m in s['personal_mensual']) * 12 * (1 + s['cargas_sociales']) * s['aguinaldo']
        admin = s['contador_mensual'] * 12 + (sum(x[1] for x in s['constitucion']) if a == 0 else 0)
        egresos = nube + personal + s['marketing_anual'][a] + admin + it
        antes = neto - egresos
        iue = max(antes, 0) * s['iue']
        flujo = antes - iue
        anios.append(dict(anio=a + 1, clientes_campus=fin['Campus'], clientes_red=fin['Red'], ingreso_bruto=round(bruto), ingreso_neto=round(neto),
                          nube=round(nube), personal=round(personal), marketing=s['marketing_anual'][a], administracion=round(admin), it=round(it),
                          egresos=round(egresos), resultado_antes_iue=round(antes), iue=round(iue), flujo=round(flujo), vms=vms))
        prev = fin
    acum = 0
    for x in anios:
        acum += x['flujo']; x['acumulado'] = round(acum)
    return anios


def van(tasa, flujos, inversion):
    return -inversion + sum(f / (1 + tasa) ** (i + 1) for i, f in enumerate(flujos))


def tir(flujos, inversion):
    lo, hi = -0.99, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if van(mid, flujos, inversion) > 0: lo = mid
        else: hi = mid
    return mid


def equilibrio():
    """Clientes Campus equivalentes que cubren los egresos fijos mensuales del año 3 (equipo completo)."""
    s = SUPUESTOS
    fijos = (sum(m[2] for _, m in s['personal_mensual']) * (1 + s['cargas_sociales']) * s['aguinaldo'] + s['marketing_anual'][2] / 12
             + s['contador_mensual'] + PLAT_USD * TC)
    margen = PRECIO['Campus'] * (1 - s['iva'] - s['it']) - s['neon_por_cliente_usd'] * TC
    return dict(costos_fijos_mensuales=round(fijos), margen_por_cliente=round(margen), clientes=round(fijos / margen, 1))


def graficos(anios):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    azul, naranja, tinta, tinta2, fondo = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#fcfcfb'
    plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 11, 'axes.edgecolor': '#c9c8c2', 'axes.labelcolor': tinta2,
                         'xtick.color': tinta2, 'ytick.color': tinta2, 'axes.spines.top': False, 'axes.spines.right': False})
    x = [f"Año {a['anio']}" for a in anios]
    fmt = lambda v, _=None: '0' if round(v) == 0 else f"{v/1000:,.0f} mil".replace(',', '.')
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=220, facecolor=fondo); ax.set_facecolor(fondo)
    w = 0.36; pos = range(len(x))
    ax.bar([p - w / 2 - 0.01 for p in pos], [a['ingreso_neto'] for a in anios], w, color=azul, label='Ingresos netos de IVA')
    ax.bar([p + w / 2 + 0.01 for p in pos], [a['egresos'] for a in anios], w, color=naranja, label='Egresos')
    ax.set_xticks(list(pos), x); ax.yaxis.set_major_formatter(fmt); ax.set_ylabel('Bs por año')
    ax.grid(axis='y', color='#e6e5e0', linewidth=.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, loc='upper left', labelcolor=tinta)
    fig.tight_layout(); fig.savefig(R / 'recursos/web/finanzas_ingresos_egresos.png', facecolor=fondo); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=220, facecolor=fondo); ax.set_facecolor(fondo)
    ac = [0] + [a['acumulado'] for a in anios]
    ax.plot(['Inicio'] + x, ac, color=azul, linewidth=2, marker='o', markersize=6)
    ax.axhline(0, color=tinta2, linewidth=.8)
    for i, v in enumerate(ac):
        if i in (ac.index(min(ac)), len(ac) - 1):
            ax.annotate(fmt(v), (i, v), textcoords='offset points', xytext=(10, -4) if v < 0 else (0, 8), ha='left' if v < 0 else 'center', color=tinta, fontsize=10)
    ax.yaxis.set_major_formatter(fmt); ax.set_ylabel('Bs acumulados'); ax.grid(axis='y', color='#e6e5e0', linewidth=.6)
    fig.tight_layout(); fig.savefig(R / 'recursos/web/finanzas_flujo_acumulado.png', facecolor=fondo); plt.close(fig)


def tir_serie(flujos):
    """Tasa que anula el valor presente de los flujos de los años 1..5 (los años con pérdida van con signo negativo)."""
    lo, hi = -0.9, 10.0
    for _ in range(300):
        mid = (lo + hi) / 2
        if sum(f / (1 + mid) ** (i + 1) for i, f in enumerate(flujos)) > 0: lo = mid
        else: hi = mid
    return mid


if __name__ == '__main__':
    anios = proyeccion(); flujos = [a['flujo'] for a in anios]
    deficit = -min(0, min(a['acumulado'] for a in anios))
    monto = -(-deficit * 1.2 // 10000) * 10000  # déficit máximo acumulado + 20 % de contingencia, redondeado a 10 000
    r = SUPUESTOS['tasa_descuento']
    res = dict(tipo_cambio=TC, nube=NUBE, plataforma=[dict(concepto=c, usd=u, bs=round(u * TC, 2), fuente=f) for c, u, f in PLATAFORMA],
               plataforma_usd=PLAT_USD, plataforma_bs=round(PLAT_USD * TC, 2), mercado=MERCADO, precios=PRECIO, implementacion=IMPL,
               tam_bs=TAM, sam_bs=SAM, som_bs_anio5=anios[-1]['ingreso_bruto'], supuestos=SUPUESTOS, anios=anios, equilibrio=equilibrio(),
               financiamiento=dict(deficit_maximo=round(deficit), monto_solicitado=int(monto)),
               van=round(sum(f / (1 + r) ** (i + 1) for i, f in enumerate(flujos))), tir=round(tir_serie(flujos) * 100, 1),
               anio_flujo_positivo=next(a['anio'] for a in anios if a['flujo'] > 0),
               anio_recuperacion=next((a['anio'] for a in anios if a['acumulado'] >= 0), None))
    # Uso de fondos: el déficit de los años 1 y 2 repartido según la composición de sus egresos, más la contingencia
    a12 = [a for a in anios if a['anio'] <= 2]
    tot = sum(a['egresos'] for a in a12)
    partes = {'Equipo (sueldos y cargas)': sum(a['personal'] for a in a12), 'Marketing y ventas': sum(a['marketing'] for a in a12),
              'Infraestructura en la nube': sum(a['nube'] for a in a12), 'Constitución, contabilidad e impuestos': sum(a['administracion'] + a['it'] for a in a12)}
    uso = [dict(destino=k, bs=round(deficit * v / tot)) for k, v in partes.items()]
    uso.append(dict(destino='Contingencia (20 %)', bs=int(monto) - sum(u['bs'] for u in uso)))
    res['uso_fondos'] = uso
    (R / 'recursos/finanzas.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    graficos(anios)
    for n in NUBE: print(n['proveedor'], n['total_usd'], 'USD', n['total_bs'], 'Bs')
    print('Plataforma', PLAT_USD, 'USD/mes;', 'TAM', TAM, 'SAM', SAM)
    for a in anios: print({k: a[k] for k in ['anio','clientes_campus','clientes_red','ingreso_bruto','ingreso_neto','egresos','flujo','acumulado','vms']})
    print('Equilibrio', res['equilibrio'], '| Financiamiento', res['financiamiento'], '| VAN', res['van'], '| TIR', res['tir'], '| flujo+', res['anio_flujo_positivo'], '| recupera', res['anio_recuperacion'])
