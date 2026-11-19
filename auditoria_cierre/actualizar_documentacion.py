"""Integra evidencias existentes y del cierre sin regenerar Taller ni inventar resultados.

Reejecutable: sustituye capítulos seleccionados, conserva PUDS, manual, CASE y manual de usuario.
"""
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "DocumentoSoftware2"
fin = json.loads((DOC / "recursos/finanzas.json").read_text(encoding="utf8"))


def dinero(n):
    return f"{n:,.0f}".replace(",", " ")


def tabla(cabecera, filas):
    return "\n| " + " | ".join(map(str,cabecera)) + " |\n| " + " | ".join(["---"] * len(cabecera)) + " |\n" + "".join(
        "| " + " | ".join(str(x).replace("|", "/") for x in fila) + " |\n" for fila in filas) + "\n"


path = DOC / "capitulos.md"
texto = path.read_text(encoding="utf8")


def reemplazar(n, cuerpo):
    global texto
    patron = rf"(?ms)^# {n}\. .*?(?=^# (?:\d+\.|Bibliografía)|\Z)"
    texto, total = re.subn(patron, lambda _: cuerpo.strip() + "\n\n", texto, count=1)
    if total != 1:
        raise RuntimeError(f"No se encontró el capítulo {n}")


# Actualizar referencias activas; los proveedores de comparación se describen en el capítulo 11.
texto = texto.replace("AWS EC2 con Linux y Docker", "Azure VM con Linux y Docker")
texto = texto.replace("Neon, AWS, Vercel", "Neon, Azure, Vercel").replace("Vercel y AWS", "Vercel y Azure")
texto = texto.replace("| Amazon Web Services | EC2 con Linux y Docker |", "| Microsoft Azure | VM con Linux y Docker |")
texto = texto.replace("DSU Tecnología y Gestión Ambiental S.R.L.", "Residata S.R.L. (en constitución)")
texto = texto.replace("Los estándares con los que puede certificarse la calidad del software son", "Las referencias de calidad empleadas son")
texto = texto.replace("ISO 9001, IEEE 730 o CMMI |", "Sistema de gestión ISO 9001; no se acredita certificación del equipo |")
texto = texto.replace("según 2.5.4", "según 3.5.4")
texto = texto.replace("La aplicación en AWS", "La aplicación en Azure").replace("la aplicación en AWS", "la aplicación en Azure")

