from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q


class ParametrosSistema(models.Model):
    """Parámetros globales configurables sin tocar el código (RF25, RNF21). Registro único (pk=1)."""

    umbral_critico_kg_dia = models.DecimalField(
        "umbral de punto crítico (kg/día)",
        max_digits=8,
        decimal_places=2,
        default=Decimal("20"),
        validators=[MinValueValidator(Decimal("0.1"))],
        help_text="Un punto es crítico si su generación promedio diaria supera este valor.",
    )
    tolerancia_capacidad = models.DecimalField(
        "tolerancia sobre la capacidad del punto",
        max_digits=4,
        decimal_places=2,
        default=Decimal("1.5"),
        validators=[MinValueValidator(Decimal("1")), MaxValueValidator(Decimal("5"))],
        help_text="Un vaciado que supere capacidad × tolerancia se rechaza por manifiestamente excesivo.",
    )
    etl_periodicidad_horas = models.PositiveSmallIntegerField(
        "periodicidad del ETL (horas)",
        default=24,
        validators=[MinValueValidator(1), MaxValueValidator(168)],
    )
    etl_umbral_observados_pct = models.DecimalField(
        "umbral de registros observados en el ETL (%)",
        max_digits=5,
        decimal_places=2,
        default=Decimal("10"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
    )
    min_registros_entrenamiento = models.PositiveIntegerField(
        "volumen mínimo de registros para entrenar",
        default=1000,
        validators=[MinValueValidator(50)],
    )
    umbral_r2_modelo = models.DecimalField(
        "R² mínimo para publicar el modelo",
        max_digits=4,
        decimal_places=3,
        default=Decimal("0.6"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("1"))],
    )
    horizonte_max_dias = models.PositiveSmallIntegerField(
        "horizonte máximo de predicción (días)",
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(30)],
    )
    alerta_capacidad_pct = models.DecimalField(
        "ocupación proyectada que activa una alerta (%)",
        max_digits=5,
        decimal_places=2,
        default=Decimal("80"),
        validators=[MinValueValidator(Decimal("10")), MaxValueValidator(Decimal("100"))],
        help_text="Porcentaje de la capacidad del punto desde el que se emite una alerta de urgencia baja.",
    )
    crecimiento_alerta_pct = models.DecimalField(
        "crecimiento proyectado que sugiere más frecuencia (%)",
        max_digits=5,
        decimal_places=2,
        default=Decimal("20"),
        validators=[MinValueValidator(Decimal("1")), MaxValueValidator(Decimal("500"))],
    )
    no_aprovechable_max_pct = models.DecimalField(
        "proporción de residuo no aprovechable tolerada (%)",
        max_digits=5,
        decimal_places=2,
        default=Decimal("40"),
        validators=[MinValueValidator(Decimal("1")), MaxValueValidator(Decimal("100"))],
        help_text="Por encima se recomienda reforzar la separación en origen.",
    )
    url_powerbi = models.URLField(
        "enlace del informe de Power BI",
        max_length=600,
        blank=True,
        validators=[RegexValidator(r"^https://app\.powerbi\.com/", "Debe ser un enlace de app.powerbi.com.")],
        help_text="Enlace para insertar el informe publicado (Archivo → Insertar informe → Sitio web o portal).",
    )
    actualizado_en = models.DateTimeField(auto_now=True)
    actualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )

    class Meta:
        verbose_name = "parámetros del sistema"
        constraints = [models.CheckConstraint(condition=Q(pk=1), name="parametros_registro_unico")]

    def __str__(self):
        return "Parámetros del sistema"

    @classmethod
    def actual(cls) -> "ParametrosSistema":
        return cls.objects.get_or_create(pk=1)[0]
