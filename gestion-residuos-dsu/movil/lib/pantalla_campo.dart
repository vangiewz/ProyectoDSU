import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import 'package:url_launcher/url_launcher.dart';
import 'api.dart';
import 'reportar.dart';
import 'recordatorios.dart';
import 'centro_avisos.dart';

class PantallaCampo extends StatefulWidget {
  const PantallaCampo({
    super.key,
    required this.api,
    required this.user,
    required this.onLogout,
    this.avisos,
  });
  final DsuApi api;
  final Recordatorios? avisos;
  final Map<String, dynamic> user;
  final Future<void> Function() onLogout;
  @override
  State<PantallaCampo> createState() => _PantallaCampoState();
}

class _PantallaCampoState extends State<PantallaCampo> {
  final map = MapController();
  List<Map<String, dynamic>> puntos = [];
  Position? position;
  bool loading = true, locating = false, leaving = false;
  String? error;
  List<Map<String, dynamic>> get cercanos {
    final ubicacion = position;
    if (ubicacion == null) return puntos;
    return ordenarPorDistancia(puntos, ubicacion.latitude, ubicacion.longitude);
  }

  bool puede(String permiso) =>
      (widget.user['permisos'] as List? ?? []).contains(permiso);
  @override
  void initState() {
    super.initState();
    widget.avisos?.opened.addListener(abrirRecordatorio);
    cargar();
  }

  @override
  void dispose() {
    widget.avisos?.opened.removeListener(abrirRecordatorio);
    map.dispose();
    super.dispose();
  }