reemplazar(6, '''# 6. Infraestructura para la producción de software

## 6.1. Topología y entornos

El sistema se implementa como monolito modular Django con frontend React separado. La API se aloja en Azure VM, región Mexico Central, detrás de Caddy y Gunicorn; la aplicación React está en Vercel y PostgreSQL permanece en Neon, São Paulo. Las tablas operativas y analíticas comparten una base de datos; no son dos motores independientes. El sitio corporativo es otro proyecto estático, distinto de la aplicación DSU.

El entorno de cierre usa PostgreSQL 18 propio y efímero en loopback. El runner impone DATABASE_URL local antes de cargar Django; no usa Neon para pruebas con escritura. Python local es 3.13; Docker/CI mantienen 3.12. Esta diferencia de entorno se declara en las evidencias, no se presenta la ejecución local como Linux.

## 6.2. Herramientas y utilización real

| Actividad | Herramienta | Aplicación y evidencia |
| --- | --- | --- |
| Configuración y versiones | Git y GitHub | Repositorio privado; rama cierre-software2-20261118; línea base y rollback en auditoria_cierre/00_inventario_y_linea_base.md |
| Planeación | Gantt, PERT y COCOMO II | paps.md y estimaciones.json; estimaciones, no horas ejecutadas |
| Modelado CASE | Enterprise Architect | Los tres .eapx se abrieron por API nativa; conteos en enterprise_architect_todos.json. No equivale a revisar visualmente todos los objetos |
| Calidad de código | Ruff, oxlint y TypeScript | pyproject.toml y scripts frontend; comandos y salida en evidencias de cierre |
| Pruebas | pytest y navegador aislado | Ejecuciones nuevas y JUnit en auditoria_cierre/05_ejecuciones_pruebas |
| Entrega continua | GitHub Actions | .github/workflows/ci.yml; configuración versionada, no implica un push o despliegue de esta rama |
| Despliegue | Docker Compose, Caddy y Vercel | backend/deploy/compose.azure.yml y sitio-residata/preparar_publicacion.py |
| Monitoreo | Azure Monitor | Evidencia histórica de disponibilidad en docs/auditoria-fase-final/qa_url/azure_disponibilidad.txt |
| Respaldo | pg_dump / pg_restore | scripts/respaldo.sh y ensayo aislado del cierre, si cuenta con acta de resultado |

## 6.3. Accesos, respaldo y control de cambios

Las credenciales no forman parte del paquete de entrega. Por decisión del titular, backend/.env es una excepción en el repositorio privado; antes de cualquier publicación del repositorio se requiere rotación, retirada y limpieza de historial. El respaldo de cambios previos del cierre está fuera del repositorio. No se hicieron cambios en datos compartidos de Neon.

La cuenta Vercel disponible en este equipo no posee los proyectos existentes. El titular indicó que realizará la publicación; los cambios locales no se presentan como desplegados. El portal devolvió 404 inicialmente y volvió a HTTP 200 en la comprobación final; la versión pública aún conserva afirmaciones comerciales y cifras anteriores que debe actualizar el titular.
''')

reemplazar(7, '''# 7. Sitio web corporativo

## 7.1. Empresa y estado de publicación

Residata S.R.L. es la denominación propuesta de una sociedad en constitución. El producto piloto es el sistema DSU-UAGRM. La app https://dsu-uagrm.vercel.app responde HTTP 200 y la API exige autenticación. El portal corporativo https://residata-bolivia.vercel.app devolvió inicialmente HTTP 404 y en la reverificación del cierre respondió HTTP 200 en once rutas/recursos. No se atribuye esa recuperación a un despliegue de esta sesión. La versión pública aún afirma facturación habilitada y conserva la ronda anterior de Bs 170 000; la corrección local distingue propuestas y actualiza las cifras. El titular publicará esta versión.

## 7.2. Contenidos y canales

| Página | Finalidad | Implementación |
| --- | --- | --- |
| Inicio | Empresa, producto y demostración | HTML estático, capturas identificadas como demo |
| Planes | Propuesta de monetización | Precios propuestos; sin contratación ni cuotas automáticas implementadas |
| Novedades y RSS | Versiones y actualizaciones | novedades.json y feed.xml |
| Soporte | FAQ, horarios y estado | Asistente de reglas; no IA generativa; respuesta opaca no se declara verificación de salud |
| Contacto | Solicitar demostración | FormSubmit a rekteado@gmail.com; envío real no repetido durante QA |
| Privacidad y términos | Tratamiento y propuesta contractual | Borradores sujetos a revisión y formalización |
| Marketing y pitch | Material promocional y financiero | Piezas locales y PDF, sin campaña comercial acreditada |

El asistente deriva consultas a un correo mediante un identificador de ticket generado en el navegador. Eso no equivale a un sistema persistente de tickets ni a atención humana en vivo. La confirmación de envío tampoco acredita recepción y respuesta por el destinatario.

## 7.3. Verificación y límites

La publicación local se prepara con preparar_publicacion.py, excluyendo documentos internos y configuraciones de herramientas. La prueba probar_sitio.py recorre páginas en 1440 y 390 píxeles, registra respuestas y desbordamiento, no utiliza perfiles personales y bloquea peticiones externas. Los resultados efectivos se conservan en auditoria_cierre/05_ejecuciones_pruebas/sitio/.

No se anuncian offline, sensores IoT, suscripciones automáticas ni facturación habilitada como capacidades del piloto. Constituyen evolución y formalización futuras. Los objetivos SLA comerciales no son mediciones de disponibilidad mensual.

<!-- fig: DocumentoSoftware2/recursos/sitio/inicio-1440.png | Portal corporativo en su captura histórica del 18 de noviembre -->
<!-- fig: DocumentoSoftware2/recursos/sitio/asistente-1440.png | Asistente de reglas y derivación por correo -->
<!-- fig: DocumentoSoftware2/recursos/qr_sitio.png | URL pública del portal; actualización de contenido pendiente por el titular -->
''')

