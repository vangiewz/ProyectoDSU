# Traspaso de sesión — Software 2 (13 puntos) · 18/11/2026, ~21:15

Leer esto primero al retomar. Complementa `PROGRESO.md` (historia anterior) y `CONTEXTO.md`.

## 0. Encargo y plazo

- Consigna (clase 17/11, `C:/Users/rekte/OneDrive/Desktop/Ingenieria Software 2.pdf` y `clase.pdf`): **un solo PDF con los 13 puntos, cada uno con su carátula**, publicado hasta el **jueves 19/11/2026 a las 8:00**; traerlo impreso + 2 carátulas; **anexos con un conjunto de QR** a material adicional.
- Los 13 puntos (orden del docente = orden de capítulos): 1 PAPS · 2 PUDS · 3 Manual de calidad (ISO 9001, CMMI, IEEE 730) · 4 Herramientas CASE (valor, aceleración de productividad) · 5 Aspectos legales · 6 Infraestructura (gestión/configuración, planeación, pruebas, despliegue, monitoreo) · 7 Sitio web corporativo **publicado** (empresa de SW; emails, chats, agentes, actualizaciones) · 8 Estudio de mercado (monetización, todo con números) · 9 Pruebas (4 formas, ver §3) · 10 Marketing (material digital) · 11 Puesta en marcha (infraestructura, disponibilidad, DevOps, calculadora de nube, términos, privacidad, licencias suscripción/freemium, AWS/Azure/GCP) · 12 Software como producto · 13 Financiamiento (pitch para inversionistas).
- Pruebas según la clase: (1) flujo de pruebas del Proceso Unificado aplicado al proyecto; (2) **listas de comprobación** de un libro de IS, genéricas y adaptadas; (3) herramientas/servicios que reciben una URL y devuelven defectos (+ pruebas móviles); (4) **≥3 CU con complejidad ≥3 representados en diagrama de secuencia y caja blanca sobre ese diagrama** (grafo, V(G), caminos, **matriz de conexiones**). También alfa/beta, caja negra, "mentalidad destructiva".
- Pedido del usuario: nada de placeholders; hacer las cosas reales; **todo lo que diga AWS → Azure** (documento y diagramas); diseño de la web con **impeccable**.

## 1. Decisiones confirmadas por el usuario (18/11)

| Tema | Decisión |
|---|---|
| Empresa | **Residata S.R.L.** (en constitución); producto **Residata**; DSU-UAGRM = cliente piloto |
| Monetización | **SaaS por suscripción + freemium** |
| Despliegue | **Azure** para el backend (antes AWS); Vercel para la app DSU y el sitio |
| Contacto | correo **rekteado@gmail.com** (FormSubmit **ya activado** por el usuario) |
| Agentes/chat | asistente sin IA (base de conocimiento) que deriva a **agente humano** por ticket al correo; sin WhatsApp |
| Sitio | HTML/CSS estático; público = compradores institucionales |
| SLA (confirmado) | disponibilidad 99 % Campus / 99,5 % Red, crédito 10 % de cuota por punto faltante; soporte 8 h hábiles Campus / 4 h Red; contactos < 1 día hábil |
| Precios | **propuestos por el estudio de mercado, no confirmados explícitamente**: Inicial Bs 0 · Campus Bs 2 900/mes · Red Bs 7 500/mes · anual = 10 meses · implementación Bs 9 000 / Bs 18 000 (los primeros precios Bs 1 450/3 900 hacían inviable el negocio: equilibrio 35 clientes) |

## 2. Lo que YA está hecho y verificado

