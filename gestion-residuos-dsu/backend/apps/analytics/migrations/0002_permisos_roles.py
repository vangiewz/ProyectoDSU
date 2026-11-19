from django.contrib.auth.management import create_permissions
from django.db import migrations

# Acceso al plano analítico por rol (Tablas 13–16): consulta para supervisión y dirección;
# ETL para administración; parámetros solo para el administrador.
ROLES = {
    "Supervisor": ["analytics.view_hechoresiduo", "analytics.generar_reporte"],
    "Directivo": ["analytics.view_hechoresiduo", "analytics.generar_reporte"],
    "Administrativo": [
        "analytics.view_hechoresiduo", "analytics.generar_reporte",
        "analytics.view_ejecucionetl", "analytics.ejecutar_etl",
    ],
    "Administrador": [
        "analytics.view_hechoresiduo", "analytics.generar_reporte",
        "analytics.view_ejecucionetl", "analytics.ejecutar_etl",
        "catalogs.view_parametrossistema", "catalogs.change_parametrossistema",
    ],
}


def asignar(apps, schema_editor):
    for config in apps.get_app_configs():
        config.models_module = True
        create_permissions(config, apps=apps, verbosity=0)
        config.models_module = None
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    for nombre, codigos in ROLES.items():
        grupo = Group.objects.filter(name=nombre).first()
        if grupo is None:
            continue
        for codigo in codigos:
            app, codename = codigo.split(".")
            grupo.permissions.add(Permission.objects.get(content_type__app_label=app, codename=codename))


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0001_initial"),
        ("catalogs", "0002_parametrossistema"),
        ("operations", "0002_roles"),
    ]
    operations = [migrations.RunPython(asignar, migrations.RunPython.noop)]
