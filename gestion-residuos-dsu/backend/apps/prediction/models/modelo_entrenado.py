from django.conf import settings
from django.db import models
from django.db.models import Q


class SinArtefacto(models.Manager):
    """El modelo serializado pesa megabytes: solo se descarga cuando se pide explícitamente."""

    def get_queryset(self):
        return super().get_queryset().defer("artefacto")


class ModeloEntrenado(models.Model):
    """Cada ejecución del entrenamiento (RF22, RBD16) es una versión del modelo; una sola es la vigente (RD13)."""

    class Estado(models.TextChoices):
        EN_CURSO = "EN_CURSO", "En curso"
        APROBADO = "APROBADO", "Aprobado"
        RECHAZADO = "RECHAZADO", "Rechazado"
        FALLIDO = "FALLIDO", "Fallido"

    version = models.PositiveIntegerField(unique=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.EN_CURSO)
    vigente = models.BooleanField(default=False, help_text="Versión que usan las predicciones.")
    inicio = models.DateTimeField(auto_now_add=True)
    fin = models.DateTimeField(null=True, blank=True)
    entrenado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Vacío cuando se entrenó desde la línea de comandos.",
    )
    hiperparametros = models.JSONField(default=dict)
    variables = models.JSONField(default=list)
    registros = models.PositiveIntegerField(default=0, help_text="Hechos depurados usados.")
    observaciones_entrenamiento = models.PositiveIntegerField(default=0)
    observaciones_prueba = models.PositiveIntegerField(default=0)
    corte = models.DateField(null=True, blank=True, help_text="Primera fecha del conjunto de prueba.")
    # Métricas estadísticas de evaluación (no son cantidades de residuo).
    mae = models.FloatField(null=True, blank=True)
    mse = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True)
    r2 = models.FloatField(null=True, blank=True)
    umbral_r2 = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    importancias = models.JSONField(default=dict)
    mensaje = models.TextField(blank=True)
    # ponytail: el modelo serializado vive en la BD (un solo despliegue, sin disco persistente);
    # pasar a almacenamiento de archivos si los artefactos crecen demasiado.
    artefacto = models.BinaryField(null=True, editable=False)

    objects = SinArtefacto()

    class Meta:
        base_manager_name = "objects"  # también al llegar desde un lote (lote.modelo)
        ordering = ["-version"]
        constraints = [models.UniqueConstraint(fields=["vigente"], condition=Q(vigente=True), name="un_modelo_vigente")]
        permissions = [
            ("entrenar_modelo", "Puede entrenar el modelo predictivo"),
            ("publicar_modelo", "Puede publicar o revertir versiones del modelo"),
        ]

    def __str__(self):
        return f"Modelo v{self.version} {self.estado}"
