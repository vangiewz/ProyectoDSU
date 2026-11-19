import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:timezone/data/latest.dart' as tzdata;
import 'package:timezone/timezone.dart' as tz;

class Recordatorio {
  const Recordatorio(this.owner, this.pointId, this.code, this.at);
  final String owner, code;
  final int pointId;
  final DateTime at;
  String encode() => jsonEncode({
    'owner': owner,
    'pointId': pointId,
    'code': code,
    'at': at.toUtc().toIso8601String(),
  });
  static Recordatorio? decode(String? payload) {
    try {
      final data = jsonDecode(payload!);
      return Recordatorio(
        data['owner'] as String,
        data['pointId'] as int,
        data['code'] as String,
        DateTime.parse(data['at'] as String),
      );
    } catch (_) {
      return null;
    }
  }
}

class Recordatorios {
  Recordatorios({FlutterLocalNotificationsPlugin? plugin})
    : plugin = plugin ?? FlutterLocalNotificationsPlugin();
  final FlutterLocalNotificationsPlugin plugin;
  final opened = ValueNotifier<Recordatorio?>(null);
  bool ready = false;
  bool avisosActivos = false;
  bool preferenciaGuardada = false;
  final storage = const FlutterSecureStorage();

  Future<void> initialize() async {
    tzdata.initializeTimeZones();
    final preference = await storage.read(key: 'dsu_avisos');
    preferenciaGuardada = preference != null;
    avisosActivos = preference == 'true';
    ready =
        await plugin.initialize(
          settings: const InitializationSettings(
            android: AndroidInitializationSettings('ic_recordatorio'),
          ),
          onDidReceiveNotificationResponse: (response) {
            opened.value = Recordatorio.decode(response.payload);
          },
        ) ??
        false;
    final launch = await plugin.getNotificationAppLaunchDetails();
    if (launch?.didNotificationLaunchApp == true) {
      opened.value = Recordatorio.decode(launch?.notificationResponse?.payload);
    }
  }

  Future<void> activarAvisos(bool enabled) async {
    if (enabled) await permiso();
    avisosActivos = enabled;
    preferenciaGuardada = true;
    await storage.write(key: 'dsu_avisos', value: '$enabled');
  }

  Future<void> iniciarSesion(String owner, {bool notificar = true}) async {
    if (!ready) return;
    try {
      final previous = await storage.read(key: 'dsu_avisos_owner');
      if (previous != null && previous != owner) await cerrarSesion();
      await storage.write(key: 'dsu_avisos_owner', value: owner);
      if (!preferenciaGuardada) {
        try {
          await activarAvisos(true);
        } catch (_) {
          preferenciaGuardada = true;
          await storage.write(key: 'dsu_avisos', value: 'false');
        }
      }
      if (notificar) {
        await avisar(
          1,
          'Sesión iniciada',
          'Tu cuenta está conectada al sistema DSU de Azure.',
        );
      }
    } catch (_) {
      /* Los avisos no bloquean el acceso al sistema. */
    }
  }

  Future<void> permiso() async {
    if (!ready) {
      throw StateError('Los avisos no están disponibles en este dispositivo.');
    }
    final android = plugin
        .resolvePlatformSpecificImplementation<
          AndroidFlutterLocalNotificationsPlugin
        >();
    if (await android?.requestNotificationsPermission() != true) {
      throw StateError(
        'Activa las notificaciones de DSU Campo en los ajustes del teléfono.',
      );
    }
  }

  Future<void> avisar(int id, String title, String body) async {
    if (!ready || !avisosActivos) return;
    // Un problema de Android no debe convertir un envío confirmado en un fallo.
    try {
      await plugin.show(
        id: 1000000 + id,
        title: title,
        body: body,
        notificationDetails: const NotificationDetails(
          android: AndroidNotificationDetails(
            'actividad_campo',
            'Actividad en campo',
            channelDescription:
                'Confirmaciones de las acciones realizadas en DSU Campo.',
            importance: Importance.high,
            priority: Priority.high,
            visibility: NotificationVisibility.private,
          ),
        ),
      );
    } catch (_) {
      /* La operación original conserva su resultado. */
    }
  }

  Future<void> programar(Recordatorio item) async {
    if (!ready) throw StateError('Los recordatorios no están disponibles.');
    if (!item.at.isAfter(DateTime.now()) || item.pointId <= 0) {
      throw ArgumentError('Selecciona un punto y una hora futuros.');
    }
    await permiso();
    // Intervalo absoluto: no depende del huso horario elegido por el teléfono.
    await plugin.zonedSchedule(
      id: item.pointId,
      title: 'Revisar punto ${item.code}',
      body:
          'Retoma la revisión en campo. Abre DSU Campo para consultar el punto.',
      scheduledDate: tz.TZDateTime.from(item.at, tz.UTC),
      notificationDetails: const NotificationDetails(
        android: AndroidNotificationDetails(
          'revision_puntos',
          'Revisión de puntos',
          channelDescription:
              'Recordatorios que programas para volver a un punto.',
          importance: Importance.defaultImportance,
          priority: Priority.defaultPriority,
          visibility: NotificationVisibility.private,
        ),
      ),
      androidScheduleMode: AndroidScheduleMode.inexactAllowWhileIdle,
      payload: item.encode(),
    );
  }

  Future<List<Recordatorio>> pendientes(String owner) async {
    if (!ready) return [];
    final requests = await plugin.pendingNotificationRequests();
    return requests
        .map((r) => Recordatorio.decode(r.payload))
        .whereType<Recordatorio>()
        .where((r) => r.owner == owner)
        .toList()
      ..sort((a, b) => a.at.compareTo(b.at));
  }

  Future<void> cancelar(int pointId) => plugin.cancel(id: pointId);
  Future<void> cerrarSesion() async {
    opened.value = null;
    if (ready) await plugin.cancelAll();
  }
}
