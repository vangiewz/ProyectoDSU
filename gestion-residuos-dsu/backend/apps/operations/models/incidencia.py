from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.campus.models import PuntoRecoleccion

from .jornada import Jornada

User = settings.AUTH_USER_MODEL


class Incidencia(models.Model):
    class Tipo(models.TextChoices):
        CONTENEDOR_DANADO = "CONTENEDOR_DANADO", "Contenedor dañado"
        ACCESO_BLOQUEADO = "ACCESO_BLOQUEADO", "Acceso bloqueado"
        MAL_SEGREGADO = "MAL_SEGREGADO", "Residuos mal segregados"
        RESIDUO_PELIGROSO = "RESIDUO_PELIGROSO", "Residuo peligroso"
        DESBORDE = "DESBORDE", "Desborde"
        OTRO = "OTRO", "Otro"

    class Gravedad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Crítica"

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ATENDIDA = "ATENDIDA", "Atendida"

    jornada = models.ForeignKey(Jornada, null=True, blank=True, on_delete=models.PROTECT, related_name="incidencias")
    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="incidencias")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    gravedad = models.CharField(max_length=10, choices=Gravedad.choices)
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE, db_index=True)
    reportada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name="incidencias_reportadas")
    fecha_hora = models.DateTimeField(default=timezone.now, db_index=True)
    atendida_por = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT, related_name="incidencias_atendidas"
    )
    accion_adoptada = models.TextField(blank=True)
    atendida_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_hora"]
        permissions = [("atender_incidencia", "Puede atender incidencias")]

    def __str__(self):
        return f"{self.get_tipo_display()} en {self.punto.codigo}"