  Future<void> cargar() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final rows = puede('campus.view_puntorecoleccion')
          ? await widget.api.list('puntos/?is_active=true&page_size=100')
          : <Map<String, dynamic>>[];
      if (!mounted) return;
      setState(() => puntos = rows);
      await widget.avisos?.avisar(
        2,
        'Puntos actualizados',
        '${rows.length} puntos disponibles según los permisos de tu cuenta.',
      );
    } catch (e) {
      if (mounted) setState(() => error = e.toString());
    } finally {
      if (mounted) {
        setState(() => loading = false);
        abrirRecordatorio();
      }
    }
  }

  Future<void> ubicar() async {
    if (locating) return;
    setState(() => locating = true);
    try {
      if (!await Geolocator.isLocationServiceEnabled()) {
        throw const ApiError('Activa la ubicación del teléfono.');
      }
      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.denied) {
        throw const ApiError(
          'Ubicación no autorizada. Puedes seguir consultando el mapa.',
        );
      }
      if (permission == LocationPermission.deniedForever) {
        throw const ApiError(
          'Habilita Ubicación en Ajustes → Aplicaciones → DSU Campo → Permisos.',
        );
      }
      final value = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
          timeLimit: Duration(seconds: 20),
        ),
      );
      if (!mounted) return;
      setState(() => position = value);
      map.move(LatLng(value.latitude, value.longitude), 16);
      if (cercanos.isNotEmpty) {
        await widget.avisos?.avisar(
          3,
          'Punto cercano encontrado',
          '${cercanos.first['codigo']} es el punto permitido más cercano. Confirma su código en campo.',
        );
      }
    } catch (e) {
      if (mounted) aviso(e.toString());
    } finally {
      if (mounted) setState(() => locating = false);
    }
  }

  void abrirRecordatorio() {
    if (!mounted || loading || leaving) return;
    final item = widget.avisos?.opened.value;
    if (item == null) return;
    widget.avisos!.opened.value = null;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      if (item.owner != '${widget.user['username']}') {
        aviso('Este recordatorio corresponde a otra cuenta.');
        return;
      }
      final punto = puntos.where((p) => p['id'] == item.pointId).firstOrNull;
      if (punto == null || !puede('campus.view_puntorecoleccion')) {
        aviso('El punto ya no está disponible para tu cuenta.');
        return;
      }
      map.move(coordenada(punto), 17);
      detalle(punto);
    });
  }

  Future<void> programarRecordatorio(Map<String, dynamic> punto) async {
    final minutos = await showModalBottomSheet<int>(
      context: context,
      builder: (ctx) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              title: Text('Volver a revisar ${punto['codigo']}'),
              subtitle: const Text(
                'Aviso local en este teléfono. La hora puede variar por ahorro de batería.',
              ),
            ),
            for (final n in [15, 30, 60])
              ListTile(
                leading: const Icon(Icons.alarm_add),
                title: Text('En $n minutos'),
                onTap: () => Navigator.pop(ctx, n),
              ),
          ],
        ),
      ),
    );
    if (minutos == null || !mounted) return;
    try {
      final at = DateTime.now().add(Duration(minutes: minutos));
      await widget.avisos!.programar(
        Recordatorio(
          '${widget.user['username']}',
          punto['id'] as int,
          '${punto['codigo']}',
          at,
        ),
      );
      if (mounted) {
        aviso(
          'Recordatorio para ${punto['codigo']} desde ${fechaRecordatorio(at)}. Puedes cancelarlo en Notificaciones.',
        );
      }
    } catch (e) {
      if (mounted) aviso(e.toString().replaceFirst('Bad state: ', ''));
    }
  }

  void aviso(String message) => ScaffoldMessenger.of(
    context,
  ).showSnackBar(SnackBar(content: Text(message)));
  LatLng coordenada(Map<String, dynamic> punto) => LatLng(
    double.parse('${punto['latitud']}'),
    double.parse('${punto['longitud']}'),
  );
  Future<void> detalle(Map<String, dynamic> punto) async {
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                '${punto['codigo']}',
                style: Theme.of(ctx).textTheme.headlineSmall,
              ),
              Text('${punto['nombre']}'),
              Text('${punto['sector_nombre'] ?? ''}'),
              if (position != null)
                Text(
                  'A ${(Geolocator.distanceBetween(position!.latitude, position!.longitude, coordenada(punto).latitude, coordenada(punto).longitude)).round()} m de tu ubicación (aprox.)',
                ),
              const SizedBox(height: 16),
              if (puede('operations.add_incidencia'))
                FilledButton.icon(
                  icon: const Icon(Icons.report_outlined),
                  label: const Text('Reportar incidencia'),
                  onPressed: () {
                    Navigator.pop(ctx);
                    reportar(punto);
                  },
                ),
              if (widget.avisos != null)
                OutlinedButton.icon(
                  icon: const Icon(Icons.add_alarm),
                  label: const Text('Recordarme revisar este punto'),
                  onPressed: () {
                    Navigator.pop(ctx);
                    programarRecordatorio(punto);
                  },
                ),
              TextButton.icon(
                icon: const Icon(Icons.directions),
                label: const Text('Abrir indicaciones'),
                onPressed: () async {
                  final c = coordenada(punto);
                  try {
                    final ok = await launchUrl(
                      Uri.https('www.google.com', '/maps/dir/', {
                        'api': '1',
                        'destination': '${c.latitude},${c.longitude}',
                        'travelmode': 'walking',
                      }),
                      mode: LaunchMode.externalApplication,
                    );
                    if (!ok && mounted) {
                      aviso('No se pudo abrir la aplicación de mapas.');
                    }
                  } catch (_) {
                    if (mounted) {
                      aviso('No se pudo abrir la aplicación de mapas.');
                    }
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> reportar(Map<String, dynamic> punto) async {
    final ok = await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (_) => Reportar(
          api: widget.api,
          user: widget.user,
          punto: punto,
          avisos: widget.avisos,
        ),
      ),
    );
    if (ok == true && mounted) {
      aviso('Incidencia registrada en el sistema DSU.');
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text('DSU Campo'),
      actions: [
        if (widget.avisos != null)
          IconButton(
            tooltip: 'Notificaciones y recordatorios',
            icon: const Icon(Icons.notifications_active_outlined),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => CentroAvisos(
                  avisos: widget.avisos!,
                  owner: '${widget.user['username']}',
                ),
              ),
            ),
          ),
        IconButton(
          tooltip: 'Actualizar puntos',
          onPressed: loading ? null : cargar,
          icon: const Icon(Icons.refresh),
        ),
        IconButton(
          tooltip: 'Cerrar sesión',
          onPressed: leaving
              ? null
              : () async {
                  setState(() => leaving = true);
                  try {
                    await widget.onLogout();
                  } catch (_) {
                    if (mounted) {
                      aviso(
                        'No se pudieron cancelar los recordatorios. Intenta cerrar sesión de nuevo.',
                      );
                    }
                  } finally {
                    if (mounted) setState(() => leaving = false);
                  }
                },
          icon: const Icon(Icons.logout),
        ),
      ],
    ),
    body: SafeArea(
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                const Icon(Icons.badge_outlined),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    '${widget.user['first_name'] ?? ''} ${widget.user['last_name'] ?? ''}'
                            .trim()
                            .isEmpty
                        ? '${widget.user['username']}'
                        : '${widget.user['first_name'] ?? ''} ${widget.user['last_name'] ?? ''}',
                  ),
                ),
                const Text('DSU', style: TextStyle(color: Color(0xff236344))),
              ],
            ),
          ),
          if (loading) const LinearProgressIndicator(),
          if (error != null)
            Padding(
              padding: const EdgeInsets.all(12),
              child: Text(error!, style: const TextStyle(color: Colors.red)),
            ),
          if (!puede('campus.view_puntorecoleccion'))
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text('Tu cuenta no tiene permiso para consultar puntos.'),
            ),
          Expanded(
            child: Stack(
              children: [
                FlutterMap(
                  mapController: map,
                  options: const MapOptions(
                    initialCenter: LatLng(-17.776, -63.195),
                    initialZoom: 15,
                  ),
                  children: [
                    TileLayer(
                      urlTemplate:
                          'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                      userAgentPackageName: 'bo.residata.dsu_movil',
                    ),
                    MarkerLayer(
                      markers: [
                        for (final p in puntos)
                          Marker(
                            point: coordenada(p),
                            width: 48,
                            height: 48,
                            child: IconButton(
                              tooltip: '${p['codigo']} · ${p['nombre']}',
                              onPressed: () => detalle(p),
                              icon: const Icon(
                                Icons.location_on,
                                size: 40,
                                color: Color(0xffc4122f),
                              ),
                            ),
                          ),
                        if (position != null)
                          Marker(
                            point: LatLng(
                              position!.latitude,
                              position!.longitude,
                            ),
                            child: const Icon(
                              Icons.my_location,
                              size: 28,
                              color: Colors.blue,
                            ),
                          ),
                      ],
                    ),
                    const SimpleAttributionWidget(
                      source: Text('OpenStreetMap contributors'),
                    ),
                  ],
                ),
                Positioned(
                  right: 16,
                  bottom: 40,
                  child: FloatingActionButton.extended(
                    heroTag: 'gps',
                    onPressed: locating || loading ? null : ubicar,
                    icon: Icon(
                      locating ? Icons.hourglass_top : Icons.my_location,
                    ),
                    label: Text(locating ? 'Buscando…' : 'Mi ubicación'),
                  ),
                ),
              ],
            ),
          ),
          if (position != null)
            ListTile(
              leading: const Icon(Icons.near_me_outlined),
              title: Text(
                cercanos.isEmpty
                    ? 'Sin puntos permitidos cercanos'
                    : 'Más cercano: ${cercanos.first['codigo']}',
              ),
              subtitle: Text(
                cercanos.isEmpty
                    ? 'Actualiza los puntos o consulta con tu supervisor.'
                    : 'A ${distanciaAlPunto(cercanos.first, position!.latitude, position!.longitude).round()} m aprox. · Confirma el código en campo',
              ),
              trailing: cercanos.isEmpty
                  ? null
                  : const Icon(Icons.chevron_right),
              onTap: cercanos.isEmpty
                  ? null
                  : () {
                      map.move(coordenada(cercanos.first), 17);
                      detalle(cercanos.first);
                    },
            ),
          if (position != null)
            Padding(
              padding: const EdgeInsets.all(8),
              child: Text(
                'GPS ±${position!.accuracy.round()} m · Solo se muestra en este teléfono',
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ),
          SizedBox(
            height: 160,
            child: puntos.isEmpty
                ? Center(
                    child: Text(
                      loading
                          ? 'Cargando puntos…'
                          : 'No hay puntos disponibles para tu cuenta.',
                    ),
                  )
                : ListView.separated(
                    itemCount: puntos.length,
                    separatorBuilder: (_, _) => const Divider(height: 1),
                    itemBuilder: (_, i) => ListTile(
                      leading: const Icon(Icons.location_on_outlined),
                      title: Text(
                        '${cercanos[i]['codigo']} · ${cercanos[i]['nombre']}',
                      ),
                      subtitle: Text('${cercanos[i]['sector_nombre'] ?? ''}'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () {
                        map.move(coordenada(cercanos[i]), 17);
                        detalle(cercanos[i]);
                      },
                    ),
                  ),
          ),
        ],
      ),
    ),
  );
}

double distanciaAlPunto(
  Map<String, dynamic> punto,
  double latitud,
  double longitud,
) => Geolocator.distanceBetween(
  latitud,
  longitud,
  double.parse('${punto['latitud']}'),
  double.parse('${punto['longitud']}'),
);

List<Map<String, dynamic>> ordenarPorDistancia(
  List<Map<String, dynamic>> puntos,
  double latitud,
  double longitud,
) => [...puntos]
  ..sort(
    (a, b) => distanciaAlPunto(
      a,
      latitud,
      longitud,
    ).compareTo(distanciaAlPunto(b, latitud, longitud)),
  );
