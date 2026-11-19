import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'api.dart';

class Reportar extends StatefulWidget {
  const Reportar({
    super.key,
    required this.api,
    required this.user,
    required this.punto,
  });
  final DsuApi api;
  final Map<String, dynamic> user, punto;
  @override
  State<Reportar> createState() => _ReportarState();
}

class _ReportarState extends State<Reportar> {
  final descripcion = TextEditingController();
  final form = GlobalKey<FormState>();
  final speech = SpeechToText();
  List<Map<String, dynamic>> jornadas = [];
  int? jornada;
  String tipo = 'OTRO', gravedad = 'MEDIA';
  String? error;
  bool loading = true, sending = false, listening = false, startingMic = false;
  bool get requiereJornada =>
      !(widget.user['is_superuser'] == true ||
          (widget.user['roles'] as List? ?? []).contains('Administrador') ||
          (widget.user['roles'] as List? ?? []).contains('Supervisor'));
  static const tipos = {
    'CONTENEDOR_DANADO': 'Contenedor dañado',
    'ACCESO_BLOQUEADO': 'Acceso bloqueado',
    'MAL_SEGREGADO': 'Residuos mal segregados',
    'RESIDUO_PELIGROSO': 'Residuo peligroso',
    'DESBORDE': 'Desborde',
    'OTRO': 'Otro',
  };
  static const gravedades = {
    'BAJA': 'Baja',
    'MEDIA': 'Media',
    'ALTA': 'Alta',
    'CRITICA': 'Crítica',
  };
  @override
  void initState() {
    super.initState();
    cargar();
  }

  @override
  void dispose() {
    speech.cancel();
    descripcion.dispose();
    super.dispose();
  }

  Future<void> cargar() async {
    try {
      final rows = await widget.api.list(
        'jornadas/?estado=EN_EJECUCION&page_size=100',
      );
      if (!mounted) return;
      setState(() {
        jornadas = rows
            .where(
              (j) => (j['ruta'] as List).any(
                (p) => p['punto'] == widget.punto['id'],
              ),
            )
            .toList();
        if (jornadas.length == 1) jornada = jornadas.first['id'] as int;
      });
    } catch (e) {
      if (mounted) setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> dictar() async {
    if (startingMic) return;
    if (listening) {
      await speech.stop();
      if (mounted) setState(() => listening = false);
      return;
    }
    setState(() {
      startingMic = true;
      error = null;
    });
    try {
      final available = await speech.initialize(
        onStatus: (status) {
          if (mounted) setState(() => listening = status == 'listening');
        },
        onError: (value) {
          if (mounted) {
            setState(() {
              listening = false;
              error =
                  'No se pudo completar el dictado. Puedes escribir la descripción.';
            });
          }
        },
      );
      if (!available) {
        throw const ApiError(
          'El dictado no está disponible o no tiene permiso. Puedes escribir la descripción.',
        );
      }
      final locales = await speech.locales();
      final spanish = locales
          .where((l) => l.localeId.startsWith('es'))
          .firstOrNull;
      if (spanish == null) {
        throw const ApiError(
          'Instala el reconocimiento de voz en español en los ajustes del teléfono.',
        );
      }
      final previous = descripcion.text.trim();
      await speech.listen(
        listenOptions: SpeechListenOptions(localeId: spanish.localeId),
        onResult: (result) {
          if (!mounted) return;
          descripcion.text = [
            previous,
            result.recognizedWords,
          ].where((s) => s.isNotEmpty).join(' ');
          descripcion.selection = TextSelection.collapsed(
            offset: descripcion.text.length,
          );
        },
      );
    } catch (e) {
      if (mounted) setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => startingMic = false);
    }
  }

  Future<void> enviar() async {
    if (!form.currentState!.validate() || sending) return;
    await speech.stop();
    if (!mounted) return;
    setState(() {
      sending = true;
      listening = false;
      error = null;
    });
    try {
      await widget.api.request(
        'incidencias/',
        body: {
          'punto': widget.punto['id'],
          'jornada': jornada,
          'tipo': tipo,
          'gravedad': gravedad,
          'descripcion': descripcion.text.trim(),
        },
      );
      if (mounted) Navigator.pop(context, true);
    } catch (e) {
      if (mounted) setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => sending = false);
    }
  }

  @override
  Widget build(BuildContext context) => PopScope(
    canPop: !sending,
    child: Scaffold(
      appBar: AppBar(title: const Text('Reportar incidencia')),
      body: SafeArea(
        child: Form(
          key: form,
          child: ListView(
            padding: const EdgeInsets.all(20),
            children: [
              Text(
                '${widget.punto['codigo']} · ${widget.punto['nombre']}',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 16),
              if (loading) const LinearProgressIndicator(),
              DropdownButtonFormField<int>(
                initialValue: jornada,
                key: ValueKey('jornada-$loading'),
                isExpanded: true,
                decoration: const InputDecoration(
                  labelText: 'Jornada en ejecución',
                ),
                items: [
                  if (!requiereJornada)
                    const DropdownMenuItem<int>(
                      value: null,
                      child: Text('Sin jornada'),
                    ),
                  for (final j in jornadas)
                    DropdownMenuItem(
                      value: j['id'] as int,
                      child: Text(
                        '#${j['id']} · ${j['fecha']} · ${j['sector_nombre']}',
                      ),
                    ),
                ],
                onChanged: loading || sending
                    ? null
                    : (v) => setState(() => jornada = v),
                validator: (_) => requiereJornada && jornada == null
                    ? 'Necesitas una jornada en ejecución asignada a este punto.'
                    : null,
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                initialValue: tipo,
                decoration: const InputDecoration(labelText: 'Tipo'),
                items: tipos.entries
                    .map(
                      (e) =>
                          DropdownMenuItem(value: e.key, child: Text(e.value)),
                    )
                    .toList(),
                onChanged: sending ? null : (v) => setState(() => tipo = v!),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                initialValue: gravedad,
                decoration: const InputDecoration(labelText: 'Gravedad'),
                items: gravedades.entries
                    .map(
                      (e) =>
                          DropdownMenuItem(value: e.key, child: Text(e.value)),
                    )
                    .toList(),
                onChanged: sending
                    ? null
                    : (v) => setState(() => gravedad = v!),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: descripcion,
                enabled: !sending,
                minLines: 4,
                maxLines: 8,
                decoration: const InputDecoration(
                  labelText: '¿Qué pasó?',
                  alignLabelWithHint: true,
                ),
                validator: (v) => v == null || v.trim().isEmpty
                    ? 'Describe lo ocurrido.'
                    : null,
              ),
              const SizedBox(height: 8),
              OutlinedButton.icon(
                onPressed: sending || startingMic ? null : dictar,
                icon: Icon(listening ? Icons.stop : Icons.mic),
                label: Text(
                  listening ? 'Detener dictado' : 'Dictar descripción',
                ),
              ),
              const Text(
                'Revisa el texto antes de enviarlo. El reconocimiento de voz depende de los servicios configurados en tu teléfono.',
              ),
              if (error != null)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  child: Text(
                    error!,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),
              const SizedBox(height: 24),
              FilledButton(
                onPressed: sending || loading || startingMic ? null : enviar,
                child: Text(sending ? 'Enviando…' : 'Enviar al sistema DSU'),
              ),
              const SizedBox(height: 12),
              const Text(
                'Este envío crea una incidencia real en el sistema compartido. Se necesita conexión a Internet.',
              ),
            ],
          ),
        ),
      ),
    ),
  );
}
