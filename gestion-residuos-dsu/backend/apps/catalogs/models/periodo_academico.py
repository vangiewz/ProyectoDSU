from django.db import models
from django.db.models import F, Q


class PeriodoAcademico(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        ordering = ["-fecha_inicio"]
        constraints = [
            models.CheckConstraint(condition=Q(fecha_fin__gt=F("fecha_inicio")), name="periodo_fechas_validas")
        ]

    def __str__(self):
        return self.nombre