# Conservar el análisis de competidores y añadir números reproducibles sin inventar validación de demanda.
inicio = texto.index("# 8.")
fin8 = texto.index("# 9.", inicio)
mercado = texto[inicio:fin8].split("## 8.6.")[0]
mercado += '''## 8.6. Dimensionamiento y monetización propuesta

Se emplean 343 municipios, de los que 43 cuentan con relleno sanitario, y 48 universidades como universo de referencia. Las fuentes se registran en recursos/finanzas.json. No son clientes contratados ni una encuesta de disposición a pagar. TAM y SAM son escenarios de cobertura comercial, no demanda demostrada.

'''
mercado += tabla(["Indicador", "Bs/año"], [["TAM", dinero(fin["tam_bs"])], ["SAM", dinero(fin["sam_bs"])], ["Ingresos brutos año 5, escenario base", dinero(fin["som_bs_anio5"])]])
mercado += '''Los precios mensuales propuestos son Campus Bs 2 900 y Red Bs 7 500; implementación Bs 9 000 y Bs 18 000. Inicial es una oferta freemium propuesta. El escenario base supone 50 % de clientes anuales a diez mensualidades y 50 % mensuales a doce, sin contratos o ventas acreditados. Los límites por plan todavía no se implementan automáticamente.

## 8.7. Proyección financiera y sensibilidad

'''
mercado += tabla(["Año", "Clientes Campus/Red", "Ingresos netos", "Egresos", "Flujo", "Acumulado"],
    [[a['anio'], f"{a['clientes_campus']}/{a['clientes_red']}", dinero(a['ingreso_neto']), dinero(a['egresos']), dinero(a['flujo']), dinero(a['acumulado'])] for a in fin['anios']])
mercado += f"El VAN al 15 % es Bs {dinero(fin['van'])} y la TIR operativa es {fin['tir']} %. El equilibrio estimado es {fin['equilibrio']['clientes']} clientes Campus equivalentes. El flujo se vuelve positivo en el año {fin['anio_flujo_positivo']} y el acumulado se recupera en el año {fin['anio_recuperacion']}. No representan resultados reales de una empresa ni retorno garantizado.\n\n"
mercado += tabla(["Escenario de clientes", "VAN al 15 %", "Déficit máximo"], [[k, dinero(v['van']), dinero(v['deficit_maximo'])] for k,v in fin['escenarios'].items()])
mercado += '''La sensibilidad varía los clientes finales al 70 %, 100 % y 130 % de la hipótesis base. No se considera que la reducción o aumento de clientes tenga probabilidad demostrada. El supuesto de ocho clientes por VM requiere medición. El modelo contable simplifica impuestos y no incluye intereses de un crédito.

La validación comercial pendiente consiste en entrevistar responsables de compras y operación, registrar tamaño, presupuesto y disposición a pagar, y contrastar precios con cartas de intención reales. No se han inventado entrevistas ni contratos.

<!-- fig: DocumentoSoftware2/recursos/web/finanzas_ingresos_egresos.png | Proyección de ingresos y egresos con descuento anual incorporado -->
<!-- fig: DocumentoSoftware2/recursos/web/finanzas_flujo_acumulado.png | Flujo acumulado del escenario base -->
'''
reemplazar(8, mercado)

