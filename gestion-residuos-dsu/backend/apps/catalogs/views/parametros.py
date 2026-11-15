from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import RolePermission
from apps.audit.models import AuditLog
from apps.audit.services import registrar, snapshot

from ..models import ParametrosSistema
from ..serializers import ParametrosSistemaSerializer


class ParametrosView(APIView):
    """RF25: consulta y modificación de los parámetros globales; cada cambio queda en la bitácora."""

    permission_classes = [RolePermission]
    queryset = ParametrosSistema.objects.all()  # requerido por RolePermission para resolver permisos de modelo

    def get(self, request):
        return Response(ParametrosSistemaSerializer(ParametrosSistema.actual()).data)

    def patch(self, request):
        parametros = ParametrosSistema.actual()
        antes = snapshot(parametros)
        s = ParametrosSistemaSerializer(parametros, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save(actualizado_por=request.user)
        registrar(request, AuditLog.Operacion.ACTUALIZAR, parametros, antes=antes, despues=snapshot(parametros))
        return Response(s.data)
