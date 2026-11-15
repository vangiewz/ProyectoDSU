from django.db import models

from apps.campus.models import PuntoRecoleccion, Sector
from apps.catalogs.models import PeriodoAcademico, TipoResiduo, UnidadMedida
from apps.operations.models import Jornada, RegistroResiduo


class HechoResiduo(models.Model):
    """Registro depurado y enriquecido por el ETL (RF15, RBD11): base de indicadores, mapas y modelo.

    Uno por registro transaccional aceptado; la cantidad se estandariza a la base de su magnitud (kg o L).
    """

    class Magnitud(models.TextChoices):
        PESO = "PESO", "Peso (kg)"
        VOLUMEN = "VOLUMEN", "Volumen (L)"

    registro = models.OneToOneField(RegistroResiduo, on_delete=models.PROTECT, related_name="hecho")
    fecha_hora = models.DateTimeField()
    fecha = models.DateField(db_index=True)
    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="hechos")
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name="hechos")
    tipo_residuo = models.ForeignKey(TipoResiduo, on_delete=models.PROTECT, related_name="hechos")
    jornada = models.ForeignKey(Jornada, on_delete=models.PROTECT, related_name="hechos")
    unidad = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name="hechos")
    cantidad_original = models.DecimalField(max_digits=10, decimal_places=3)
    magnitud = models.CharField(max_length=10, choices=Magnitud.choices, db_index=True)
    cantidad_base = models.DecimalField(max_digits=14, decimal_places=3)
    dia_semana = models.PositiveSmallIntegerField(help_text="0 = lunes … 6 = domingo")
    mes = models.PositiveSmallIntegerField()
    semana_anio = models.PositiveSmallIntegerField()
    anio = models.PositiveSmallIntegerField()
    periodo = models.ForeignKey(
        PeriodoAcademico, null=True, blank=True, on_delete=models.PROTECT, related_name="hechos"
    )
    atipico = models.BooleanField(default=False, help_text="Valor fuera del rango habitual del punto; para revisión.")
    ejecucion = models.ForeignKey("EjecucionETL", on_delete=models.PROTECT, related_name="hechos")

    class Meta:
        ordering = ["-fecha_hora"]
        indexes = [models.Index(fields=["sector", "fecha"]), models.Index(fields=["punto", "fecha"])]
        permissions = [("generar_reporte", "Puede generar y exportar reportes")]

    def __str__(self):
        return f"{self.punto_id} {self.fecha} {self.cantidad_base}"
