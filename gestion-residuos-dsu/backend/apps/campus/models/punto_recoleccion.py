from django.db import models
from django.db.models import Q

from .sector import Sector


class PuntoRecoleccion(models.Model):
    class Estado(models.TextChoices):
        OPERATIVO = "OPERATIVO", "Operativo"
        OBSERVADO = "OBSERVADO", "Observado"
        FUERA_SERVICIO = "FUERA_SERVICIO", "Fuera de servicio"

    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name="puntos")
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    referencia = models.TextField(blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    capacidad_kg = models.DecimalField("capacidad estimada (kg)", max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.OPERATIVO)
    is_active = models.BooleanField(default=True)
    motivo_baja = models.TextField(blank=True)

    class Meta:
        ordering = ["codigo"]
        constraints = [
            models.CheckConstraint(condition=Q(capacidad_kg__gt=0), name="punto_capacidad_positiva"),
            models.CheckConstraint(condition=Q(latitud__gte=-90, latitud__lte=90), name="punto_latitud_valida"),
            models.CheckConstraint(condition=Q(longitud__gte=-180, longitud__lte=180), name="punto_longitud_valida"),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
