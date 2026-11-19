from django.forms.models import model_to_dict

from ..models import AuditLog

Op = AuditLog.Operacion


def snapshot(instance) -> dict:
    """Valores JSON: relaciones por identificador; nunca contraseñas ni sus hashes."""
    data = model_to_dict(instance, exclude=["password"])
    # model_to_dict devuelve instancias para M2M (p. ej. Permission en un rol).
    # Sus identificadores permiten auditar cambios de permisos sin serializar modelos.
    for campo in instance._meta.many_to_many:
        if campo.name in data:
            data[campo.name] = sorted(getattr(instance, campo.name).values_list("pk", flat=True))
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
