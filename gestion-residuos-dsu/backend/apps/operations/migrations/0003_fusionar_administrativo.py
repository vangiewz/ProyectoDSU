from django.db import migrations

# El rol Administrativo se integra al Administrador, que ya tenía todos sus permisos
# (Fase 2, revisión del 30/10/2026: un solo actor administrador).
PERMISOS_ADMINISTRATIVO = [
    "campus.view_sector", "campus.view_puntorecoleccion", "campus.view_contenedor",
    "catalogs.view_tiporesiduo", "catalogs.view_unidadmedida", "catalogs.view_periodoacademico",
    "operations.view_jornada", "operations.view_registroresiduo", "operations.view_incidencia",
    "operations.view_vehiculo",
    "catalogs.add_tiporesiduo", "catalogs.change_tiporesiduo",
    "catalogs.add_unidadmedida", "catalogs.change_unidadmedida",
    "audit.view_auditlog",
    "analytics.view_hechoresiduo", "analytics.generar_reporte",
    "analytics.view_ejecucionetl", "analytics.ejecutar_etl",
    "prediction.view_modeloentrenado",
]


def fusionar(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    viejo = Group.objects.filter(name="Administrativo").first()
    if viejo is None:
        return
    admin = Group.objects.get(name="Administrador")
    for user in viejo.user_set.all():
        user.groups.add(admin)
    viejo.delete()


def separar(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    grupo, _ = Group.objects.get_or_create(name="Administrativo")
    for codigo in PERMISOS_ADMINISTRATIVO:
        app, codename = codigo.split(".")
        grupo.permissions.add(Permission.objects.get(content_type__app_label=app, codename=codename))


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0002_roles"),
        ("analytics", "0004_registro_descartado"),
        ("prediction", "0004_alter_modeloentrenado_options"),
    ]
    operations = [migrations.RunPython(fusionar, separar)]
