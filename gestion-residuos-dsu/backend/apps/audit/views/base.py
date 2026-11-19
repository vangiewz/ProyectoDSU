from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import AuditLog
from ..services import registrar, snapshot

Op = AuditLog.Operacion


class AuditedViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD sin borrado físico (RNF11, RBD20); toda escritura queda en la bitácora (RF26)."""

    @transaction.atomic
    def perform_create(self, serializer):
        obj = serializer.save()
        registrar(self.request, Op.CREAR, obj, despues=snapshot(obj))

    @transaction.atomic
    def perform_update(self, serializer):
        antes = snapshot(serializer.instance)
        obj = serializer.save()
        registrar(self.request, Op.ACTUALIZAR, obj, antes=antes, despues=snapshot(obj))


class DeactivatableViewSet(AuditedViewSet):
    """Agrega baja/alta lógica mediante `is_active` (POST .../desactivar/ y .../activar/)."""

    def validar_desactivacion(self, obj, data):
        """Hook para reglas de negocio previas a la baja."""

    @action(detail=True, methods=["post"])
    def desactivar(self, request, pk=None):
        obj = self.get_object()
        if not obj.is_active:
            raise ValidationError("El registro ya está desactivado.")
        self.validar_desactivacion(obj, request.data)
        obj.is_active = False
        obj.save()
        registrar(request, Op.DESACTIVAR, obj, detalle=str(request.data.get("motivo", "")))
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=["post"])
    def activar(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = True
        obj.save()
        registrar(request, Op.ACTIVAR, obj)
        return Response(self.get_serializer(obj).data)

    def get_permissions(self):
        if self.action in ("desactivar", "activar"):
            meta = self.get_queryset().model._meta
            self.action_perms = {self.action: [f"{meta.app_label}.change_{meta.model_name}"]}
        return super().get_permissions()
