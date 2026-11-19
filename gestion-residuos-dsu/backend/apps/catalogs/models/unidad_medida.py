from django.db import models
from django.db.models import Q


class UnidadMedida(models.Model):
    """El factor convierte la unidad a la base de su magnitud (kg o L) para homogeneizar registros (RBD9)."""

    class Magnitud(models.TextChoices):
        PESO = "PESO", "Peso (base kg)"
        VOLUMEN = "VOLUMEN", "Volumen (base L)"

    nombre = models.CharField(max_length=50, unique=True)
    simbolo = models.CharField(max_length=10, unique=True)
    magnitud = models.CharField(max_length=10, choices=Magnitud.choices)
    factor_conversion = models.DecimalField(max_digits=12, decimal_places=6)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        constraints = [models.CheckConstraint(condition=Q(factor_conversion__gt=0), name="unidad_factor_positivo")]

    def __str__(self):
        return self.simbolo
