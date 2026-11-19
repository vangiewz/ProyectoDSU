import 'package:flutter/material.dart';
import 'api.dart';
import 'pantalla_campo.dart';
import 'recordatorios.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final avisos = Recordatorios();
  try {
    await avisos.initialize();
  } catch (_) {
    /* La app funciona sin avisos. */
  }
  runApp(DsuApp(api: DsuApi(), avisos: avisos));
}

class DsuApp extends StatefulWidget {
  const DsuApp({super.key, required this.api, this.avisos});
  final DsuApi api;
  final Recordatorios? avisos;
  @override
  State<DsuApp> createState() => _DsuAppState();
}

class _DsuAppState extends State<DsuApp> {
  Map<String, dynamic>? user;
  bool loading = true;
  String? error;
  @override
  void initState() {
    super.initState();
    restore();
  }

  Future<void> restore() async {
    try {
      if (await widget.api.restore()) {
        user = await widget.api.request('auth/me/') as Map<String, dynamic>;
        await widget.avisos?.iniciarSesion(
          '${user!['username']}',
          notificar: false,
        );
      }
    } catch (e) {
      if (e is ApiError && e.status == 401) await widget.api.clear();
      error = e.toString();
    }
    if (mounted) setState(() => loading = false);
  }

  Future<void> signOut() async {
    String? failure;
    await widget.avisos?.cerrarSesion();
    try {
      await widget.api.logout();
    } catch (_) {
      failure =
          'Sesión borrada del teléfono. No se pudo confirmar la revocación remota.';
    }
    if (mounted) {
      setState(() {
        user = null;
        error = failure;
      });
    }
  }

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'DSU Campo',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xffc4122f)),
      scaffoldBackgroundColor: const Color(0xfff4f6f8),
      inputDecorationTheme: const InputDecorationTheme(
        border: OutlineInputBorder(),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(minimumSize: const Size(48, 52)),
      ),
    ),
    home: loading
        ? const Scaffold(body: Center(child: CircularProgressIndicator()))
        : user == null
        ? Login(
            api: widget.api,
            initialError: error,
            onLogin: (value) {
              setState(() => user = value);
              widget.avisos?.iniciarSesion('${value['username']}');
            },
          )
        : PantallaCampo(
            api: widget.api,
            user: user!,
            onLogout: signOut,
            avisos: widget.avisos,
          ),
  );
}

class Login extends StatefulWidget {
  const Login({
    super.key,
    required this.api,
    required this.onLogin,
    this.initialError,
  });
  final DsuApi api;
  final ValueChanged<Map<String, dynamic>> onLogin;
  final String? initialError;
  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  final username = TextEditingController();
  final password = TextEditingController();
  final form = GlobalKey<FormState>();
  bool busy = false;
  bool hidden = true;
  String? error;
  @override
  void initState() {
    super.initState();
    error = widget.initialError;
  }

  @override
  void dispose() {
    username.dispose();
    password.dispose();
    super.dispose();
  }

  Future<void> login() async {
    if (!form.currentState!.validate() || busy) return;
    setState(() {
      busy = true;
      error = null;
    });
    try {
      await widget.api.login(username.text, password.text);
      final user = await widget.api.request('auth/me/') as Map<String, dynamic>;
      if (mounted) widget.onLogin(user);
    } catch (e) {
      if (mounted) setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 440),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: form,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(
                    Icons.recycling,
                    size: 64,
                    color: Color(0xffc4122f),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'DSU Campo',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.headlineLarge,
                  ),
                  const Text(
                    'UAGRM · Operación móvil',
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  TextFormField(
                    controller: username,
                    enabled: !busy,
                    autocorrect: false,
                    autofillHints: const [AutofillHints.username],
                    decoration: const InputDecoration(labelText: 'Usuario'),
                    validator: (v) => v == null || v.trim().isEmpty
                        ? 'Escribe tu usuario.'
                        : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: password,
                    enabled: !busy,
                    obscureText: hidden,
                    autofillHints: const [AutofillHints.password],
                    onFieldSubmitted: (_) => login(),
                    decoration: InputDecoration(
                      labelText: 'Contraseña',
                      suffixIcon: IconButton(
                        tooltip: hidden
                            ? 'Mostrar contraseña'
                            : 'Ocultar contraseña',
                        onPressed: () => setState(() => hidden = !hidden),
                        icon: Icon(
                          hidden ? Icons.visibility : Icons.visibility_off,
                        ),
                      ),
                    ),
                    validator: (v) => v == null || v.isEmpty
                        ? 'Escribe tu contraseña.'
                        : null,
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
                    onPressed: busy ? null : login,
                    child: Text(busy ? 'Ingresando…' : 'Ingresar'),
                  ),
                  const SizedBox(height: 24),
                  const Text(
                    'Usa tu cuenta del sistema DSU. Las incidencias enviadas se guardan en el sistema compartido.',
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
