import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class ApiError implements Exception {
  const ApiError(this.message, [this.status = 0]);
  final String message;
  final int status;
  @override
  String toString() => message;
}

class DsuApi {
  DsuApi({http.Client? client, FlutterSecureStorage? storage})
    : client = client ?? http.Client(),
      storage = storage ?? const FlutterSecureStorage();
  static const base = String.fromEnvironment(
    'DSU_API_URL',
    defaultValue: 'https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com/api/',
  );
  final http.Client client;
  final FlutterSecureStorage storage;
  String? access;
  String? refresh;
  Future<void>? _renewing;

  Future<bool> restore() async {
    refresh = await storage.read(key: 'dsu_refresh');
    if (refresh == null) return false;
    await _renew();
    return true;
  }

  Future<void> login(String username, String password) async {
    final data = await request(
      'auth/login/',
      body: {'username': username.trim(), 'password': password},
      authenticated: false,
    );
    access = data['access'] as String;
    refresh = data['refresh'] as String;
    await storage.write(key: 'dsu_refresh', value: refresh);
  }

  Future<void> _renew() async {
    if (refresh == null) {
      throw const ApiError('Inicia sesión para continuar.', 401);
    }
    final data = await request(
      'auth/refresh/',
      body: {'refresh': refresh},
      authenticated: false,
    );
    access = data['access'] as String;
    if (data['refresh'] != null) {
      refresh = data['refresh'] as String;
      await storage.write(key: 'dsu_refresh', value: refresh);
    }
  }

  Future<void> clear() async {
    access = null;
    refresh = null;
    await storage.delete(key: 'dsu_refresh');
  }

  Future<void> logout() async {
    try {
      if (refresh != null) {
        await request('auth/logout/', body: {'refresh': refresh});
      }
    } finally {
      await clear();
    }
  }

  Future<dynamic> request(
    String path, {
    Map<String, dynamic>? body,
    bool authenticated = true,
    bool retry = true,
  }) async {
    final root = Uri.parse(base);
    final uri = root.resolve(path);
    if (uri.origin != root.origin || !uri.path.startsWith(root.path)) {
      throw const ApiError('La API devolvió una dirección inesperada.');
    }
    final headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      if (authenticated && access != null) 'Authorization': 'Bearer $access',
    };
    late http.Response response;
    try {
      response =
          await (body == null
                  ? client.get(uri, headers: headers)
                  : client.post(uri, headers: headers, body: jsonEncode(body)))
              .timeout(const Duration(seconds: 30));
    } on TimeoutException {
      throw const ApiError(
        'El servidor tardó en responder. Comprueba el resultado antes de reenviar.',
      );
    } on SocketException {
      throw const ApiError(
        'Sin conexión. Revisa Internet e inténtalo de nuevo.',
      );
    } on http.ClientException {
      throw const ApiError('No se pudo conectar con el servidor.');
    }
    if (response.statusCode == 401 &&
        authenticated &&
        retry &&
        refresh != null) {
      final pending = _renewing ??= _renew();
      try {
        await pending;
      } finally {
        if (identical(_renewing, pending)) _renewing = null;
      }
      return request(path, body: body, retry: false);
    }
    dynamic data;
    try {
      data = response.body.isEmpty
          ? null
          : jsonDecode(utf8.decode(response.bodyBytes));
    } on FormatException {
      throw ApiError(
        'Respuesta inesperada del servidor (${response.statusCode}).',
        response.statusCode,
      );
    }
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw ApiError(_message(data), response.statusCode);
    }
    return data;
  }

  static String _message(dynamic data) {
    if (data is Map) {
      return data.entries
          .map(
            (e) => e.key == 'detail'
                ? '${e.value}'
                : '${e.key}: ${e.value is List ? (e.value as List).join(', ') : e.value}',
          )
          .join('\n');
    }
    return 'No se pudo completar la operación.';
  }

  Future<List<Map<String, dynamic>>> list(String path) async {
    final result = <Map<String, dynamic>>[];
    String? next = path;
    final visited = <String>{};
    while (next != null) {
      if (!visited.add(next) || visited.length > 100) {
        throw const ApiError('Paginación inesperada.');
      }
      final data = await request(next);
      final rows = data is List ? data : data['results'] as List;
      result.addAll(rows.cast<Map<String, dynamic>>());
      next = data is List ? null : data['next'] as String?;
    }
    return result;
  }
}
