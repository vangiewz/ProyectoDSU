from apps.audit.views import AuditedViewSet

from ..models import PeriodoAcademico
from ..serializers import PeriodoAcademicoSerializer


class PeriodoAcademicoViewSet(AuditedViewSet):
    queryset = PeriodoAcademico.objects.all()
    serializer_class = PeriodoAcademicoSerializer
