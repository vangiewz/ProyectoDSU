from django.conf import settings
from django.db import models


class Sector(models.Model):
    class Tipo(models.TextChoices):
        FACULTAD = "FACULTAD", "Facultad"
        MODULO = "MODULO", "Módulo"
        AREA_COMUN = "AREA_COMUN", "Área común"
        UNIDAD_DESCONCENTRADA = "UNIDAD_DESCONCENTRADA", "Unidad desconcentrada"

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=25, choices=Tipo.choices, default=Tipo.FACULTAD)
    descripcion = models.TextField(blank=True)
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="sectores"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
