# Fichas concretas para la defensa de los trece puntos

## 1. PAPS y estimaciones

**Evidencia:** DocumentoSoftware2/paps.md; estimaciones.json.

**Pregunta probable:** ¿Son horas trabajadas?
**Respuesta defendible:** No: los valores PERT son estimaciones de esfuerzo pendiente; E=(O+4M+P)/6. No se presentan como partes de trabajo reales.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 2. PUDS aplicado

**Evidencia:** generador/fase2/datos.py; backend/apps/.

**Pregunta probable:** ¿Se crearon requisitos distintos para dos materias?
**Respuesta defendible:** No: Taller y Software II usan el mismo sistema, 27 RF y 34 CU; se adapta el entregable, no el negocio.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 3. Aseguramiento de calidad

**Evidencia:** DocumentoSoftware2/estandares.md; auditoria_gui/regresion/.

**Pregunta probable:** ¿Tener SQAP equivale a certificación ISO?
**Respuesta defendible:** No: SQAP define procedimientos y evidencias; las normas citadas son referencias, no certificaciones obtenidas.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 4. Herramientas CASE

**Evidencia:** modelo_uml/DSU-FaseFinal.eapx; inventario_EA.xml.

**Pregunta probable:** ¿Qué es evidencia de CASE?
**Respuesta defendible:** El archivo nativo abierto en Enterprise Architect, sus diagramas exportados y la correspondencia con modelos/servicios. Un editor de código no sustituye esa evidencia.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 5. Aspectos legales

**Evidencia:** auditoria_cierre/legal/matriz_tramites.md.

**Pregunta probable:** ¿La sociedad y el software están registrados?
**Respuesta defendible:** No se acredita formalización con una propuesta. Distinguir documentos preparados de trámites efectivamente completados y respaldados.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 6. Infraestructura

**Evidencia:** backend/deploy/compose.azure.yml; config/settings.py.

**Pregunta probable:** ¿Dónde están los datos?
**Respuesta defendible:** PostgreSQL permanece en Neon. La API se despliega en Azure y React en Vercel. PostgreSQL local se usa solo para QA aislado.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 7. Sitio corporativo

**Evidencia:** sitio-residata/paginas; auditoria_gui/corporativo.

**Pregunta probable:** ¿Se comprobó que llega el correo?
**Respuesta defendible:** Se comprobó formulario y error con red bloqueada; no se enviaron correos reales. La entrega de FormSubmit no está acreditada.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 8. Mercado y proyección

**Evidencia:** DocumentoSoftware2/finanzas.py; recursos/finanzas.json.

**Pregunta probable:** ¿TAM y clientes proyectados son contratos?
**Respuesta defendible:** No: son hipótesis cuantificadas. La demanda, conversión, capacidad por VM e ingresos necesitan validación comercial.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 9. Cuatro modalidades de prueba

**Evidencia:** guía docente; auditoria_gui; pruebas/validacion_matematica.json.

**Pregunta probable:** ¿Por qué 8, 8 y 9 caminos?
**Respuesta defendible:** Son E−N+2P de tres grafos con P=1; las matrices tienen E entradas y los vectores de caminos poseen rango V. No se copió el 4 del ejemplo del pizarrón.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 10. Marketing

**Evidencia:** sitio-residata/marketing; recursos/sitio.

**Pregunta probable:** ¿Las piezas demuestran una campaña ejecutada?
**Respuesta defendible:** No: las piezas existen; el alcance, leads y conversión son objetivos si no hay mediciones de una campaña real.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 11. Puesta en marcha

**Evidencia:** backend/deploy; auditoria_cierre/05_ejecuciones_pruebas/restauracion.json.

**Pregunta probable:** ¿Se probó recuperación productiva?
**Respuesta defendible:** Se verificó restauración sintética local con recuentos y claves; no es simulación de pérdida de la VM ni prueba de RTO productivo.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 12. Producto real

**Evidencia:** frontend/docs/MANUAL_USUARIO.md; auditoria_gui/INFORME_FINAL.md.

**Pregunta probable:** ¿El producto tiene offline, IoT o cobro automático?
**Respuesta defendible:** No: esas capacidades son propuestas. Sí hay operación, analítica, Random Forest y reportes verificables. Power BI publicado y aceptación DSU siguen pendientes.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.

## 13. Financiamiento

**Evidencia:** DocumentoSoftware2/finanzas.py; recursos/finanzas.json.

**Pregunta probable:** ¿VAN o TIR garantizan retorno al inversor?
**Respuesta defendible:** No: son resultados del escenario. La TIR operativa difiere del retorno por participación y salida hipotética; el capital propuesto no está conseguido.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.
