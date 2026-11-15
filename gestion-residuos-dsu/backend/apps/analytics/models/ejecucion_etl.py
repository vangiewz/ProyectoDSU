from django.conf import settings
from django.db import models


class EjecucionETL(models.Model):
    """Bitácora de cada ejecución del proceso de extracción, transformación y carga (RF15, RBD19)."""

    class Estado(models.TextChoices):
        EN_CURSO = "EN_CURSO", "En curso"
        EXITOSA = "EXITOSA", "Exitosa"
        CON_ALERTA = "CON_ALERTA", "Exitosa con alerta"
        SIN_CAMBIOS = "SIN_CAMBIOS", "Sin registros nuevos"
        FALLIDA = "FALLIDA", "Fallida"

    inicio = models.DateTimeField(auto_now_add=True, db_index=True)
    fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.EN_CURSO)
    disparada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Vacío cuando la ejecutó la programación automática.",
    )
    procesados = models.PositiveIntegerField(default=0)
    aceptados = models.PositiveIntegerField(default=0)
    observados = models.PositiveIntegerField(default=0)
    duplicados = models.PositiveIntegerField(default=0)
    atipicos = models.PositiveIntegerField(default=0)
    mensaje = models.TextField(blank=True)

    class Meta:
        ordering = ["-inicio"]
        permissions = [("ejecutar_etl", "Puede ejecutar el proceso ETL bajo demanda")]

    def __str__(self):
        return f"ETL {self.inicio:%Y-%m-%d %H:%M} {self.estado}"

    @property
    def duracion_segundos(self):
        return round((self.fin - self.inicio).total_seconds(), 1) if self.fin else None
