# Verificación de DSU Campo en dispositivo real

Fecha: 19/11/2026. Dispositivo Android Samsung Galaxy S23 conectado por ADB. Ocho tests Flutter aprobados y análisis sin incidencias. La evidencia de persistencia se conserva en resultado_dispositivo.json.

Se inició sesión con supervisor desde la UI del APK; se reinició y se comprobó la restauración. El mapa cargó puntos desde Azure. El GPS mostró precisión y sugerencia cercana; no se guardan coordenadas personales. El usuario confirmó la transcripción de una frase por micrófono. Se envió una incidencia única, tipo OTRO/gravedad BAJA, con marca de prueba, se leyó desde otro cliente HTTP y se atendió para no dejar trabajo operativo pendiente. El GET posterior confirmó ATENDIDA.

Las capturas login.png y current.png muestran acceso y mapa del campus antes del GPS; no acreditan un recorrido físico. No incluyen credenciales ni ubicación personal. El dictado está confirmado por el usuario, no por una aserción automática de audio. No se declara prueba exhaustiva de todas las cuentas, redes, permisos denegados o teléfonos. El APK está firmado para demostración.