suite_path=ROOT/'auditoria_cierre/05_ejecuciones_pruebas/regresion_final.xml'
if not suite_path.exists():suite_path=ROOT/'auditoria_cierre/05_ejecuciones_pruebas/regresion_corregida.xml'
suite = next(ET.parse(suite_path).getroot().iter('testsuite')).attrib
pruebas = '''# 9. Pruebas en el software

## 9.1. Objetivo y flujo de prueba del PUDS

Se busca descubrir defectos con entradas válidas, inválidas, límites y conflictos de permisos y concurrencia. Siguiendo el flujo de prueba del Proceso Unificado, se planificaron riesgos, se diseñaron casos vinculados a RF/CU, se implementaron fixtures y pruebas, se ejecutaron integración y sistema y se evaluaron los resultados conservando defectos y regresión (Jacobson et al., 2000, capítulo 11).

| Actividad | Aplicación real | Evidencia |
| --- | --- | --- |
| Planificar | Riesgos de integridad y los 13 puntos | auditoria_cierre/01_plan_y_dependencias.md |
| Diseñar | Sector incompatible, reenvío y conexiones simultáneas | test_integridad_cierre.py; test_concurrencia_cierre.py |
| Implementar | PostgreSQL propio y datos sintéticos | auditoria_cierre/ejecutar_aislado.py |
| Integración | API, persistencia, auditoría, ETL y modelo | apps/*/tests/ y reportes JUnit |
| Sistema | Navegación y exportaciones | escenarios API y recorridos de navegador aislado |
| Evaluar | Fallos antes, correcciones y regresión | reproduccion_controlada.xml y regresion_corregida.xml |

## 9.2. Reproducción y regresión del cierre

La reproducción controlada previa registró cinco fallos: sector incompatible, reenvío entre tandas, inicio simultáneo de ETL, inicio simultáneo de entrenamiento y doble asignación de personal. Se conservaron los resultados anteriores a la corrección. La prueba inicial tuvo además errores de limpieza por el trigger de auditoría; se corrigió únicamente el arnés de test para limpiar su base sintética. La segunda reproducción controlada no tuvo esos errores de infraestructura.

Se reprodujo además un error de precisión: 0,005 multiplicado por un factor 0,7 se persistía como 0,003 al pasar por coma flotante, frente al resultado decimal redondeado 0,004. La normalización ahora conserva Decimal; los cuantiles de detección de atípicos usan float solo como cálculo estadístico no persistido. Se conservan la prueba fallida anterior y su regresión. La concurrencia de asignación se verifica separadamente para personal y vehículos.

'''
pruebas += f"La regresión corregida registra {suite['tests']} pruebas, {suite['failures']} fallos y {suite['errors']} errores, en {suite['time']} segundos sobre Windows y PostgreSQL 18 local. El código está en una rama con cambios locales; no es una ejecución de producción ni un nuevo resultado Linux. Los controles posteriores al cierre se consultan en la matriz de evidencia.\n\n"
pruebas += '''Las pruebas concurrentes crean conexiones PostgreSQL independientes, comprueban sus PID y sincronizan los participantes con una barrera. No se confunde una segunda llamada secuencial con concurrencia real. Se añadieron bloqueos transaccionales de PostgreSQL para serializar arranques y asignación.

La demo aislada completa login, planificación, asignación, apertura, vaciado, omisión, cierre, ETL, predicción y exportación. El navegador recorre dieciséis pantallas de cuatro roles. La carga HTTP de doce clientes virtuales durante sesenta segundos registró 531 peticiones sin errores y 156 vaciados confirmados frente a 156 persistidos. Utiliza identidades compartidas de lectura y escritura: no son doce personas reales ni una medición de producción. El reporte conserva mediana, p95, máximos y límites.

## 9.3. Caja negra y casos de uso

<!-- resultados api -->

Los resultados del marcador anterior son históricos y se conservan como tales. Las nuevas pruebas no se ejecutan contra Neon. El alta y la auditoría deben deshacerse juntas ante fallo de bitácora; el test de reversión conserva ese criterio como regresión.

## 9.4. Caja blanca sobre diagramas de secuencia

Los tres casos siguientes utilizan las secuencias exportadas desde el modelo y la matriz conservada en caja_blanca_secuencias.json. Las cifras corresponden a ese modelo de mensajes; no deben confundirse con la complejidad completa de cada función Python tras incorporar bloqueos transaccionales. Los resultados de caminos se contrastan con los tests identificados, sin extrapolarlos a cobertura total.

'''
for c in json.loads((ROOT/'docs/auditoria-fase-final/pruebas/caja_blanca_secuencias.json').read_text(encoding='utf8')):
    cu=c['cu']
    pruebas += f"### 9.4.{[9,15,28].index(cu)+1}. CU{cu} {c['nombre']}\n\n"
    pruebas += f"<!-- figh: generador/figuras/fase_final/c9_seq_cu{cu:02d}.png | Secuencia de CU{cu} y sus rechazos -->\n\n"
    pruebas += f"<!-- fig: generador/figuras/fase_final/c9_grafo_cu{cu:02d}.png | Grafo de mensajes del CU{cu} -->\n\n"
    pruebas += f"N={c['N']}; E={c['E']}; predicados={c['P']}. V(G)=E−N+2={c['E']}-{c['N']}+2={c['V']}; P+1={c['P']}+1={c['V']}; regiones={c['regiones']}.\n\n"
    pruebas += tabla(['Nodo','Mensaje o condición','Referencia'],c['nodos'])
    pruebas += "Matriz de conexiones: una fila y columna por nodo; 1 indica arista.\n\n"
    pruebas += tabla(['Nodo']+list(range(1,c['N']+1)), [[i+1]+fila for i,fila in enumerate(c['matriz'])])
    pruebas += tabla(['Camino','Secuencia','Prueba vinculada','Resultado histórico'], [[x['n'],x['camino'],x['prueba'],x['resultado']] for x in c['caminos']])
