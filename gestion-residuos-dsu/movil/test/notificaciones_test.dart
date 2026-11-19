import 'dart:convert';
import 'package:dsu_movil/centro_avisos.dart';
import 'package:dsu_movil/recordatorios.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  const channel = MethodChannel('dexterous.com/flutter/local_notifications');
  late List<MethodCall> calls;
  var allowed = true;
  var failShow = false;
  late List<Map<String, dynamic>> pending;
  setUp(() {
    AndroidFlutterLocalNotificationsPlugin.registerWith();
    calls = [];
    pending = [];
    allowed = true;
    failShow = false;
    FlutterSecureStorage.setMockInitialValues({});
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (call) async {
          calls.add(call);
          switch (call.method) {
            case 'initialize':
              return true;
            case 'requestNotificationsPermission':
              return allowed;
            case 'getNotificationAppLaunchDetails':
              return {'notificationLaunchedApp': false};
            case 'pendingNotificationRequests':
              return pending;
            case 'show':
              if (failShow) throw PlatformException(code: 'ANDROID_DENIED');
              return null;
            default:
              return null;
          }
        });
  });
  tearDown(
    () => TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, null),
  );

  test(
    'No pide permiso al arrancar; respeta la negativa y la preferencia guardada',
    () async {
      final service = Recordatorios();
      await service.initialize();
      expect(
        calls.where((c) => c.method == 'requestNotificationsPermission'),
        isEmpty,
      );
      allowed = false;
      await service.iniciarSesion('operario');
      expect(service.avisosActivos, isFalse);
      expect(calls.where((c) => c.method == 'show'), isEmpty);
      final count = calls.length;
      await service.iniciarSesion('operario');
      expect(calls.length, count);
    },
  );

  test(
    'Un recordatorio se agenda en Android y no contiene tokens ni ubicación personal',
    () async {
      final service = Recordatorios();
      await service.initialize();
      final at = DateTime.now().add(const Duration(minutes: 15));
      await service.programar(Recordatorio('operario', 42, 'P-42', at));
      final arguments =
          calls.singleWhere((c) => c.method == 'zonedSchedule').arguments
              as Map;
      expect(arguments['id'], 42);
      final payload = jsonDecode(arguments['payload'] as String) as Map;
      expect(payload.keys.toSet(), {'owner', 'pointId', 'code', 'at'});
      expect(Recordatorio.decode(arguments['payload'])!.at.toUtc(), at.toUtc());
      expect(arguments['timeZoneName'], anyOf('UTC', 'Etc/UTC'));
      await service.cancelar(42);
      expect((calls.last.arguments as Map)['id'], 42);
    },
  );

  test(
    'Denegar notificaciones impide anunciar un recordatorio como programado',
    () async {
      final service = Recordatorios();
      await service.initialize();
      allowed = false;
      await expectLater(
        service.programar(
          Recordatorio(
            'operario',
            1,
            'P-1',
            DateTime.now().add(const Duration(minutes: 15)),
          ),
        ),
        throwsStateError,
      );
      expect(calls.where((c) => c.method == 'zonedSchedule'), isEmpty);
    },
  );

  test(
    'Los pendientes pertenecen a la cuenta y cerrar sesión cancela los avisos',
    () async {
      final service = Recordatorios();
      await service.initialize();
      for (final user in ['operario', 'otra_cuenta']) {
        pending.add({
          'id': pending.length + 1,
          'title': 'Revisar',
          'body': '',
          'payload': Recordatorio(
            user,
            pending.length + 1,
            'P',
            DateTime.now().add(const Duration(minutes: 15)),
          ).encode(),
        });
      }
      expect((await service.pendientes('operario')).map((r) => r.owner), [
        'operario',
      ]);
      service.opened.value = Recordatorio.decode(pending.first['payload']);
      await service.cerrarSesion();
      expect(service.opened.value, isNull);
      expect(calls.last.method, 'cancelAll');
    },
  );

  test(
    'Un fallo del aviso nativo no propaga error a la operación ya confirmada',
    () async {
      final service = Recordatorios();
      await service.initialize();
      await service.activarAvisos(true);
      failShow = true;
      await service.avisar(5, 'Incidencia registrada', 'Guardada en DSU.');
      expect(calls.last.method, 'show');
    },
  );

  testWidgets(
    'El centro es una configuración real, sin botones de demostración',
    (tester) async {
      final service = Recordatorios();
      await service.initialize();
      await tester.pumpWidget(
        MaterialApp(
          home: CentroAvisos(avisos: service, owner: 'operario'),
        ),
      );
      await tester.pumpAndSettle();
      expect(find.text('Avisos de actividad'), findsOneWidget);
      expect(find.text('No tienes recordatorios programados.'), findsOneWidget);
      expect(find.textContaining('Probar'), findsNothing);
    },
  );
}
