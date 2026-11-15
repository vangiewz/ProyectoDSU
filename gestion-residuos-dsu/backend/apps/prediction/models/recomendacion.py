from django.conf import settings
from django.db import models

from apps.campus.models import PuntoRecoleccion, Sector
from apps.operations.models import Jornada

from .lote_prediccion import LotePrediccion


class Recomendacion(models.Model):
    """Alerta o recomendación logística con su evidencia y la decisión del supervisor (RF24, RBD18).

    PRIORIZAR es la alerta temprana de desborde; las demás son acciones estructurales.
    """

    class Tipo(models.TextChoices):
        PRIORIZAR = "PRIORIZAR", "Priorizar el punto"
        INCREMENTAR_FRECUENCIA = "INCREMENTAR_FRECUENCIA", "Incrementar la frecuencia de recolección"
        REDISTRIBUIR_CONTENEDORES = "REDISTRIBUIR_CONTENEDORES", "Redistribuir o incorporar contenedores"
        REFORZAR_SEPARACION = "REFORZAR_SEPARACION", "Reforzar la separación en origen"

    class Urgencia(models.TextChoices):
        ALTA = "ALTA", "Alta"
        MEDIA = "MEDIA", "Media"
        BAJA = "BAJA", "Baja"

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ACEPTADA = "ACEPTADA", "Aceptada"
        DESCARTADA = "DESCARTADA", "Descartada"
        REEMPLAZADA = "REEMPLAZADA", "Reemplazada por una evaluación posterior"

    lote = models.ForeignKey(LotePrediccion, on_delete=models.PROTECT, related_name="recomendaciones")
    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="recomendaciones")
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name="recomendaciones")
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    urgencia = models.CharField(max_length=5, choices=Urgencia.choices)
    mensaje = models.TextField()
    evidencia = models.JSONField(default=dict)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE, db_index=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    resuelta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )
    resuelta_en = models.DateTimeField(null=True, blank=True)
    motivo_decision = models.TextField(blank=True)
    jornada = models.ForeignKey(
        Jornada,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="recomendaciones",
        help_text="Jornada planificada en la que se incorporó la recomendación aceptada.",
    )

    class Meta:
        ordering = ["estado", "urgencia", "-creada_en"]
        permissions = [("resolver_recomendacion", "Puede aceptar o descartar recomendaciones")]

    def __str__(self):
        return f"{self.get_tipo_display()} {self.punto_id} ({self.urgencia})"
