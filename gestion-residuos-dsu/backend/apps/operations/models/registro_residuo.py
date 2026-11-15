from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import TipoResiduo, UnidadMedida

from .jornada import Jornada

User = settings.AUTH_USER_MODEL


class RegistroResiduo(models.Model):
    """Núcleo transaccional (RF8). Nunca se elimina: es el histórico de entrenamiento (RNF11, RBD13)."""

    jornada = models.ForeignKey(Jornada, on_delete=models.PROTECT, related_name="registros")
    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="registros")
    tipo_residuo = models.ForeignKey(TipoResiduo, on_delete=models.PROTECT, related_name="registros")
    unidad = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name="registros")
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name="registros")
    fecha_hora = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-fecha_hora"]
        constraints = [models.CheckConstraint(condition=Q(cantidad__gt=0), name="registro_cantidad_positiva")]

    def __str__(self):
        return f"{self.punto.codigo} {self.cantidad} {self.unidad.simbolo}"
