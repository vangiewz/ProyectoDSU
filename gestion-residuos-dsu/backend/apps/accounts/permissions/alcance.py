from rest_framework.exceptions import PermissionDenied

from ..models import Rol


def es_supervisor_restringido(user) -> bool:
    return not user.acceso_global and Rol.SUPERVISOR in user.roles


def filtrar_por_sector(qs, user, ruta_sector: str, filtro_operativo=None):
    """Restricción territorial: el supervisor ve sus sectores; el operativo, lo de sus jornadas."""
    if user.acceso_global:
        return qs
    if Rol.SUPERVISOR in user.roles:
        campo = f"{ruta_sector}__supervisor" if ruta_sector else "supervisor"
        return qs.filter(**{campo: user})
    if Rol.OPERATIVO in user.roles and filtro_operativo is not None:
        # Subconsulta por pk: evita duplicar filas (y agregados) al cruzar relaciones múltiples.
        return qs.filter(pk__in=qs.model.objects.filter(filtro_operativo).values("pk"))
    return qs.none()


def exigir_sector(user, sector):
    if es_supervisor_restringido(user) and sector.supervisor_id != user.id:
        raise PermissionDenied("No tiene permisos sobre el sector indicado.")