pruebas += '''## 9.5. Listas de comprobación adaptadas

Se adaptan las categorías de inspección de Myers, Sandler y Badgett (2012), capítulo 3. Son criterios de revisión, no una certificación del producto.

| Categoría genérica | Comprobación DSU | Resultado y evidencia |
| --- | --- | --- |
| Datos y declaraciones | Variables definidas y tipos coherentes | Ruff; tipos Decimal en cantidades; no implica precisión predictiva real |
| Cálculo | Conversión kg/g y agregados | test_etl_estandariza_deriva_variables_y_excluye_duplicados |
| Comparaciones y límites | Horizonte fuera de rango, capacidad y periodos | test_rechazos_prediccion; test_caminos_registro; comparación de periodos |
| Flujo de control | Estados de jornada y caminos de rechazo | test_flujo_completo_de_jornada y caja blanca anterior |
| Interfaz y autorización | Roles y sector del usuario | test_roles_y_sesion; test_supervisor_no_opera_sectores_ajenos |
| Entrada/salida | PDF y XLSX válidos | test_reportes_exportan_y_quedan_en_bitacora |
| Concurrencia | Arranque y asignación simultáneos | test_concurrencia_cierre, conexiones independientes |
| Integridad | Sector/ruta y duplicado entre tandas | test_integridad_cierre; test_etl_detecta_reenvio_en_tanda_posterior |

## 9.6. Herramientas por URL, móviles y seguridad

Las evidencias históricas de qa_url/resumen.json registran Observatory A+ para app y sitio, W3C sin errores y SSL Labs A+/A para el sitio y A+ para la API. Las corridas Lighthouse corregidas tienen sus propios archivos. Estos resultados son de la fecha conservada; la recuperación posterior a HTTP 200 no permite declarar esos grados de seguridad vigentes sin repetir sus herramientas.

El registro móvil histórico tiene 12 casos aprobados en perfiles iPhone 13 y Pixel 7, sin desbordamiento. Es emulación de navegador, no certificación de equipos físicos. ZAP fue pasivo y conserva advertencias; no acredita pentest completo. La revisión local actual no envía formularios ni ataca servicios externos.

## 9.7. Rendimiento, alfa y aceptación beta

RTR11 no cumplió el límite de 15 segundos con 512 puntos en la medición histórica contra Neon. La medición nueva del cierre en PostgreSQL local y API dentro del mismo proceso sí cumple los límites medidos: sus valores exactos, recuentos y rollback están en rendimiento_local.txt/json. No incluye la latencia de Azure a Neon ni la red del teléfono; no autoriza a declarar cumplimiento productivo. Las latencias móviles de producción siguen requiriendo contraste con RTR1. La carga HTTP de doce usuarios con escrituras se ejecuta solo en la demo aislada y se registra en carga_12_usuarios.txt; su resultado no se presume si hay un error en ese archivo. No se declara capacidad de ocho clientes por VM sin medirla.

La alfa corresponde a comprobaciones técnicas del equipo. La beta y la aceptación por DSU son pendientes externos; el anexo C es un formato sin firmas ficticias. El modelo Random Forest fue validado con datos sintéticos; su calidad institucional requiere datos y evaluación reales.
'''
reemplazar(9, pruebas)

