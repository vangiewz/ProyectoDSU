from rest_framework.exceptions import ValidationError

from apps.audit.views import DeactivatableViewSet

from ..models import User
from ..serializers import UserSerializer


class UserViewSet(DeactivatableViewSet):
    """RF1: gestión de usuarios. La baja es lógica y conserva su historial."""

    queryset = User.objects.prefetch_related("groups")
    serializer_class = UserSerializer
    filterset_fields = ["is_active", "groups__name"]
    search_fields = ["username", "first_name", "last_name", "email", "ci"]

    def validar_desactivacion(self, obj, data):
        if obj == self.request.user:
            raise ValidationError("No puede desactivar su propia cuenta.")