### 2.1 Producción (real, funcionando)
- **API**: https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com — Azure VM `dsu-api` (Standard_B2als_v2, 2 vCPU, 4 GB, Ubuntu 24.04, swap 2 GB), grupo `residata-dsu-rg`, **Mexico Central** (la suscripción Azure for Students solo permite mexicocentral, canadacentral, eastus, southcentralus, northcentralus; eastus sin capacidad). IP 68.155.156.170, DNS `dsu-uagrm-api.mexicocentral.cloudapp.azure.com`. SSH `azureuser@68.155.156.170` con `~/.ssh/id_ed25519`, NSG: SSH solo desde 192.223.106.95, 80/443 abiertos.
  - En la VM: `~/dsu/backend` con `deploy/compose.azure.yml` (app Gunicorn, proxy Caddy con Let's Encrypt, respaldo pg_dump diario 14 días) y `.env` de producción (DEBUG=False, SECRET_KEY nueva, ALLOWED_HOSTS, CORS=https://dsu-uagrm.vercel.app, DSU_API_DOMAIN). **Neon se mantiene** (São Paulo; migraciones al día, 48 aplicadas).
  - cron horario del ETL (`crontab -l` en la VM). Primer respaldo `respaldos/dsu-20261118-2258.dump`.
  - Comando de redespliegue: `cd ~/dsu/backend/deploy && docker compose --env-file ../.env -f compose.azure.yml up -d --build`.
- **App DSU**: https://dsu-uagrm.vercel.app (proyecto Vercel `dsu-uagrm`, cuenta vangiewz, env `VITE_API_URL`). Login demo funciona (usuarios `supervisor`, `operario1`, `directivo`; clave demo en `seed.py`).
- **Sitio corporativo**: https://residata-bolivia.vercel.app (proyecto Vercel `residata`; `residata.vercel.app` pertenece a otro). Publicar con `sh sitio-residata/publicar.sh` (ensambla y re-apunta el alias).
  - Páginas: index, planes, novedades (+`feed.xml` RSS, 5 versiones reales de ESTADO.md), soporte (FAQ, niveles, **estado del servicio en vivo**), contacto, términos, privacidad, 404, **`/pitch/`** (11 láminas + `pitch/Residata_pitch.pdf`), **`/marketing/`** (piezas de campaña).
  - Asistente en todas las páginas (en móvil: botón en la cabecera) con derivación a agente → ticket `RD-AAAAMMDD-NNNN` por FormSubmit.
  - Diseño con impeccable: mundo «Ticket de báscula» (seed:66e3e17cff34ed12); `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json`, brief en `.impeccable/surfaces/index-html.md`. Revisión final: 2 rondas, todos los arreglos resueltos.
  - Fuentes: `paginas/*.html` + `construir.py` → raíz; `css/site.css`, `js/site.js`, `novedades.json`, `calendario.json` (totales semanales reales del ETL demo).
- **Monitoreo Azure** (real): Log Analytics `residata-logs`, Application Insights `residata-monitor`, prueba estándar `disponibilidad-api` (cada 900 s, Texas + São Paulo, espera 401, verifica TLS), alertas `disponibilidad-caida` (<90 %), `vm-cpu-alta` (>80 %), `vm-memoria-baja` (<400 MB), grupo de acción `residata-alertas` → correo. Se borraron las pruebas `-web` y `-sitio` por costo (con 3 pruebas/3 regiones/5 min ≈ USD 43/mes; ahora ≈ USD 3,21/mes a USD 0,00055 por ejecución). Primera hora: 50/50 ejecuciones exitosas (`docs/auditoria-fase-final/qa_url/azure_disponibilidad.txt`).
- **CI/CD**: `.github/workflows/ci.yml` (backend Ruff + `makemigrations --check` + pytest contra PostgreSQL 18; frontend oxlint + build; sitio ensamblado sin diferencias; job de despliegue a la VM si existen los secrets `AZURE_VM_HOST` y `AZURE_VM_SSH_KEY`). **No se ha hecho push** (no hay commits de esta sesión).

### 2.2 Cambios de código
- `backend/deploy/compose.aws.yml` → `compose.azure.yml` (git mv).
- `backend/config/settings.py`: comentario partido (defecto E501 hallado por el CI).
- `backend/apps/operations/tests/test_registro_caminos.py`: 8 caminos básicos de CU9.
- `frontend/index.html`: meta description; `frontend/public/robots.txt`.
- **Suite: 50 pruebas, 0 fallos (43,8 s)**, corrida en contenedores de la VM → `docs/auditoria-fase-final/pruebas_ci/pytest.xml`.

### 2.3 Diagramas (Enterprise Architect, `modelo_uml/DSU-FaseFinal.eapx`, regenerado con `python generador/fase_final/ea_final.py`)
- AWS → Azure: `generador/fase2/disenio.py` (nodo «Azure VM: Ubuntu 24.04 y Docker (Mexico Central)», Caddy, Neon «São Paulo», Vercel con «sitio corporativo Residata»), `ea_final.py`, `componentes.py`. Exportados en `generador/figuras/fase_final/`: `c7_despliegue.png`, `c8_general.png`, `c8_sub1..8.png`.
- **Caja blanca sobre secuencias** (nuevo `generador/fase_final/secuencias_caja_blanca.py`, llamado desde `ea_final.py`): `c9_seq_cu09/15/28.png` (fragmentos `break`/`opt`) y `c9_grafo_cu09/15/28.png`. Datos en `docs/auditoria-fase-final/pruebas/caja_blanca_secuencias.json` (`python generador/fase_final/secuencias_caja_blanca.py`):
  - CU9 Registrar vaciado: N=11, E=17, P=7, **V(G)=8**, 8 caminos, todos aprobados (`test_caminos_registro[...]`).
  - CU15 Asignar personal y vehículos: N=11, E=17, P=7, **V(G)=8**, 8 caminos aprobados (`test_caminos_asignacion[...]`).
  - CU28 Predecir generación: N=14, E=21, P=8, **V(G)=9**, 9 caminos aprobados (`test_rechazos_prediccion`, `test_prediccion_con_filtros`, `test_entrena_publica...`, `test_alerta_de_desborde...`).
  - V(G) verificado por E−N+2, P+1 y matriz de conexiones; caminos linealmente independientes (rango = V).
- **Pendiente en Taller**: el documento de Taller sigue diciendo AWS (cap. 7, 8, 10) y sus figuras compartidas ya muestran Azure si se reensambla. Preguntar al usuario si también se cambia Taller.

### 2.4 Pruebas por URL y móviles (evidencia en `docs/auditoria-fase-final/qa_url/` y `movil/`)
- `DocumentoSoftware2/qa_url.py` → `resumen.json`: **sitio** Observatory A+ (125), SSL Labs A+/A, W3C 0 errores, Lighthouse móvil 99/96/100/100 → tras corregir: **98/100/100/100**; **app** Observatory A+ (135), W3C 0, Lighthouse 98/100/100/82 → **95/100/100/100**; **API** SSL Labs A+ (Observatory 422: sin HTML en la raíz). Corridas posteriores: `lighthouse-*-corregido.json`.
- Defectos hallados y corregidos: barras del calendario como botones de ~8 px (target-size) → decorativas + deslizador accesible; app sin meta description; `robots.txt` inválido (la SPA devolvía HTML); E501 (CI).
- `DocumentoSoftware2/prueba_movil.py` → `movil/resultados.json`: iPhone 13 y Pixel 7, 6 pantallas por rol, **12/12 aprobados**, sin desborde; login 4,8–6,9 s, carga 3,4–7,3 s (latencia VM México ↔ Neon São Paulo; región Brasil no permitida por la suscripción).
- `DocumentoSoftware2/capturar_produccion.py` → `recursos/prod/*.png` (capturas del sistema en producción; tablero y mapa con rango 01/03–05/10/2026).

### 2.5 Finanzas (`DocumentoSoftware2/finanzas.py` → `recursos/finanzas.json`, gráficos `recursos/web/finanzas_*.png`)
- TC Bs 11,67/USD (BCB, igual que Taller cap. 10).
- Nube equivalente (2 vCPU, 4 GB, 32 GB SSD, IPv4) USD/mes: **Azure 39,68** (Mexico Central, adoptado) · **GCP 47,28** (São Paulo, e2-medium 0,0531852/h; disco balanceado 0,000205479/GiB·h; IP 0,005/h — leídos en las páginas oficiales con Chrome) · **AWS 57,57** (São Paulo, t3.medium 0,0672/h; gp3 0,152/GB; IP 0,005/h — AWS Price List API).
- Plataforma mensual: Azure 39,68 + Neon Launch 11,30 + Vercel Pro 20 + Azure Monitor 3,21 = **USD 74,19 (Bs 865,8)**.
- Mercado: 343 municipios (300 con botaderos, 43 con relleno; MMAyA 2025 vía Correo del Sur 2026), 15 universidades CEUB, 33 privadas (eju.tv). **TAM Bs 32,54 M/año · SAM Bs 5,54 M/año · SOM año 5 Bs 1,22 M**.
- Proyección 5 años (clientes fin de año Campus 2/5/9/13/17, Red 1/2/4/6/8; sueldos fundadores 4 500→7 000→9 000; agente desde año 2; dev desde año 4; IVA 13 %, IT 3 %, IUE 25 %, cargas 16,71 %, aguinaldo): flujo −80 261, −58 994, +77 213, +167 947, +361 095; **flujo positivo año 3, recuperación año 4, VAN 15 % Bs 211 921, TIR 64,2 %, equilibrio 13,2 clientes Campus, déficit máximo Bs 139 255 → ronda Bs 170 000** (uso: equipo 111 407, marketing 11 638, nube 7 271, constitución/contabilidad/impuestos 8 939, contingencia 30 745).
- Fuentes de financiamiento halladas: Fideicomiso de Capital Semilla BDP–COSUDE (FOCASE; ficha ASFI sep-2025: hasta 1 año operaciones, 5 años inversión), concurso Incuba Unión Tecnológico (Bs 48 000 a 5 startups, 2025), iThink VC (pre-semilla/semilla), BID feb-2026 (1,2 startups con VC por millón de hab.; 12,3 % captó USD 10 001–100 000), AgroInnovatec 2026 PNUD-BDP.

### 2.6 Documento (`DocumentoSoftware2/`)
- `capitulos.md` reordenado: **2 = PUDS, 3 = Manual de calidad (SQAP)** (respaldo `versiones/capitulos_2026-11-18_antes_13puntos.md`); referencias cruzadas corregidas (incl. `modelos.py`).
- Recursos listos: `recursos/sitio/*.png` (inicio 1440 y móvil, asistente, planes, novedades, soporte, 3 piezas de marketing), `recursos/pitch/lamina-01..11.png`, `recursos/qr_sitio.png`, `qr_app.png`, `qr_pitch.png`, `recursos/prod/*.png`, `movil/*.png`.
- **NO se ha regenerado el .docx/PDF todavía.**

## 3. LO QUE FALTA (en orden) — redacción del documento

Editar `capitulos.md`/`paps.md` y luego `python ensamblar.py` (genera docx, índice, PDF en `Entregables/Software_2/` y `Material_Drive`). Formato: sin numeración de figuras; `<!-- fig: ruta | título | fuente -->`. **Agregar a `ensamblar.py` una variante apaisada** (p. ej. `<!-- figh: ... -->` que llame `figure(..., land=True)`) para las secuencias anchas. Quitar del cap. 9 el marcador `<!-- grafos pruebas -->` (grafos viejos de código) o mencionarlo como complemento.

1. **AWS → Azure en el texto**: `paps.md` líneas ~326 (tabla 1.4), ~341 (1.4.1 operación: reemplazar Bs 2 186,31 por plataforma USD 74,19 + Power BI Pro 2 usuarios USD 28 = USD 102,19 ≈ **Bs 1 192,56/mes, Bs 14 310,7/año**), ~420; `capitulos.md` ~52 (cap. 2), ~401 y ~598/604 (SQAP, proveedor Azure VM), cap. 11 completo, ~1223 (privacidad). `grep -n -i "aws\|ec2\|amazon" paps.md capitulos.md`.
2. **Cap. 6 Infraestructura**: tabla Actividad | Herramienta | Uso real | Evidencia → configuración/versiones (Git, GitHub privado), planeación (Gantt `generador/figuras/gantt.png`, PERT `estimaciones.json`, COCOMO II), modelado (EA), CI (GitHub Actions `ci.yml`), pruebas (pytest, Playwright, Lighthouse, ZAP, Observatory, SSL Labs, W3C), despliegue (Docker Compose `compose.azure.yml`, Caddy, Vercel CLI, `publicar.sh`), monitoreo (Azure Monitor: prueba, 3 alertas, correo; costo), respaldo (pg_dump). Secciones: CI/CD (jobs y su verificación en la VM: 50/50, defecto E501), monitoreo y alertas (50/50 ejecuciones), entornos (VM B2als v2 Mexico Central, Neon São Paulo, Vercel), inventario de versiones (`<!-- versiones -->`).
3. **Cap. 7 Sitio web corporativo** (reemplazar el actual, que describe la app DSU): URL publicada, empresa, arquitectura de información (tabla de páginas), canales **correo** (formularios FormSubmit), **chat** (asistente), **agentes** (ticket a persona), **actualizaciones** (Novedades + RSS + suscripción + estado del servicio en vivo); niveles de atención; diseño (impeccable, mundo «Ticket de báscula», fuentes propias, accesibilidad 100); seguridad (CSP, HSTS, Observatory A+); capturas `recursos/sitio/*`; hoja de ruta (PWA offline, IoT) del texto viejo; QR `qr_sitio.png`.
4. **Cap. 8 Estudio de mercado**: actualizar 8.1 con cifras MMAyA; conservar 8.2–8.4; agregar **tamaño del mercado (TAM/SAM/SOM)**, **modelo de monetización** (planes, freemium, implementación, anual), **proyección** (tabla 5 años + `finanzas_ingresos_egresos.png`), **equilibrio, VAN, TIR** (+ `finanzas_flujo_acumulado.png`); luego estrategia de adopción (texto viejo 8.5).
5. **Cap. 9 Pruebas** — estructura: 9.1 objetivo (mentalidad destructiva, alfa/beta); 9.2 **flujo de trabajo de prueba del PU** (Jacobson et al., 2000, cap. 11: planificar, diseñar, implementar, realizar integración, realizar sistema, evaluar; artefactos y roles; qué se hizo en cada actividad); 9.3 caja negra (escenarios críticos + resultados API existentes); 9.4 **caja blanca sobre secuencias** (3 CU: figura secuencia apaisada, figura grafo, tabla de nodos con mensajes, cálculo de V(G) de 3 formas, **matriz de conexiones** N×N, tabla de caminos con prueba y resultado; todo desde `caja_blanca_secuencias.json`); 9.5 **listas de comprobación** (Myers, Sandler y Badgett, 2012, *The Art of Software Testing* 3.ª ed., cap. 3: lista de errores para inspecciones — referencia a datos, declaración, cálculo, comparación, flujo de control, interfaz, E/S — adaptada con resultado y evidencia; p. ej. Ruff F821, DecimalField, factor_conversion, límites 1..máximo probados, `@transaction.atomic` + `select_for_update`, firmas xlsx/pdf probadas, bitácora inalterable probada, mensajes en español); 9.6 **herramientas por URL** (tabla resumen.json + antes/después Lighthouse + defectos corregidos + ZAP previo); 9.7 **pruebas móviles** (tabla movil/resultados.json, capturas `docs/auditoria-fase-final/movil/`); 9.8 regresión (JUnit Windows/Linux + CI 50); 9.9 alfa (producción controlada 18/11) y beta (plan con la DSU, anexo C); 9.10 componente predictivo (texto existente); 9.11 cierre.
6. **Cap. 10 Marketing**: agregar «Material publicitario digital» con `recursos/sitio/marketing-*.png` (https://residata-bolivia.vercel.app/marketing/) y el `og.png` del sitio; actualizar canales (sitio publicado, RSS, correo) y KPIs.
7. **Cap. 11 Puesta en marcha**: comparativa con números (tabla nube de `finanzas.json`; método = calculadoras/APIs oficiales), costo de plataforma; arquitectura desplegada (figura `c7_despliegue.png` apaisada); **DevOps** (pipeline, comandos de despliegue, monitoreo); **verificación ejecutada** (TLS A+, HTTP→HTTPS, CORS, login por rol, ETL cron, respaldo creado, disponibilidad 50/50); **disponibilidad en el lanzamiento** (SLA comprometido + medido); DRP (actualizar a Azure); hardening; **licencias: suscripción/freemium** (planes) + licencia institucional sin costo para la DSU piloto; términos y privacidad alineados con el sitio (Azure, FormSubmit).
8. **Cap. 12**: URLs de producción, pitch, sitio; lista de entrega.
9. **Cap. 13 Financiamiento (NUEVO, antes de Bibliografía)**: necesidad (déficit, Bs 170 000), uso de fondos (tabla), fuentes en Bolivia (FOCASE, Incuba Unión Tecnológico, VC, ángeles), estructura propuesta (Plan A no dilutivo: concurso Bs 48 000 + FOCASE Bs 122 000 a 5 años; Plan B ángel 15 % por Bs 170 000 = valoración post-money ≈ Bs 1,13 M), indicadores (VAN, TIR, recuperación, equilibrio), **pitch** (11 láminas `recursos/pitch/`, PDF + QR), riesgos para el inversionista.
10. **Anexo F QR**: agregar `qr_sitio.png`, `qr_app.png`, `qr_pitch.png` (y los existentes repositorio/Drive) en `ensamblar.py`.
11. **Bibliografía**: Myers et al. (2012); MMAyA (2025)/Correo del Sur (2026); CEUB; BID (2026) diagnóstico de emprendimiento; ASFI (2025) ficha FOCASE; Microsoft (Azure pricing, Azure Monitor); AWS Price List; Google Cloud pricing; Neon; Vercel; Mozilla HTTP Observatory; Qualys SSL Labs; Google Lighthouse; W3C Nu Validator; Playwright; FormSubmit. Actualizar la nota de fecha de consulta (18/11/2026).
12. Regenerar: `cd DocumentoSoftware2 && python ensamblar.py` (≈1 min; actualiza índice y PDF vía Word). Revisar el PDF (carátula por capítulo = 13 carátulas), `material.py` arma `Entregables/Material_Drive/`.
13. Actualizar `PROGRESO.md`, `backend/docs/ESTADO.md` (despliegue Azure real, 50 pruebas, CI) y la memoria del proyecto.
14. Con permiso del usuario: commit (y push para que corra el CI). Configurar secrets si quiere CD.

## 4. Cuidado

- Costos en la suscripción **Azure for Students** (crédito USD 100): VM ≈ USD 39,68/mes + monitoreo ≈ 3,21. Para apagar: `az vm deallocate -g residata-dsu-rg -n dsu-api` (la IP estática se mantiene).
- `.env` del backend está versionado a propósito (repo privado); el `.env` de producción vive solo en la VM. No imprimir secretos.
- Git Bash convierte rutas `/subscriptions/...` en `az`: usar `export MSYS_NO_PATHCONV=1`.
- Heredocs largos con comillas fallan en el Bash de esta máquina: escribir scripts a archivo y ejecutarlos.
- El documento de Taller no se tocó; si se reensambla, sus figuras compartidas ya muestran Azure.
