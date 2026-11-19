"""Cierra registros a partir de evidencias efectivas; no publica ni convierte bloqueos en logros."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'auditoria_cierre'
EVID=OUT/'05_ejecuciones_pruebas'
pdf=json.loads((EVID/'pdf/revision.json').read_text(encoding='utf8'))
assert pdf['pdf_sha256']==hashlib.sha256((ROOT/'Entregables/Software_2/Documento_Software_2_DSU.pdf').read_bytes()).hexdigest()
suite=next(ET.parse(EVID/'regresion_final.xml').getroot().iter('testsuite')).attrib
assert suite['failures']==suite['errors']=='0'
ui=json.loads((EVID/'demo_ui/resultados.json').read_text(encoding='utf8'))
sitio=json.loads((EVID/'sitio/resultados.json').read_text(encoding='utf8'))
assert len(ui['casos'])==len(sitio['casos'])==16
carga=(EVID/'carga_12_usuarios.txt').read_text(encoding='utf8')
assert '531 peticiones, 0 errores' in carga and '156 vaciados confirmados, 156 guardados' in carga and '❌' not in carga
perf=json.loads((EVID/'rendimiento_local.json').read_text(encoding='utf8'))
assert perf['exit_code']==0 and perf['rollback_verificado']

rows=[
(1,'PAPS','CUMPLE','DocumentoSoftware2/paps.md; Entregables/Material_Drive/02_PAPS.pdf','Alcance, métricas, presupuesto y cronograma; costos distinguidos de gastos reales.','Estimaciones y responsabilidades no son horas ni actuaciones acreditadas.'),
(2,'Proceso PUDS','CUMPLE','DocumentoSoftware2/capitulos.md, capítulo 2; generador/fase2/datos.py; modelo_uml/','Fases, 34 CU y artefactos del mismo sistema.','No atribuir fechas de iteración ni autoría sin registros.'),
(3,'Manual de calidad','CUMPLE','DocumentoSoftware2/capitulos.md, capítulo 3; 03_SQAP.pdf','Plan, roles, controles, métricas, defectos y resultados reales.','No es certificación ISO ni nivel CMMI; actas vacías son formatos.'),
(4,'Herramientas CASE','CUMPLE','modelo_uml/*.eapx; enterprise_architect_todos.json; capítulos 2/4','Los tres modelos abrieron por API nativa; exportaciones y generadores localizables.','Lectura estructural, no inspección visual exhaustiva de cada objeto.'),
(5,'Aspectos legales','PARCIAL','capítulo 5; auditoria_cierre/legal/','Nombre unificado, propuesta de licencia y matriz de trámites; 174 componentes inventariados.','Registro, NIT, SENAPI, firmas y revisión final de obligaciones no acreditados. PENDIENTE EXTERNO cuando corresponda.'),
(6,'Infraestructura','CUMPLE','backend/deploy/compose.azure.yml; deploy/README.md; .github/workflows/ci.yml','Topología, configuración, pruebas aisladas y procedimiento de reversión concretos.','Cambios de esta rama no desplegados; CI nuevo no ejecutado en GitHub.'),
(7,'Sitio corporativo publicado','PARCIAL','sitio-residata/dist/; sitio/resultados.json; estado_publico_final.json','Versión local corregida, 16 recorridos y materiales preparados.','Reverificación: once rutas/recursos HTTP 200, pero con oferta y cifras anteriores. La actualización la publicará el titular; no se atribuye la recuperación a esta sesión.'),
(8,'Mercado y valorización','PARCIAL','capítulo 8; finanzas.py; recursos/finanzas.json','Competidores, hipótesis, TAM/SAM, precios, escenarios y sensibilidad.','No hay entrevistas, ventas ni disposición a pagar acreditadas; capacidad por cliente es supuesto.'),
(9,'Pruebas','CUMPLE','capítulo 9; 05_ejecuciones_pruebas/; matriz_trazabilidad.json','Regresión nueva, fallos antes/después, conexiones concurrentes, UI/API, carga, restauración y tres matrices de caja blanca.','Cumple como evidencia académica; no acredita pentest completo, aceptación de todos los RNF ni rendimiento productivo.'),
(10,'Marketing','CUMPLE','sitio-residata/marketing/; recursos/sitio/marketing-*.png; capítulo 10','Material digital revisado y responsive, con propuesta comercial diferenciada.','No se acreditan campañas, conversiones ni ventas; publicación dependiente del punto 7.'),
(11,'Puesta en marcha','PARCIAL','capítulo 11; 06_despliegue_y_operacion.md; restauracion.json','Runbook Azure, rollback, salud, demo y restauración aislada comprobados.','Publicación de correcciones, copia externa y recuperación productiva no demostradas; hilos web conservan riesgo de interrupción.'),
(12,'Software como producto','PARCIAL','backend/ y frontend/; demo_ui/resultados.json; regresion_final.xml','Piloto técnico funcional: jornada, vaciado, ETL, reportes y predicción con persistencia.','No es SaaS comercial terminado ni producción institucional aceptada; Power BI publicado y validación real pendientes.'),
(13,'Financiamiento','CUMPLE','capítulo 13; recursos/finanzas.json; pitch/Residata_pitch.pdf','Propuesta reproducible de Bs 200.000, escenarios, uso de fondos y retorno ilustrativo separado.','No es capital obtenido ni garantía de rentabilidad; ofertas y elegibilidad de terceros por confirmar.'),
]
matrix='''# Matriz final de los trece requisitos

La hoja con notas pertenece a otro grupo; no se asignan sus resultados a DSU. Estado del alcance académico/local al cierre; no implica certificación ni aceptación institucional.

|N|Requisito|Estado|Ruta exacta relativa a la raíz|Criterio verificado|Pendiente o límite|
|---|---|---|---|---|---|
'''+''.join('|'+ '|'.join(map(str,r))+'|\n' for r in rows)
matrix+='\nResultado: 8 CUMPLE, 5 PARCIAL y 0 NO CUMPLE. CUMPLE se refiere al alcance indicado en su fila, no a una operación comercial/institucional al 100 %.\n'
(OUT/'02_matriz_13_requisitos.md').write_text(matrix,encoding='utf8')

final=f'''# Auditoría final del cierre local DSU y Residata

## Veredicto

Se ejecutaron correcciones de código, pruebas, finanzas, documentación y preparación de publicación. No es otra auditoría sin implementación. El piloto funciona en el recorrido aislado probado; no se declara 100 % de los trece puntos ni lanzamiento comercial completo. Resultado académico/local: 8 CUMPLE, 5 PARCIAL y 0 NO CUMPLE, según 02_matriz_13_requisitos.md.

La hoja con 68 puntos era de otro grupo. No se usa como nota del proyecto. La autoría individual de Carlos previa a la unificación sigue NO VERIFICABLE con el Git disponible. Las responsabilidades declaradas en PAPS no se convierten en autoría de cada función.

## Evidencia nueva

- Regresión PostgreSQL aislado: {suite['tests']} pruebas, 0 fallos, 0 errores, {suite['time']} segundos; regresion_final.xml/json/txt.
- Antes de corregir: cinco fallos en reproduccion_controlada.xml y un fallo de precisión en reproduccion_precision.xml. Se conservan los errores del primer arnés como tales, no se ocultan.
- Demo: 16 pantallas de cuatro roles, login UI real y flujo integrado por API en el navegador de prueba; demo_ui/resultados.json. No se dice que cada formulario se haya rellenado manualmente.
- Carga: 12 hilos HTTP, 60 s, 531 peticiones, 0 errores y 156 vaciados confirmados/persistidos; carga_12_usuarios.txt. Son clientes virtuales con identidades compartidas, no doce participantes reales.
- Rendimiento: 500 puntos añadidos y más de 100.000 registros; todas las filas con límite del comando cumplieron localmente. Ver valores exactos y recuentos de rollback en rendimiento_local.txt/json. API en proceso local, sin red Azure–Neon; no certifica RNF productivos.
- Restauración: dump sintético restaurado en otra base local, coincidencia de todas las tablas, claves foráneas validadas y trigger activo; restauracion.json. No restaura producción ni mide RTO institucional.
- Sitio: 16 recorridos a 1440 y 390 px y seis escenarios de función de salud. No se enviaron formularios reales.
- Caja blanca: matrices, aristas, E−N+2, P+1 e independencia verificados para CU9, CU15 y CU28; caja_blanca_verificada.json. Es el modelo de mensajes, no cobertura total del código Python.
- EA: tres archivos abiertos por API, sin guardar cambios; enterprise_architect_todos.json.
- Finanzas: siete comprobaciones y conciliación de web/pitch/documento; finanzas.json. Déficit Bs 162.817, capital propuesto Bs 200.000, VAN operativo Bs 120.674 y TIR operativa 42,7 %. Son proyecciones.
- Documento: {pdf['paginas']} páginas, trece carátulas, cero páginas vacías, campos rotos o elementos fuera de página detectados. Exportación Word nativa y muestreo visual de PNG; revisión.json vincula hashes de Word y PDF. El renderer empaquetado falló por LibreOffice ausente; no se afirma que ese método funcionó.

## Fases y criterios de aceptación

|Fase|Estado|Criterios aprobados y evidencia|Criterios pendientes / siguiente acción|
|---|---|---|---|
|0 Inventario y recuperación|COMPLETA|Rama, commit base, respaldo privado con SHA256; matrices 27 RF y 46 RNF/RTR/RCM.|No usar el patch privado como entregable; contiene configuración privada.|
|1 Calidad del producto|PARCIAL|Seis defectos reproducidos corregidos, transacción de auditoría y concurrencia de personal/vehículo; regresión y demo aprobadas.|Hilos web no durables; recorrido de todos los formularios/variantes y producción institucional no cerrado. Riesgo interno explícito.|
|2 Sitio y marketing|PARCIAL|Versión local, rutas, responsive, salud, pitch y material preparados.|Publicación a cargo del titular; URL corporativa recuperada a 200, pero aún con contenido anterior a corregir.|
|3 Pruebas y seguridad|PARCIAL|Suite, caja blanca, errores negativos, carga, precisión, restauración y navegador aprobados en entorno aislado.|ZAP disponible es histórico y pasivo; no se repitió pentest ni toda la matriz de navegadores/RNF productivos.|
|4 Infraestructura y puesta en marcha|PARCIAL|Runbook Azure, CI revisado, rollback preparado, restauración sintética y salud de solo lectura.|No se desplegó la rama; copia independiente y recuperación productiva sin evidencia nueva.|
|5 Legal|PARCIAL|Capítulo coherente, inventario de licencias y borradores/matriz listos.|Formalización, revisión competente, convenio y firmas reales: PENDIENTE EXTERNO.|
|6 Mercado y financiamiento|PARCIAL|Cálculos, descuento anual, escenarios, capital, valoración y pitch conciliados.|Demanda, precios aceptados y capacidad por cliente no validados; no inventar entrevistas.|
|7 PAPS/PUDS/SQAP/CASE|COMPLETA|Documentación preservada y actualizada, normas sin certificación ficticia y modelos nativos comprobados.|No acredita ejecución de todas las revisiones previstas ni autoría individual completa.|
|8 Entrega unificada|PARCIAL|Word/PDF de 13 capítulos, manuales, pitch, código sin .env real y manifiesto del paquete.|Los QR/URLs responden, pero enlazan una versión pública anterior; revisión final humana de consigna original aconsejada.|
|9 Defensa y aceptación|PARCIAL|Guion, preguntas difíciles, demo reproducible, matrices y formatos preparados.|Ensayo oral de los integrantes y aceptación/firma institucional no realizados.|

Cada fase conserva rollback en el commit base y respaldo privado descritos en 00_inventario_y_linea_base.md; no hay commits ni push del cierre. Los nuevos archivos son identificables en esta rama. No se ejecutó restauración, seed, entrenamiento ni pruebas con escritura contra Neon.

## Cambios principales y archivos

- config/concurrencia.py: bloqueos transaccionales PostgreSQL entre workers sin nuevas tablas.
- operations/serializers/jornada.py: sector y ruta existente coherentes; services/jornada.py: asignación serializada.
- analytics/services/etl.py: reenvíos entre tandas y normalización Decimal; tests de error binario.
- prediction/services/entrenamiento.py: arranque y numeración de versiones serializados.
- audit/views/base.py: alta/edición y bitácora en la misma transacción; prueba de reversión.
- scripts/carga.py: HTTP 4xx ya no se cuentan como éxito y el script devuelve error si incumple criterios.
- sitio-residata/js/site.js: respuestas 404/500 y opacas no se declaran servicio sano; propuesta comercial sin factura habilitada ficticia.
- sitio-residata/preparar_publicacion.py y publicar.sh: solo recursos públicos y proyecto previamente vinculado, sin cambio automático de alias.
- DocumentoSoftware2/finanzas.py y ensamblar.py: descuento anual, escenarios, financiación y trece capítulos con matrices y QR.
- .github/workflows/ci.yml: CD espera tres jobs, exige dos secretos y reintenta salud; no se ejecutó un despliegue.

Las rutas de código anteriores son relativas a gestion-residuos-dsu/backend salvo las que nombran otra carpeta. El paquete incluye código actualizado sin historial ni configuración privada. backend/.env sigue siendo la excepción autorizada en el repositorio privado; no debe publicarse el repositorio sin aplicar la rotación/limpieza acordadas.

## Bloqueos y trabajo que no se oculta

Solo los trámites, cuentas, autorizaciones y firmas de terceros se listan en 07_pendientes_externos.md. Internamente siguen pendientes una solución durable para tareas largas, comprobación productiva de capacidad/latencia, automatización de todos los formularios y revisión completa de obligaciones de licencias. El proyecto se entrega como piloto funcional con estas limitaciones, no como SaaS multiempresa terminado.

La actualización pública la realizará el titular por instrucción explícita. El sitio pasó de 404 a HTTP 200 en una reverificación de once rutas/recursos, sin despliegue del agente; siguen públicas la oferta no corregida y la ronda anterior. No se le pide otra autorización para el mismo trabajo local. No se han enviado mensajes, celebrado contratos, registrado entidades, comprado suscripciones ni atribuido resultados del otro grupo.
'''
(OUT/'09_auditoria_final.md').write_text(final,encoding='utf8')
with (OUT/'04_bitacora_cambios.md').open('a',encoding='utf8') as f:
    f.write(f'\n\n## Cierre de registros\nRegresión final: {suite["tests"]} aprobadas en {suite["time"]} s. Carga: 531 peticiones sin errores y 156 vaciados sin pérdida. Medición posterior a Decimal con rollback comprobado. Word/PDF: {pdf["paginas"]} páginas y trece capítulos. Ver 09_auditoria_final.md para criterios pendientes; no se marca 100 %.\n')
print('Registros finales actualizados: 8 CUMPLE, 5 PARCIAL, 0 NO CUMPLE; límites explícitos.')
