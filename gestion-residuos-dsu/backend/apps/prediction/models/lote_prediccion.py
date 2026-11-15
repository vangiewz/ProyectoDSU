from django.conf import settings
from django.db import models

from apps.campus.models import PuntoRecoleccion, Sector

from .modelo_entrenado import ModeloEntrenado


class LotePrediccion(models.Model):
    """Una solicitud de predicción (RF23): alcance, horizonte y versión del modelo que la produjo."""

    modelo = models.ForeignKey(ModeloEntrenado, on_delete=models.PROTECT, related_name="lotes")
    solicitado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    creado_en = models.DateTimeField(auto_now_add=True, db_index=True)
    desde = models.DateField()
    hasta = models.DateField()
    sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    punto = models.ForeignKey(PuntoRecoleccion, null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    puntos_omitidos = models.JSONField(default=list, help_text="Puntos del alcance sin historial suficiente.")

    class Meta:
        ordering = ["-creado_en"]
        permissions = [("generar_prediccion", "Puede generar predicciones")]

    def __str__(self):
        return f"Predicción {self.desde}–{self.hasta} (v{self.modelo.version})"
