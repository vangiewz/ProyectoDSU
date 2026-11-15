from django.conf import settings
from django.db import models

from apps.campus.models import PuntoRecoleccion, Sector

from .vehiculo import Vehiculo

User = settings.AUTH_USER_MODEL


class Jornada(models.Model):
    """Jornada de recolección: planificación (RF11), asignación (RF13) y ejecución (RF12)."""

    class Turno(models.TextChoices):
        MANANA = "MANANA", "Mañana"
        TARDE = "TARDE", "Tarde"
        NOCHE = "NOCHE", "Noche"

    class Estado(models.TextChoices):
        PLANIFICADA = "PLANIFICADA", "Planificada"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        EN_EJECUCION = "EN_EJECUCION", "En ejecución"
        CERRADA = "CERRADA", "Cerrada"

    fecha = models.DateField(db_index=True)
    turno = models.CharField(max_length=10, choices=Turno.choices)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name="jornadas")
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.PLANIFICADA, db_index=True)
    descripcion = models.CharField(max_length=255, blank=True)
    planificada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name="jornadas_planificadas")
    responsable = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT, related_name="jornadas_responsable"
    )
    personal = models.ManyToManyField(User, blank=True, related_name="jornadas_asignadas")
    vehiculos = models.ManyToManyField(Vehiculo, blank=True, related_name="jornadas")
    hora_inicio = models.DateTimeField(null=True, blank=True)
    hora_fin = models.DateTimeField(null=True, blank=True)
    observaciones_cierre = models.TextField(blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "turno"]
        constraints = [models.UniqueConstraint(fields=["fecha", "turno", "sector"], name="jornada_unica_por_turno")]
        permissions = [
            ("asignar_jornada", "Puede asignar personal y vehículos a jornadas"),
            ("ejecutar_jornada", "Puede abrir jornadas y registrar su avance"),
            ("cerrar_jornada", "Puede cerrar jornadas"),
        ]

    def __str__(self):
        return f"{self.fecha} {self.get_turno_display()} - {self.sector.codigo}"


class JornadaPunto(models.Model):
    """Punto de la ruta. atendido=None pendiente, True atendido, False omitido con motivo (RBD15)."""

    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, related_name="ruta")
    punto = models.ForeignKey(PuntoRecoleccion, on_delete=models.PROTECT, related_name="en_rutas")
    orden = models.PositiveSmallIntegerField()
    atendido = models.BooleanField(null=True)
    sin_generacion = models.BooleanField(default=False)
    motivo_omision = models.TextField(blank=True)
    atendido_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["jornada", "orden"]
        constraints = [models.UniqueConstraint(fields=["jornada", "punto"], name="punto_unico_en_jornada")]

    def __str__(self):
        return f"{self.orden}. {self.punto.codigo}"
