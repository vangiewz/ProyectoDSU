from django.db import models

from apps.campus.models import PuntoRecoleccion, Sector
from apps.catalogs.models import TipoResiduo

from .lote_prediccion import LotePrediccion


class Prediccion(models.Model):
    """Cantidad estimada (kg) de un punto, tipo y fecha futura, siempre con su margen de error (RBD17, RNF13)."""

    lote = models.ForeignKey(LotePrediccion, on_delete=models.PROTECT, related_name="predicciones")
    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="predicciones")
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name="predicciones")
    tipo_residuo = models.ForeignKey(TipoResiduo, on_delete=models.PROTECT, related_name="predicciones")
    fecha = models.DateField()
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=3)
    margen_kg = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        ordering = ["fecha", "punto"]
        indexes = [models.Index(fields=["punto", "fecha"]), models.Index(fields=["sector", "fecha"])]

    def __str__(self):
        return f"{self.punto_id} {self.fecha} {self.cantidad_kg}±{self.margen_kg}"
