from .incidencia import IncidenciaSerializer
from .jornada import AsignacionSerializer, JornadaPuntoSerializer, JornadaSerializer
from .registro_residuo import RegistroResiduoSerializer
from .vehiculo import VehiculoSerializer
from .visita import DetalleVisitaSerializer, OmisionSerializer, VisitaSerializer

__all__ = [
    "VehiculoSerializer",
    "JornadaPuntoSerializer",
    "JornadaSerializer",
    "AsignacionSerializer",
    "DetalleVisitaSerializer",
    "VisitaSerializer",
    "OmisionSerializer",
    "RegistroResiduoSerializer",
    "IncidenciaSerializer",
]
