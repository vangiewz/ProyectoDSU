> **Antecedente histórico.** Para exponer usar las guías y cifras vigentes de revision_documental_final/entrega/defensa y su informe del 19/11/2026. Este archivo conserva el cierre anterior.

# Guion de defensa del piloto DSU y Residata

## Apertura y alcance

Presentar un sistema web para registrar y planificar la recolección universitaria, centralizar datos y estimar generación con Random Forest. DSU es el piloto; Residata es la propuesta de producto y sociedad en constitución. No afirmar aceptación institucional, empresa registrada o ventas sin documentos.

## Demostración reproducible

Ejecutar `DSU_ONLY_EXTENDED=1` con `ejecutar_aislado.py` para el recorrido automatizado; el navegador efímero y la base son sintéticos. Para demostración humana usar una instancia aislada equivalente; no ejecutar seed sobre Neon.

1. Mostrar login y los cuatro roles. Directivo accede a tablero y recibe Sin acceso en Usuarios.
2. Supervisor: planificar jornada con puntos del mismo sector, asignar operario, confirmar y abrir.
3. Registrar vaciado válido; demostrar rechazo de cantidad inválida y capacidad excesiva.
4. Omitir un punto con motivo y cerrar; demostrar que una jornada cerrada no admite cambios.
5. Administrador: ejecutar ETL; mostrar registros aceptados/observados y trazabilidad.
6. Consultar indicadores, mapa, comparación y exportar PDF/Excel.
7. Mostrar modelo, métricas y versión; generar predicción con margen y recomendaciones.
8. Mostrar bitácora; no intentar modificar datos reales. Presentar la prueba aislada del trigger.
9. Mostrar JUnit antes/después, carga de doce usuarios y restauración sintética.
10. Abrir documento de trece capítulos, pitch y propuesta económica. Indicar que el titular publicará Residata.

## Preguntas difíciles y respuestas respaldadas

| Pregunta | Respuesta verificable |
|---|---|
| ¿Es un microservicio? | No: monolito modular Django, React separado, ORM y servicios; PostgreSQL compartido con plano analítico de tablas. |
| ¿Qué es CASE? | Enterprise Architect para modelado y trazabilidad; Git, Docker, pytest y Vercel son herramientas complementarias. Hay lectura nativa y exportaciones, no certificados de calidad. |
| ¿Usa IA generativa? | No. Random Forest Regressor aprende de histórico; el asistente del sitio usa reglas y correo. |
| ¿Qué tan precisa es la IA? | Hay evaluación sobre datos sintéticos, con partición temporal. No se ha validado precisión institucional. RMSE y versión acompañan la estimación; no garantiza una cifra exacta. |
| ¿Cuándo fueron probadas las correcciones? | Ver JUnit y JSON del cierre, que indican fecha UTC, entorno local y commit base con cambios locales. No confundir con los JUnit históricos. |
| ¿Cómo se probó concurrencia? | Conexiones PostgreSQL distintas, barrera entre participantes, conflicto de personal y vehículo; carga HTTP aislada con doce hilos. No se extrapola a producción. |
| ¿Se comprobó recuperación? | Dump y restauración a otro destino local, recuentos coincidentes, claves foráneas y trigger. No es ensayo de pérdida de VM ni RTO productivo. |
| ¿Por qué cambió la ronda? | Al incluir 50 % de clientes anuales con descuento, el déficit estimado es Bs 162.817 y la propuesta de capital pasa a Bs 200.000. No es financiamiento conseguido. |
| ¿La TIR del inversionista es 42,7 %? | No: esa es la TIR operativa del escenario base. El retorno del inversionista depende de participación y salida hipotética, separado en el JSON y capítulo 13. |
| ¿Es SaaS terminado? | El piloto institucional tiene funciones reales. Contratación, cuotas y límites automáticos por plan no están implementados; son propuesta comercial. |
| ¿Está disponible el portal? | Al principio devolvió 404; la reverificación encontró once rutas/recursos HTTP 200, con contenido anterior. La actualización local está corregida y probada; la publicará el titular. No atribuir la recuperación a un despliegue de esta sesión. |
| ¿Quién programó cada parte? | El Git unificado no permite atribución individual completa. No se inventan aportes; presentar solo commits o registros identificables. |
| ¿Qué falta internamente? | Cola durable o mitigación operativa de hilos web; capacidad productiva y matriz completa de navegadores; revisión jurídica final y obligaciones de terceros. Los pendientes internos no se ocultan como externos. |

## Cierre de la exposición

Recorrer `02_matriz_13_requisitos.md` y `09_auditoria_final.md`. Mostrar qué cumple en el alcance académico, qué es parcial y qué depende de publicación, firma o autoridad externa. La hoja con 68 puntos era de otro grupo y no representa una nota de este proyecto.
