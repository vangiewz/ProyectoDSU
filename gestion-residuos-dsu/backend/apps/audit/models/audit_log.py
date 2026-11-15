from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class AuditLog(models.Model):
    """Bitácora inalterable (RF26, RBD21): un trigger de PostgreSQL rechaza UPDATE y DELETE."""

    class Operacion(models.TextChoices):
        CREAR = "CREAR", "Crear"
        ACTUALIZAR = "ACTUALIZAR", "Actualizar"
        DESACTIVAR = "DESACTIVAR", "Desactivar"
        ACTIVAR = "ACTIVAR", "Activar"
        TRANSICION = "TRANSICION", "Cambio de estado"
        LOGIN = "LOGIN", "Inicio de sesión"
        LOGIN_FALLIDO = "LOGIN_FALLIDO", "Inicio de sesión fallido"
        LOGOUT = "LOGOUT", "Cierre de sesión"
        ACCESO_DENEGADO = "ACCESO_DENEGADO", "Acceso denegado"
        EXPORTAR = "EXPORTAR", "Emisión de reporte"
        PROCESO = "PROCESO", "Ejecución de proceso"

    fecha = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    modulo = models.CharField(max_length=50, db_index=True)
    operacion = models.CharField(max_length=20, choices=Operacion.choices, db_index=True)
    entidad = models.CharField(max_length=100)
    entidad_id = models.CharField(max_length=50, blank=True)
    detalle = models.CharField(max_length=255, blank=True)
    datos_anteriores = models.JSONField(null=True, encoder=DjangoJSONEncoder)
    datos_nuevos = models.JSONField(null=True, encoder=DjangoJSONEncoder)
    ip = models.GenericIPAddressField(null=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.fecha:%Y-%m-%d %H:%M} {self.operacion} {self.entidad}"
