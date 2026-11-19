"""EA COM: modelo independiente de fase final; no sobrescribe el modelo previo."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'generador/fase2'))
from ea_util import Modelo
from componentes import D, SUBSISTEMAS, validar

FIG = ROOT / 'generador/figuras/fase_final'


def exportar(m, d, name, fuente='120'):
    d.DiagramObjects.Refresh()
    for o in d.DiagramObjects:
        # Fijar fuente en el modelo: el PNG debe ser legible al imprimirlo.
        o.SetStyleEx('font', 'Arial')
        o.SetStyleEx('fontsz', fuente)
        o.Update()
    m.exportar(d, str(FIG / name))


def general(m, p):
    d = m.diagrama(p, 'Arquitectura del sistema DSU', 'Component')
    d.ExtendedStyle += 'UseAlias=1;'
    d.Update()
    central = m.elemento(p, 'Sistema web DSU-UAGRM', 'Component', 'source')
    m.colocar(d, central, 300, 250, 230, 90)
    for i, paq in enumerate(D.PAQUETES):
        left = i < 4
        x, y = (20 if left else 620), 35 + (i % 4) * 140
        nombre = f"{paq['n']}. " + paq['nombre']
        e = m.elemento(p, nombre, 'Package')
        e.Alias = f"{paq['n']}. " + ['Usuarios', 'Topología', 'Residuos', 'Logística',
                                   'Analítica', 'Cartografía', 'Predicción', 'Administración'][i]
        e.Update()
        m.colocar(d, e, x, y, 220, 110)
        c = m.conectar(central, e, 'Dependency')
        # Cada dependencia termina en el borde del cuerpo del paquete, a la
        # altura de su centro (antes la de Logística quedaba en el vacío).
        m.quebrar(d, c, [(265 if left else 595, y + 70)])
    oltp = m.elemento(p, 'PostgreSQL en Neon\nEstructura transaccional', 'Component', 'OLTP')
    olap = m.elemento(p, 'PostgreSQL en Neon\nHechoResiduo y vistas bi_*', 'Component', 'OLAP')
    m.colocar(d, oltp, 300, 450, 230, 95)
    m.colocar(d, olap, 300, 640, 230, 95)
    m.conectar(central, oltp, 'Dependency', nombre='Django ORM / PostgreSQL-TLS')
    m.conectar(olap, oltp, 'Dependency', nombre='ETL: lectura de origen')
    c = m.conectar(central, olap, 'Dependency', nombre='analítica')
    m.quebrar(d, c, [(575, 330), (575, 685)])
    exportar(m, d, 'c8_general.png')


def _lineas(texto, ancho=30):
    """Líneas que ocupará un texto en una caja de unos `ancho` caracteres."""
    import textwrap
    return sum(max(1, len(textwrap.wrap(t, ancho))) for t in texto.split('\n'))


def subsistema(m, root, spec):
    """Diagrama de componentes por nodos reales del despliegue (lámina cap. 8
    p. 9 adaptada): cliente en Vercel, API en Azure VM y PostgreSQL en Neon."""
    from componentes import CAPAS, dependencias
    n = spec['n']
    p = m.paquete(f"8.2.{n}. {D.PAQUETES[n-1]['nombre']}", root)
    d = m.diagrama(p, f'Subsistema {n}', 'Component')
    W, X = 800, 20
    ext_cli = [e for e in spec['externos'] if e['desde'] == 'cliente']
    ext_olap = [e for e in spec['externos'] if e['desde'] == 'olap']
    fondo, medio, frente = [], [], []

    def caja(nombre, tipo, est, x, y, w, h, contenedor=False, nivel=None):
        e = m.elemento(p, nombre, tipo, est)
        o = m.colocar(d, e, x, y, w, h)
        (nivel if nivel is not None else fondo if contenedor else frente).append(o)
        return e

    def rotulo(texto, x, y, w, h):
        # Las etiquetas de conectores salen con la fuente pequeña de EA; los
        # protocolos se escriben como texto del diagrama, al tamaño del resto.
        t = caja('', 'Text', '', x, y, w, h)
        t.Notes = texto.replace(chr(10), chr(13) + chr(10))
        t.Update()

    # Cliente web
    ancho_cli = W - 360 if ext_cli else W
    cli = caja('Cliente web: SPA React (Vercel)', 'Component', '', X, 40, ancho_cli, 150, True)
    k = len(spec['cliente'])
    bw = min(230, (ancho_cli - 40 - 20 * (k - 1)) // k)
    for i, name in enumerate(spec['cliente']):
        caja(name.split('/')[-1], 'Component', '', X + 20 + i * (bw + 20), 95, bw, 70)
    externos = {}
    for e in ext_cli + ext_olap:
        if e['nombre'] not in externos:
            lee = ext_olap and e['nombre'] == ext_olap[0]['nombre']
            nombre = e['nombre'] + ('\nlee bi_* por PostgreSQL/TLS\n(rol de solo lectura)' if lee else '')
            externos[e['nombre']] = caja(nombre, 'Component', 'external', X + W - 230, 60, 230, 110)
    for e in ext_cli:
        m.conectar(cli, externos[e['nombre']], 'Dependency')
        rotulo(e['etiqueta'].replace(': ', '\n'), X + ancho_cli + 5, 50, 125, 55)

    # Servidor de aplicaciones: capas reales y sus dependencias por imports.
    y_srv = 290
    textos = {}
    for capa in CAPAS:
        items = spec['servidor'][capa]
        if not items:
            continue
        por_app = {}
        for it in items:
            app, archivo = it.split('/')
            por_app.setdefault(app, []).append(archivo)
        textos[capa] = '\n'.join(f"{app}/{capa}/: " + ', '.join(fs) for app, fs in por_app.items())
    alto = {c: 40 + 19 * _lineas(t) for c, t in textos.items()}
    fila1 = max(alto.get('views', 0), alto.get('serializers', 0))
    fila2 = max(alto.get('services', 0), alto.get('models', 0))
    extra = 80 if spec.get('artefacto') else 0
    h_srv = 60 + fila1 + 60 + fila2 + 20 + extra
    srv = caja('API Django REST Framework (Azure VM, Linux, Docker)', 'Component', '', X, y_srv, W, h_srv, True)
    m.conectar(cli, srv, 'Dependency')
    rotulo('«JSON/HTTPS»\nJWT Bearer, TCP 443', X + (ancho_cli + W) // 4 + 15, 205, 250, 55)
    cw = (W - 60) // 2
    pos = {'views': (X + 20, y_srv + 50), 'serializers': (X + 40 + cw, y_srv + 50),
           'services': (X + 20, y_srv + 110 + fila1), 'models': (X + 40 + cw, y_srv + 110 + fila1)}
    cajas = {}
    for capa, texto in textos.items():
        x, y = pos[capa]
        cajas[capa] = caja(texto, 'Artifact', 'source', x, y, cw, alto[capa])
    for a, b in dependencias(spec):
        m.conectar(cajas[a], cajas[b], 'Dependency')
    if spec.get('artefacto'):
        art = caja(spec['artefacto'], 'Artifact', 'artifact', X + 20, y_srv + h_srv - extra - 10, cw, 65)
        m.conectar(cajas['services'], art, 'Dependency')

    # Neon: estructuras OLTP y OLAP lógicas de la misma base.
    y_db = y_srv + h_srv + 90
    th = 55

    def bloque(nombres, est, y):
        # Tres columnas; dos si algún nombre de tabla no cabe en la caja.
        cols = 3 if max(map(len, nombres)) <= 24 else 2
        tw = (W - 70 - (cols - 1) * 10) // cols
        filas = -(-len(nombres) // cols)
        h = 50 + filas * (th + 15)
        cont = caja('Estructura transaccional' if est == 'OLTP' else 'Estructura analítica',
                    'Component', est, X + 20, y, W - 40, h, nivel=medio)
        for i, t in enumerate(nombres):
            caja(t, 'Component', 'view' if t.startswith('bi_') else 'table',
                 X + 35 + (i % cols) * (tw + 10), y + 45 + (i // cols) * (th + 15), tw, th)
        return cont, h

    y = y_db + 45
    oltp, h1 = bloque(spec['oltp'], 'OLTP', y)
    olap, h2 = (None, 0)
    if spec['olap']:
        olap, h2 = bloque(spec['olap'], 'OLAP', y + h1 + 20)
    h_db = 45 + h1 + (20 + h2 if olap else 0) + 15
    db = caja('Neon: PostgreSQL 18 (São Paulo)', 'Component', 'database', X, y_db, W, h_db, True)
    m.conectar(srv, db, 'Dependency')
    rotulo('PostgreSQL/TLS 5432\n(Django ORM)', X + W // 2 + 15, y_srv + h_srv + 15, 250, 55)
    for e in ext_olap:
        c = m.conectar(externos[e['nombre']], olap, 'Dependency', nombre='')
        xr = X + W + 25
        m.quebrar(d, c, [(xr, 115), (xr, y + h1 + 20 + h2 // 2)])
    # Orden Z de EA: el Sequence más bajo se dibuja al frente.
    for nivel, seq in ((fondo, 100), (medio, 50), (frente, 1)):
        for o in nivel:
            o.Sequence = seq
            o.Update()
    exportar(m, d, f'c8_sub{n}.png', fuente='130')


def main():
    validar()
    FIG.mkdir(parents=True, exist_ok=True)
    ruta = ROOT / 'modelo_uml/DSU-FaseFinal.eapx'
    if ruta.exists():
        import shutil
        shutil.copy2(ruta, ruta.with_suffix('.eapx.bak'))
    m = Modelo(str(ruta))
    try:
        p = m.paquete('Capítulo 8 Implementación')
        general(m, p)
        for s in SUBSISTEMAS:
            subsistema(m, p, s)
        import ea_cap7
        p7 = m.paquete('Actualización del despliegue de producción')
        ea_cap7.despliegue(m, p7, lambda name: str(FIG / name))
        import caja_blanca
        caja_blanca.diagramas(m, m.paquete('Capítulo 9 Caja blanca'), FIG)
        import secuencias_caja_blanca
        secuencias_caja_blanca.diagramas(m, m.paquete('Software 2 Caja blanca sobre secuencias'), FIG)
    finally:
        m.cerrar()
    print('EA: 9 diagramas de componentes y despliegue exportados')


if __name__ == '__main__':
    main()
