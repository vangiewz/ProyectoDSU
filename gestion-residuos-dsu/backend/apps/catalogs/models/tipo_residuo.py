from django.db import models

from .unidad_medida import UnidadMedida


class TipoResiduo(models.Model):
    class Clasificacion(models.TextChoices):
        ORGANICO = "ORGANICO", "Orgánico"
        RECICLABLE = "RECICLABLE", "Reciclable"
        NO_APROVECHABLE = "NO_APROVECHABLE", "No aprovechable"
        PELIGROSO = "PELIGROSO", "Peligroso"
        ESPECIAL = "ESPECIAL", "Especial"

    nombre = models.CharField(max_length=80, unique=True)
    clasificacion = models.CharField(max_length=20, choices=Clasificacion.choices)
    aprovechable = models.BooleanField(default=False)
    unidad = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name="tipos")
    descripcion = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
