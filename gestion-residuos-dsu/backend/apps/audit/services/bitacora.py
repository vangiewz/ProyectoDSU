from django.forms.models import model_to_dict

from ..models import AuditLog

Op = AuditLog.Operacion


def snapshot(instance) -> dict:
    """Valores de los campos simples de una instancia, aptos para guardar en la bitácora."""
    data = model_to_dict(instance)
    for campo in ("password", "groups", "user_permissions"):
        data.pop(campo, None)
    return data


def registrar(request, operacion, instance=None, *, antes=None, despues=None, detalle="", entidad="", usuario=None):
    """Inserta una entrada en la bitácora de auditoría (RF26)."""
    user = usuario or getattr(request, "user", None)
    meta = instance._meta if instance is not None else None
    return AuditLog.objects.create(
        usuario=user if user is not None and user.is_authenticated else None,
        modulo=meta.app_label if meta else "accounts",
        operacion=operacion,
        entidad=entidad or (meta.model_name if meta else ""),
        entidad_id=str(instance.pk) if instance is not None else "",
        detalle=detalle[:255],
        datos_anteriores=antes,
        datos_nuevos=despues,
        ip=request.META.get("REMOTE_ADDR") if request is not None else None,
    )
