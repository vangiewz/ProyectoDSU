# Bit?cora de cierre

18/11/2026: le?das instrucciones completas; autorización para cambios locales y pruebas aisladas. Creada rama y respaldo privado con hash. Sin commits, cambios públicos o datos productivos. Creado runner de PostgreSQL propio que impone DATABASE_URL local y detiene su clúster al terminar.


## Fases 0 y 1

- Fase 0 COMPLETA como línea base de trabajo: rama, commit base, respaldo con hash e inventario disponibles. La matriz final se actualiza con resultados; no usa notas de otros grupos.
- Reproducción controlada: cinco fallos reales con cero errores de arnés en reproduccion_controlada.xml. El primer intento tuvo errores de limpieza del trigger, conservados como tales en reproduccion_antes.xml.
- Correcciones: validación de ruta al cambiar sector; bloqueos PostgreSQL de arranque ETL/modelo y asignación; duplicados ETL entre tandas; transacción de alta/edición junto a auditoría. No se agregaron migraciones ni se modificó Neon.
- Regresión 55/55 y luego 56/56 con prueba de reversión de alta ante fallo de bitácora. Ruff correcto; frontend build correcto y audit sin vulnerabilidades conocidas; persisten nueve advertencias de lint y tamaño del bundle.
- El runner creó y detuvo clústeres propios. En las pruebas transaccionales solo la limpieza de test_* suspende temporalmente el trigger; las pruebas de inmutabilidad y el producto mantienen la protección.

## Fase 2

- Sitio local: 16 recorridos a 1440/390 aprobados; corregido desbordamiento de la galería de marketing y falta de encabezado principal accesible.
- Función de salud: seis casos aprobados; 404, 500 y respuesta opaca no se declaran servicio sano.
- Oferta local identificada como propuesta: sin contratación, cuotas automáticas ni factura electrónica habilitadas.
- Estado PARCIAL: publicación explícitamente a cargo del titular. CLI local leosb12 no tiene los proyectos existentes. No se cambiaron alias ni DNS.

## Fases 4 a 7

- Runbook Azure corregido, CI espera los tres jobs, verifica ambos secretos y reintenta salud. No se hizo push ni despliegue.
- Inventario de 174 componentes Python/npm con licencias declaradas; borradores y matriz legal sin firmas ni trámites inventados.
- Finanzas: 50 % anual con diez meses y 50 % mensual, tres escenarios; siete comprobaciones aprobadas. Capital propuesto Bs 200.000 por déficit Bs 162.817 y contingencia/redondeo; sustituye propuesta preliminar de Bs 170.000. No es inversión obtenida. Retorno de inversionista separado del operativo.
- Lectura nativa por API de Enterprise Architect: DSU-FaseFinal.eapx, 18 paquetes, 343 elementos y 18 diagramas; sin guardar cambios ni atribuir autoría individual. No equivale a revisar visualmente todos los objetos.
- Word/PDF generados con 13 capítulos, pruebas y financiamiento. Se conserva Material_Drive anterior en Entregables/versiones. La herramienta render_docx.py no pudo usar LibreOffice (ausente); se utiliza exportación nativa Word y render de PDF con PyMuPDF para QA.


## Ampliación de precisión y capacidad

Se detectó y reprodujo RNF23: 0,005 por factor 0,7 persistía 0,003 por representación binaria, frente a 0,004 con Decimal. Se conservó reproduccion_precision.xml fallido antes de corregir, sin modificar Neon. La normalización conserva Decimal y solo convierte a float para estadística de atípicos no persistida. Regresión posterior y concurrencia de vehículo separado en regresion_final.xml.

Medición aislada con 500 puntos añadidos y 100.000 registros: todas las filas con umbral del comando cumplieron en proceso local. El primer arnés falló al imprimir Unicode después de guardar el resultado; se corrigió la salida y se repitió, con código 0 y recuentos antes/después iguales. Esa medición antecede a la corrección Decimal: no se declara medición de ese código posterior hasta repetirla.

Se verificó la demo con 16 pantallas y 18 pasos API integrados. Primeros intentos del arnés fallaron por intérprete sin Playwright, carrera de arranque del servidor y supuesto incorrecto de encabezado en Campo; se corrigieron y se conservaron logs. El recorrido válido incluye escritura, ETL, predicción y exportaciones. Se amplía ahora con 12 hilos HTTP y verificación de persistencia; no se presume aprobado hasta leer su resultado.


## Revalidación pública y límites finales

Azure confirmó dsu-api encendida, Standard_B2als_v2, Mexico Central. En el chequeo final Residata volvió a HTTP 200; se verificaron once rutas/recursos. No se hizo ningún despliegue. El contenido público aún conserva facturación afirmada y la ronda de Bs 170.000, mientras el local corrige ambos puntos. Por ello el requisito de sitio pasa de NO CUMPLE a PARCIAL: publicado pero desalineado con la corrección local. No se atribuye la recuperación a una causa no verificada.

Carga final: doce clientes virtuales en sesenta segundos, 531 peticiones sin errores y 156/156 vaciados persistidos. Se corrigió el arnés para usar un operario sintético nuevo en cada repetición, evitando el conflicto legítimo con asignaciones de intentos previos.

La medición se repitió sobre la normalización Decimal: código 0, recuentos antes/después iguales; tiempos exactos en rendimiento_local.txt. Se añadieron los tres QR al anexo, conservando la distinción entre versión local y pública anterior.


## Cierre de registros
Regresión final: 58 aprobadas en 172.475 s. Carga: 531 peticiones sin errores y 156 vaciados sin pérdida. Medición posterior a Decimal con rollback comprobado. Word/PDF: 298 páginas y trece capítulos. Ver 09_auditoria_final.md para criterios pendientes; no se marca 100 %.


Servidor local de desarrollo reiniciado para cargar el código corregido; GET frontend 200 y API directa/proxy 401 esperados. Sin login ni escrituras nuevas en Neon. Las instancias de prueba PostgreSQL, API/Vite y navegador efímeros se detuvieron al terminar; quedan los servidores de desarrollo solicitados anteriormente. Paquete final con manifiesto y comprobación contra secretos privados.
