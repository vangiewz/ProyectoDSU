from django.db import models

from apps.operations.models import RegistroResiduo


class RegistroDescartado(models.Model):
    """Registro transaccional que el ETL procesó y excluyó del analítico (p. ej. doble envío).

    Evita que ejecuciones posteriores lo vuelvan a extraer y lo carguen como válido.
    """

    class Motivo(models.TextChoices):
        DUPLICADO = "DUPLICADO", "Duplicado"

    registro = models.OneToOneField(RegistroResiduo, on_delete=models.PROTECT, related_name="descarte")
    motivo = models.CharField(max_length=12, choices=Motivo.choices)
    ejecucion = models.ForeignKey("EjecucionETL", on_delete=models.PROTECT, related_name="descartes")

    def __str__(self):
        return f"{self.registro_id} {self.motivo}"
