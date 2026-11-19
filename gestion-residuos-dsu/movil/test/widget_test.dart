import 'package:dsu_movil/pantalla_campo.dart';
import 'dart:convert';
import 'package:dsu_movil/api.dart';
import 'package:dsu_movil/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'GPS sugiere el punto permitido más cercano sin modificar los datos de la API',
    () {
      final puntos = <Map<String, dynamic>>[
        {'id': 1, 'latitud': '-17.78', 'longitud': '-63.20'},
        {'id': 2, 'latitud': '-17.77', 'longitud': '-63.19'},
      ];
      final ordenados = ordenarPorDistancia(puntos, -17.7701, -63.1901);
      expect(ordenados.first['id'], 2);
      expect(puntos.first['id'], 1);
      expect(
        distanciaAlPunto(ordenados.first, -17.7701, -63.1901),
        lessThan(20),
      );
    },
  );
  setUp(() => FlutterSecureStorage.setMockInitialValues({}));
  test(
    'El login guarda refresh en almacenamiento seguro; no guarda contraseña',
    () async {
      final api = DsuApi(
        client: MockClient((r) async {
          expect(r.url.path, '/api/auth/login/');
          expect(jsonDecode(r.body), {
            'username': 'prueba',
            'password': 'solo-test',
          });
          return http.Response(
            '{"access":"access-test","refresh":"refresh-test"}',
            200,
          );
        }),
      );
      await api.login(' prueba ', 'solo-test');
      expect(await api.storage.readAll(), {'dsu_refresh': 'refresh-test'});
    },
  );
  test('Renueva JWT ante 401 y repite la lectura con el token nuevo', () async {
    var calls = 0;
    final api =
        DsuApi(
            client: MockClient((r) async {
              calls++;
              if (r.url.path.endsWith('refresh/')) {
                return http.Response('{"access":"nuevo"}', 200);
              }
              if (r.headers['Authorization'] == 'Bearer nuevo') {
                return http.Response('{"id":1}', 200);
              }
              return http.Response('{"detail":"expirado"}', 401);
            }),
          )
          ..access = 'anterior'
          ..refresh = 'refresh-test';
    expect((await api.request('auth/me/'))['id'], 1);
    expect(calls, 3);
  });
  test('No filtra el JWT hacia URLs ajenas recibidas por paginación', () async {
    var calls = 0;
    final api = DsuApi(
      client: MockClient((r) async {
        calls++;
        return http.Response(
          '{"results":[],"next":"https://example.com/api/puntos/"}',
          200,
        );
      }),
    )..access = 'privado';
    await expectLater(api.list('puntos/'), throwsA(isA<ApiError>()));
    expect(calls, 1);
  });
  test('Une las páginas para no perder puntos', () async {
    final api = DsuApi(
      client: MockClient(
        (r) async => http.Response(
          r.url.query.isEmpty
              ? '{"results":[{"id":1}],"next":"${DsuApi.base}puntos/?page=2"}'
              : '{"results":[{"id":2}],"next":null}',
          200,
        ),
      ),
    );
    expect((await api.list('puntos/')).map((p) => p['id']), [1, 2]);
  });
  test('Un error de validación conserva el mensaje del servidor', () async {
    final api = DsuApi(
      client: MockClient(
        (r) async => http.Response('{"punto":["Fuera de alcance"]}', 400),
      ),
    );
    await expectLater(
      api.request('incidencias/', body: {'punto': 4}),
      throwsA(
        isA<ApiError>().having(
          (e) => e.message,
          'mensaje',
          contains('Fuera de alcance'),
        ),
      ),
    );
  });
  test(
    'El logout borra el token local aunque no se confirme la revocación remota',
    () async {
      FlutterSecureStorage.setMockInitialValues({
        'dsu_refresh': 'refresh-test',
      });
      final api =
          DsuApi(
              client: MockClient(
                (r) async => http.Response('{"detail":"error"}', 503),
              ),
            )
            ..refresh = 'refresh-test'
            ..access = 'access-test';
      await expectLater(api.logout(), throwsA(isA<ApiError>()));
      expect(await api.storage.readAll(), isEmpty);
      expect(api.access, isNull);
    },
  );
  testWidgets(
    'El formulario solicita usuario y contraseña antes de contactar Azure',
    (tester) async {
      var calls = 0;
      final api = DsuApi(
        client: MockClient((r) async {
          calls++;
          return http.Response('{}', 200);
        }),
      );
      await tester.pumpWidget(DsuApp(api: api));
      await tester.pumpAndSettle();
      expect(find.text('DSU Campo'), findsOneWidget);
      await tester.tap(find.widgetWithText(FilledButton, 'Ingresar'));
      await tester.pumpAndSettle();
      expect(find.text('Escribe tu usuario.'), findsOneWidget);
      expect(find.text('Escribe tu contraseña.'), findsOneWidget);
      expect(calls, 0);
    },
  );
}
