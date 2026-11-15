from django.contrib.auth.management import create_permissions
from django.db import migrations

# Usuarios de RF22–RF24 (Tablas 40–42): el administrador entrena y publica; el administrativo consulta
# las versiones; supervisión y dirección piden predicciones; el supervisor resuelve recomendaciones.
PREDICCION = ["prediction.view_prediccion", "prediction.generar_prediccion", "prediction.view_recomendacion"]
ROLES = {
    "Administrador": [
        "prediction.view_modeloentrenado", "prediction.entrenar_modelo", "prediction.publicar_modelo",
        *PREDICCION, "prediction.resolver_recomendacion",
    ],
    "Administrativo": ["prediction.view_modeloentrenado"],
    "Supervisor": [*PREDICCION, "prediction.resolver_recomendacion"],
    "Directivo": PREDICCION,
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
    dependencies = [("prediction", "0001_initial"), ("operations", "0002_roles")]
    operations = [migrations.RunPython(asignar, migrations.RunPython.noop)]
