# DSU Campo para Android

Complemento Flutter de la web DSU, conectado directamente a la API HTTPS de Azure. Misma cuenta, permisos y datos; sin duplicar reglas de negocio ni cambiar el documento académico.

## Tarea que resuelve

En campo, el usuario pulsa «Mi ubicación», revisa el punto permitido más cercano, confirma su código y abre una incidencia para ese punto. Puede dictar la descripción, revisarla y enviarla al sistema compartido. El orden por distancia es una sugerencia; los puntos demo tienen coordenadas aproximadas y el GPS tiene error. La API valida los permisos y la jornada.

- GPS: ubicación puntual en primer plano, distancia aproximada y lista ordenada por cercanía. No se envían ni se guardan coordenadas personales en Azure.
- Micrófono: dictado en español mediante los servicios de reconocimiento del teléfono. El audio no se adjunta a la incidencia; revisar la configuración del proveedor de voz del dispositivo.
- Mapa OpenStreetMap: puntos visibles según la cuenta y enlace a indicaciones externas.
- Reporte: tipo, gravedad, jornada cuando corresponda y texto revisable antes de enviar.
- Sesión JWT: refresh en almacenamiento seguro del sistema, renovación y cierre con revocación remota cuando hay conexión.

## Construir y probar

Flutter 3.41.7, Dart 3.11.5, Android SDK instalado. Android 7/API 24 como mínimo, con procesador ARM64 para el APK distribuido.

```powershell
flutter pub get
flutter analyze
flutter test
flutter build apk --debug --split-per-abi --target-platform android-arm64
adb install -r build/app/outputs/flutter-apk/app-arm64-v8a-debug.apk
```

APK de demostración: `build/app/outputs/flutter-apk/app-arm64-v8a-debug.apk`; copia distribuible en `Entregables/Material_Drive/09_Android/DSU_Campo_Android_Demo.apk`. Está firmado para pruebas, no es una publicación en Play Store.

La URL predeterminada es la API de Azure existente. Para un entorno propio: `flutter run --dart-define=DSU_API_URL=https://servidor/api/`. Mantener la barra final y HTTPS. No introducir credenciales en el proyecto ni en parámetros de compilación.

## Validación del 19/11/2026

Ocho pruebas automáticas aprobadas: cercanía sin alterar la lista recibida, login/almacenamiento, renovación JWT, protección de URL paginada, paginación completa, validaciones del servidor, borrado local al cerrar y validación del formulario.

Dispositivo real Samsung Galaxy S23, por ADB: login supervisor, restauración de sesión tras reiniciar, mapa/puntos de Azure, GPS y sugerencia cercana. El usuario confirmó el dictado real de una frase. El único reporte de prueba se identifica en `auditoria_movil/resultado_dispositivo.json`; se verificó por GET independiente y se dejó atendido. No se publican coordenadas personales ni credenciales.

## Límites

No incluye cámara ni fotos porque la API vigente no almacena adjuntos. No hay cola offline, captura de vaciados ni planificación completa en esta app; esas funciones siguen en la web. No guarda borradores después de cerrar la pantalla. Un timeout de envío exige comprobar el resultado antes de reenviar. Falta prueba en un recorrido físico por el campus y una matriz exhaustiva de dispositivos/roles. Si el dictado no está disponible, se puede escribir.
