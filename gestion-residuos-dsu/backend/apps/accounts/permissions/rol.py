from rest_framework.permissions import DjangoModelPermissions

from apps.audit.models import AuditLog
from apps.audit.services import registrar


class RolePermission(DjangoModelPermissions):
    """Control de acceso por rol en los servicios (RF3, RNF16).

    Lectura exige `view_<modelo>`; escritura, los permisos de modelo de Django.
    Una vista puede fijar permisos por acción con `action_perms = {"accion": ["app.codename"]}`.
    Los rechazos quedan en la bitácora (RF3, paso 2.2).
    """

    perms_map = {
        **DjangoModelPermissions.perms_map,
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
    }

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        perms = getattr(view, "action_perms", {}).get(getattr(view, "action", None))
        permitido = request.user.has_perms(perms) if perms is not None else super().has_permission(request, view)
        if not permitido:
            registrar(
                request,
                AuditLog.Operacion.ACCESO_DENEGADO,
                entidad=view.__class__.__name__,
                detalle=f"{request.method} {request.path}",
            )
        return permitido
