from django.db import migrations

# Cap. 4, características del Administrador del Sistema: "no debe alterar información operativa
# sin autorización formal". La operación de campo (RF8, RF10, RF12) es del operativo y del supervisor.
CAMPO = [
    "add_registroresiduo", "ejecutar_jornada", "cerrar_jornada", "add_incidencia", "atender_incidencia",
]


def quitar(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    admin = Group.objects.get(name="Administrador")
    admin.permissions.remove(*Permission.objects.filter(content_type__app_label="operations", codename__in=CAMPO))


def devolver(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    admin = Group.objects.get(name="Administrador")
    admin.permissions.add(*Permission.objects.filter(content_type__app_label="operations", codename__in=CAMPO))


class Migration(migrations.Migration):
    dependencies = [("operations", "0003_fusionar_administrativo")]
    operations = [migrations.RunPython(quitar, devolver)]
