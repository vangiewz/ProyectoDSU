import 'package:flutter/material.dart';
import 'recordatorios.dart';

class CentroAvisos extends StatefulWidget {
  const CentroAvisos({super.key, required this.avisos, required this.owner});
  final Recordatorios avisos;
  final String owner;
  @override
  State<CentroAvisos> createState() => _CentroAvisosState();
}

class _CentroAvisosState extends State<CentroAvisos> {
  List<Recordatorio> pendientes = [];
  bool busy = true;
  String? error;
  @override
  void initState() {
    super.initState();
    cargar();
  }

  Future<void> cargar() async {
    try {
      final rows = await widget.avisos.pendientes(widget.owner);
      if (mounted) setState(() => pendientes = rows);
    } catch (_) {
      if (mounted) {
        setState(() => error = 'No se pudieron consultar los recordatorios.');
      }
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> ejecutar(Future<void> Function() action) async {
    setState(() {
      busy = true;
      error = null;
    });
    try {
      await action();
    } catch (e) {
      if (mounted) {
        setState(() => error = e.toString().replaceFirst('Bad state: ', ''));
      }
    }
    await cargar();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Notificaciones')),
    body: ListView(
      padding: const EdgeInsets.all(20),
      children: [
        const Icon(
          Icons.notifications_active,
          size: 64,
          color: Color(0xffc4122f),
        ),
        const SizedBox(height: 12),
        Text(
          'Avisos de DSU Campo',
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 12),
        const Text(
          'Recibe confirmaciones de tus acciones y programa recordatorios para volver a revisar un punto.',
        ),
        const SizedBox(height: 16),
        SwitchListTile(
          title: const Text('Avisos de actividad'),
          subtitle: const Text(
            'Sesión, puntos actualizados, GPS, dictado e incidencias guardadas.',
          ),
          value: widget.avisos.avisosActivos,
          onChanged: busy
              ? null
              : (value) => ejecutar(() => widget.avisos.activarAvisos(value)),
        ),
        const SizedBox(height: 24),
        Text(
          'Recordatorios pendientes (${pendientes.length})',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const Text(
          'Programa uno desde un punto del mapa. Android puede demorar '
          'su entrega para ahorrar batería. Se cancelan al cerrar sesión.',
        ),
        if (busy) const LinearProgressIndicator(),
        if (error != null)
          Padding(
            padding: const EdgeInsets.all(12),
            child: Text(error!, style: const TextStyle(color: Colors.red)),
          ),
        if (!busy && pendientes.isEmpty)
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 24),
            child: Text('No tienes recordatorios programados.'),
          ),
        for (final item in pendientes)
          Card(
            child: ListTile(
              leading: const Icon(Icons.alarm),
              title: Text('Revisar ${item.code}'),
              subtitle: Text(
                'Desde ${fechaRecordatorio(item.at)} · hora aproximada',
              ),
              trailing: IconButton(
                tooltip: 'Cancelar recordatorio',
                icon: const Icon(Icons.close),
                onPressed: busy
                    ? null
                    : () =>
                          ejecutar(() => widget.avisos.cancelar(item.pointId)),
              ),
            ),
          ),
      ],
    ),
  );
}

String fechaRecordatorio(DateTime value) {
  final d = value.toLocal();
  String two(int n) => n.toString().padLeft(2, '0');
  return '${two(d.day)}/${two(d.month)} ${two(d.hour)}:${two(d.minute)}';
}
