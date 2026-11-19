# DSU y Residata — Software 2

Sistema de gestión de residuos sólidos para la DSU-UAGRM, con API Django, aplicación React, predicción mediante Random Forest Regressor y complemento Android en Flutter.

## Software

- [Backend](gestion-residuos-dsu/backend): API, reglas de negocio, predicción, pruebas y configuración Azure.
- [Frontend](gestion-residuos-dsu/frontend): aplicación React/Vite.
- [Android](gestion-residuos-dsu/movil): puntos cercanos por GPS e incidencias con dictado, usando la API Azure.
- [Sitio Residata](sitio-residata): sitio corporativo, marketing y pitch.
- [Configuración Vercel](despliegue/vercel_proyectos.json) y [CI/CD](.github/workflows/ci.yml).
- herramientas/pruebas: ejecución de pruebas en PostgreSQL aislado.

## Entregables

[Índice](Entregables/INDICE_ENTREGA_ACTUAL.md): documento Software 2, manual, planes, diagramas, modelos EA, pruebas, material comercial, APK y proyecto Power BI. El manual está también en el capítulo 12 del documento; estándares de codificación en 3.9.3 y anexo I.

[PDF final](Entregables/Software_2/Documento_Software_2_DSU.pdf) · [Word editable](Entregables/Software_2/Documento_Software_2_DSU.docx) · [Drive del QR](https://drive.google.com/drive/folders/1GtrE_rtlimZ3zcj4aZsuvZf6RaErTHqg)

## Producción y desarrollo

- Aplicación: https://dsu-uagrm.vercel.app/
- API Azure: https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com/api/
- Sitio: https://residata-bolivia.vercel.app/
- Base de datos: PostgreSQL en Neon.

Consultar el README de cada componente. Usar Python 3.12, Node.js 22 actualizado y Flutter 3.41.7. Configurar el entorno con .env.example y obtener las credenciales por un canal privado; los archivos .env quedan excluidos. La base demo es compartida: ejecutar las pruebas en una base aislada, sin seed, restauraciones, ETL ni entrenamiento sobre producción.

El APK es una demostración Android ARM64 con firma de depuración. Se construye localmente como archivo descargable; Vercel publica la web y el sitio, y Azure aloja la API. No hay publicación del APK en una tienda.
