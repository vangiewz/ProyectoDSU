from django.db import models
from django.db.models import Q

from .punto_recoleccion import PuntoRecoleccion


class Contenedor(models.Model):
    class Estado(models.TextChoices):
        BUENO = "BUENO", "Bueno"
        DETERIORADO = "DETERIORADO", "Deteriorado"
        REEMPLAZADO = "REEMPLAZADO", "Reemplazado"
        REUBICADO = "REUBICADO", "Reubicado"
        BAJA = "BAJA", "De baja"

    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="contenedores")
    codigo = models.CharField(max_length=30, unique=True)
    tipo = models.CharField(max_length=60)
    capacidad_litros = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_instalacion = models.DateField()
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.BUENO)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ["punto__codigo", "codigo"]
        constraints = [
            models.CheckConstraint(condition=Q(capacidad_litros__gt=0), name="contenedor_capacidad_positiva")
        ]

    def __str__(self):
        return self.codigo