# Conservar estrategia de marketing y agregar material realmente disponible.
pos=texto.index('# 10.');end=texto.index('# 11.',pos)
marketing=texto[pos:end].split('## 10.5.')[0]+'''## 10.5. Material digital y estado de difusión

Existen afiche, banner y publicaciones cuadradas en sitio-residata/marketing/ y recursos/sitio/marketing-*.png. Se revisaron las piezas visuales; no se han acreditado campañas pagadas, conversiones, clientes o ventas. Las cifras de pesaje y predicción corresponden a demostración y deben acompañarse de esa aclaración. La URL promocional volvió a responder HTTP 200; la actualización de las piezas y de las condiciones sigue a cargo del titular.

<!-- fig: DocumentoSoftware2/recursos/sitio/marketing-banner.png | Banner comercial con interfaz de demostración -->
<!-- fig: DocumentoSoftware2/recursos/sitio/marketing-post-kilos.png | Publicación de demostración sin atribuir resultados institucionales -->
'''
reemplazar(10,marketing)

operacion='''# 11. Puesta en marcha y operación

## 11.1. Arquitectura comprobada y comparación económica

API en Azure VM Mexico Central, Caddy, Gunicorn y Docker; PostgreSQL en Neon São Paulo; aplicación React en Vercel. La consulta de Azure de la sesión anterior confirmó la VM dsu-api y suscripción Azure for Students. El sitio corporativo es independiente: inicialmente devolvió 404 y en la reverificación final devolvió 200, con contenido anterior a las correcciones locales. No se cambió el proveedor de base de datos.

<!-- figh: generador/figuras/fase_final/c7_despliegue.png | Topología de Azure, Vercel y Neon -->

La comparación utiliza precios de referencia del 18/11/2026 y 730 horas/mes para 2 vCPU, 4 GB, disco de 32 GB e IPv4. Son hipótesis de presupuesto; no facturas. AWS y GCP se conservan solo como alternativas comparadas.

'''
operacion+=tabla(['Proveedor/región','USD/mes','Fuente registrada'],[[n['proveedor']+' / '+n['region'],n['total_usd'],n['fuente']] for n in fin['nube']])
operacion+=f"La plataforma de referencia totaliza USD {fin['plataforma_usd']} al mes, Bs {fin['plataforma_bs']}, para Azure, Neon, Vercel y Monitor. Si se añaden dos licencias Power BI Pro de USD 14, la referencia pasa a USD 102,19 al mes. El crédito educativo no se trata como ingreso recurrente garantizado.\n\n"
operacion+='''## 11.2. Instalación, despliegue y reversión

El runbook actualizado está en backend/deploy/README.md. La configuración productiva se mantiene exclusivamente en la VM. El comando Compose aplica migraciones normales al arrancar; requiere coordinación y respaldo antes de desplegar contra datos compartidos. El cierre local no ha desplegado estos cambios ni ejecutado migraciones en Neon. El titular realizará la publicación web.

CI comprueba Ruff, migraciones pendientes, pytest, build frontend y ensamblado del sitio. La existencia del workflow no acredita una ejecución reciente en GitHub. Se conservan JUnit locales y el reporte histórico del contenedor por separado.

## 11.3. Disponibilidad y monitoreo

La evidencia histórica de Monitor contiene 19/19 sondeos de API, 15/15 de app y 16/16 de sitio: 50 resultados totales, no 50 de API. Es una muestra de minutos y no una disponibilidad mensual. Los objetivos comerciales de 99 % Campus y 99,5 % Red deben acordarse contractualmente y medirse durante el periodo completo.

El indicador del portal no declara éxito por un 404 o 500; una respuesta opaca se marca no verificable. Se conservaron seis pruebas de esa función. No se crean recursos cloud pagos para cerrar el documento.

## 11.4. Continuidad, respaldo y restauración

El servicio respaldo ejecuta pg_dump diario y retiene catorce días en la VM. Una copia en el mismo servidor no protege contra pérdida de ese servidor. La copia independiente y la restauración productiva requieren procedimiento y verificación. El ensayo del cierre se realiza exclusivamente en PostgreSQL local con datos sintéticos; sus resultados, cuando aprobados, quedan en restauracion.json. No acredita que un dump productivo sea recuperable ni mide RTO institucional.

RPO objetivo: 24 horas; RTO objetivo: dos horas. Permanecen objetivos hasta medirlos en el entorno correspondiente. No se aplican restauraciones, limpieza ni entrenamiento sobre Neon durante el cierre.

## 11.5. Licencia y propuesta de condiciones

Se propone licencia institucional no exclusiva y sin costo para DSU, separada de las suscripciones comerciales proyectadas. No se acredita firma de convenio, constitución concluida, registro SENAPI ni facturación electrónica habilitada. Los textos locales de términos y privacidad son borradores para revisión, con encargados Azure, Neon, Vercel y FormSubmit identificados.

Los tokens JWT viven en localStorage, con access de 30 minutos y refresh de diez horas configurables. La API vuelve a comprobar permisos y alcance. No se afirma ausencia de vulnerabilidades por tener TLS y cabeceras. ETL y entrenamiento bajo demanda aún usan hilos web: un reinicio puede interrumpirlos; se recomienda ejecución por comandos controlados y supervisión hasta disponer de cola persistente.
'''
reemplazar(11,operacion)

