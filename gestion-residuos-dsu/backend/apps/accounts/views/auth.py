from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.audit.models import AuditLog
from apps.audit.services import registrar

from ..models import User
from ..serializers import MeSerializer

Op = AuditLog.Operacion


class LoginView(TokenObtainPairView):
    """RF3: emite access + refresh JWT; registra aciertos y fallos en la bitácora."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception:
            registrar(request, Op.LOGIN_FALLIDO, entidad="user", detalle=str(request.data.get("username", ""))[:150])
            raise
        user = User.objects.get(username=request.data["username"])
        registrar(request, Op.LOGIN, user, usuario=user)
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            RefreshToken(request.data.get("refresh")).blacklist()
        except TokenError as err:
            raise ValidationError({"refresh": "Token inválido o ya revocado."}) from err
        registrar(request, Op.LOGOUT, request.user)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)
