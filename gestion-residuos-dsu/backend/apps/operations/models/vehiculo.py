from django.db import models


class Vehiculo(models.Model):
    class Estado(models.TextChoices):
        OPERATIVO = "OPERATIVO", "Operativo"
        FUERA_SERVICIO = "FUERA_SERVICIO", "Fuera de servicio"

    placa = models.CharField(max_length=15, unique=True)
    descripcion = models.CharField(max_length=120)
    capacidad_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.OPERATIVO)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["placa"]

    def __str__(self):
        return self.placa
