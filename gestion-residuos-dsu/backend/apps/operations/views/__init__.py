from .incidencia import IncidenciaViewSet
from .jornada import JornadaViewSet
from .registro_residuo import RegistroResiduoViewSet
from .vehiculo import VehiculoViewSet

__all__ = [
    "VehiculoViewSet",
    "JornadaViewSet",
    "RegistroResiduoViewSet",
    "IncidenciaViewSet",
]