funding=f'''# 13. Financiamiento

## 13.1. Necesidad de capital y uso de fondos

Con mezcla de 50 % anual y 50 % mensual, el déficit máximo proyectado es Bs {dinero(fin['financiamiento']['deficit_maximo'])}. Se propone solicitar Bs {dinero(fin['financiamiento']['monto_solicitado'])}, incorporando contingencia y redondeo. Sustituye la referencia inicial de Bs 170 000, que no contemplaba el descuento anual. No se ha obtenido ni comprometido ese financiamiento.

'''
funding+=tabla(['Destino','Bs propuestos'],[[u['destino'],dinero(u['bs'])] for u in fin['uso_fondos']])
funding+='''## 13.2. Fuentes y condiciones por verificar

Se estudian concursos de capital semilla, FOCASE/BDP, ángeles y fondos presemilla. Las referencias históricas a Incuba Unión y otras convocatorias no acreditan convocatoria vigente, elegibilidad ni adjudicación. Un crédito requiere tasa, plazo, garantías y servicio de deuda; ese escenario no se presenta como equivalente al aporte de capital y debe recalcularse antes de solicitarlo.

## 13.3. Inversionista y valoración ilustrativa

'''
inv=fin['inversionista_ilustrativo']
funding+=f"Una hipótesis de Bs {dinero(inv['aporte'])} por 15 % implica valoración post-money de Bs {dinero(inv['valoracion_post_money'])}. La ilustración de salida al año cinco supone resultado antes de IUE multiplicado por tres, caja acumulada, deuda cero y ningún dividendo. El cobro estimado de esa participación sería Bs {dinero(inv['cobro_estimado'])}, con TIR anual ilustrativa de {inv['tir_anual_pct']} %. Es diferente de la TIR operativa del proyecto. No hay comprador, inversión ni salida acreditados; puede perderse el capital.\n\n"
funding+='''## 13.4. Pitch y riesgos

El pitch local contiene once láminas. El HTML y su PDF deben conservar las mismas cifras que recursos/finanzas.json. La publicación del pitch y su QR depende del actualización pública de Residata por el titular. Riesgos: adopción y disposición a pagar sin validar, dependencia de nube y tipo de cambio, capacidad no medida, disponibilidad comercial no acreditada, formalización y costos de soporte.

<!-- fig: DocumentoSoftware2/recursos/qr_pitch.png | Enlace público del pitch; actualización pendiente por el titular -->
'''
if re.search(r'(?m)^# 13\.',texto):reemplazar(13,funding)
else:texto=texto.replace('# Bibliografía',funding+'\n# Bibliografía',1)
if 'Myers, G. J., Sandler, C., y Badgett, T. (2012)' not in texto:
    texto=texto.replace('# Bibliografía', '''# Bibliografía

Myers, G. J., Sandler, C., y Badgett, T. (2012). The Art of Software Testing (3.ª ed.). Wiley.

Microsoft. (2026). Azure Retail Prices API y Azure Monitor. Referencias de planificación consultadas el 18/11/2026; ver recursos/finanzas.json.

Mozilla, Google, Qualys y W3C. (2026). HTTP Observatory, Lighthouse, SSL Labs y Nu Validator. Resultados conservados en docs/auditoria-fase-final/qa_url/; no acreditan disponibilidad actual.
''',1)
path.write_text(texto,encoding='utf8')
p=DOC/'paps.md';t=p.read_text(encoding='utf8').replace('AWS EC2','Azure VM').replace('Amazon EC2','Azure VM')
t=t.replace('2.186,31','1.192,56').replace('2 186,31','1 192,56')
if '### 1.4.2. Conciliación de costos del cierre' not in t:
    nota = '''
### 1.4.2. Conciliación de costos del cierre

El presupuesto inicial valora desarrollo y herramientas como planificación, no gastos efectivamente pagados. La referencia operativa revisada es USD 74,19/mes de plataforma más USD 28 para dos usuarios Power BI Pro: USD 102,19, aproximadamente Bs 1 192,56 al cambio de planificación 11,67. La proyección empresarial y su capital de trabajo están en los capítulos 8 y 13; no se suman indistintamente al costo de desarrollar el piloto.
'''
    t=t.replace('## 1.5.',nota+'\n## 1.5.',1)
# Insertar la nota antes del capítulo siguiente, no al final del archivo si contiene anexos.
nota_existente=re.search(r'(?ms)^### 1\.4\.2\. Conciliación de costos del cierre\n.*?(?=^## |\Z)',t)
if nota_existente:
    contenido=nota_existente.group().strip()
    t=t[:nota_existente.start()]+t[nota_existente.end():]
    t=t.replace('## 1.5.',contenido+'\n\n## 1.5.',1)
t=t.replace('según 2.','según 3.')
p.write_text(t,encoding='utf8')
print('Capítulos revisados: 6, 7, 8, 9, 10, 11 y 13; conservados PUDS, SQAP, CASE y manual por rol.')
