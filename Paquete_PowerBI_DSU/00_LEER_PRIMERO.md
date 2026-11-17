# Traspaso de Power BI — DSU-UAGRM

Actualizado el 16/11/2026. Empezar por `PROMPT_PARA_OTRO_AGENTE.md`.

## Contenido

- `01_proyecto_powerbi/DSU-Residuos.pbip`: proyecto actual con modelo BIM y reporte PBIR; siete tablas, 16 medidas y un gráfico. Conservar el formato que guardó Desktop. No regenerar el informe.
- `02_capturas/`: evidencias PNG y `INDICE_CAPTURAS.md`, que distingue lo histórico de la conexión comprobada.
- `03_documentacion/`: documento Word/PDF con el nombre habitual, fuentes de clase y tres PDF oficiales del docente. El cierre editorial global sigue en curso.
- `04_codigo_referencia/`: definiciones de las vistas y puntos de integración. No es un backend ejecutable ni una instrucción para migrar la base.
- `05_auditoria/`: inventario, DAX, comprobación de conexión y revisión del paquete.

## Estado comprobado

Neon conectado con el rol `powerbi`. Consultas SQL por TLS y lectura de tablas en Power BI Desktop: 15.430 hechos, 1.046 jornadas, 1 incidencia, 12 puntos, 0 predicciones vigentes y 8 recomendaciones; Calendario tiene 1.374 filas. El gráfico existente ya muestra datos. El informe y las relaciones siguen pendientes de una auditoría completa de medidas y filtros; no hay RLS definido ni publicación comprobada.

El usuario introdujo las credenciales en Desktop. Se reabrió el proyecto para revisar la presentación. Los parámetros Servidor y BaseDatos están configurados con valores reales. Las credenciales quedan exclusivamente en `gestion-residuos-dsu/backend/.env` del repositorio privado (`POWERBI_HOST`, `POWERBI_DATABASE`, `POWERBI_USER`, `POWERBI_PASSWORD`); no se incluyen aquí. Power BI no lee `.env` automáticamente y un perfil de Windows diferente puede pedir la clave. El acceso Microsoft para publicar es distinto del acceso PostgreSQL.

La contraseña del backend no se cambió. Se renovó únicamente la del rol `powerbi`, por petición expresa del usuario, sin alterar registros ni ejecutar ETL/entrenamiento. El rol tiene SELECT en las seis vistas y no puede escribir en ellas. El paquete no incluye caché de datos, perfiles ni sesiones.

## Límites

La base contiene datos sintéticos compartidos, no resultados institucionales. La vista de predicciones usa la fecha actual: cero filas es un resultado real, no un error de carga. No alterar fechas ni entrenar para fabricar un gráfico.

La Figura 169 existente sigue siendo la pestaña web antes de publicar. Las capturas nuevas de Desktop no demuestran integración web ni producción. Conservar el rótulo honesto hasta tener publicación autorizada y carga verificadas. No usar publicación anónima.

La copia del documento mantiene `Documento_Taller_de_Grado_I_Grupo_8`. Si se integra una evidencia, actualizar el documento oficial y sus campos/índices; no crear otra entrega con distinto nombre.

## Actualización 16/11/2026 (tarde)

El proyecto ya no tiene un solo gráfico: `powerbi/tablero.py` (repositorio original) completó la página Tablero y las 16 medidas se contrastaron con SQL (`05_auditoria/powerbi_medidas.json`). La captura `02_capturas/22_tablero_completo_desktop.png` reemplazó la Figura 169 del documento, rotulada como Power BI Desktop con datos sintéticos y sin publicar. Pendiente: RLS y publicación.
