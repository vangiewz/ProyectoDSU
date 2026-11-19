from django.contrib.auth.management import create_permissions
from django.db import migrations

# Permisos por rol según las Tablas 12–16 del documento (características y restricciones del usuario).
VER_OPERACION = [
    "campus.view_sector", "campus.view_puntorecoleccion", "campus.view_contenedor",
    "catalogs.view_tiporesiduo", "catalogs.view_unidadmedida", "catalogs.view_periodoacademico",
    "operations.view_jornada", "operations.view_registroresiduo", "operations.view_incidencia",
    "operations.view_vehiculo",
]

ROLES = {
    "Supervisor": VER_OPERACION + [
        "accounts.view_user",
        "campus.change_sector", "campus.add_puntorecoleccion", "campus.change_puntorecoleccion",
        "campus.add_contenedor", "campus.change_contenedor",
        "operations.add_jornada", "operations.change_jornada", "operations.asignar_jornada",
        "operations.ejecutar_jornada", "operations.cerrar_jornada",
        "operations.add_registroresiduo", "operations.add_incidencia", "operations.atender_incidencia",
        "operations.add_vehiculo", "operations.change_vehiculo",
    ],
    "Operativo": [
        "campus.view_sector", "campus.view_puntorecoleccion",
        "catalogs.view_tiporesiduo", "catalogs.view_unidadmedida",
        "operations.view_jornada", "operations.ejecutar_jornada",
        "operations.view_registroresiduo", "operations.add_registroresiduo",
        "operations.view_incidencia", "operations.add_incidencia",
    ],
    "Administrativo": VER_OPERACION + [
        "catalogs.add_tiporesiduo", "catalogs.change_tiporesiduo",
        "catalogs.add_unidadmedida", "catalogs.change_unidadmedida",
        "audit.view_auditlog",
    ],
    "Directivo": VER_OPERACION,
}
APPS_ADMIN = ["accounts", "auth", "audit", "catalogs", "campus", "operations"]


def sembrar_roles(apps, schema_editor):
    for config in apps.get_app_configs():
        config.models_module = True
        create_permissions(config, apps=apps, verbosity=0)
        config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    def permisos(codigos):
        pares = [c.split(".") for c in codigos]
        qs = Permission.objects.none()
        for app, codename in pares:
            qs |= Permission.objects.filter(content_type__app_label=app, codename=codename)
        if qs.count() != len(pares):
            raise RuntimeError("Faltan permisos al sembrar roles")
        return qs

    admin, _ = Group.objects.get_or_create(name="Administrador")
    admin.permissions.set(Permission.objects.filter(content_type__app_label__in=APPS_ADMIN))
    for nombre, codigos in ROLES.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        grupo.permissions.set(permisos(codigos))


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0001_initial"),
        ("audit", "0001_initial"),
        ("accounts", "0001_initial"),
        ("catalogs", "0001_initial"),
        ("campus", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]
    operations = [migrations.RunPython(sembrar_roles, migrations.RunPython.noop)]
