from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.accounts.permissions import filtrar_por_sector
from apps.audit.views import AuditedViewSet

from .. import services
from ..filters.jornada import JornadaFilter
from ..models import Jornada, JornadaPunto
from ..serializers import (
    AsignacionSerializer,
    JornadaSerializer,
    OmisionSerializer,
    RegistroResiduoSerializer,
    VisitaSerializer,
)

RUTA = JornadaPunto.objects.select_related("punto").only(
    *("jornada", "punto", "orden", "atendido", "sin_generacion", "motivo_omision", "atendido_en"),
    *("punto__codigo", "punto__nombre", "punto__latitud", "punto__longitud"),
)


class JornadaViewSet(AuditedViewSet):
    """RF11–RF14: planificación, asignación, ejecución e historial de jornadas."""

    serializer_class = JornadaSerializer
    filterset_class = JornadaFilter
    ordering_fields = ["fecha", "estado"]
    action_perms = {
        "asignar": ["operations.asignar_jornada"],
        "confirmar": ["operations.change_jornada"],
        "abrir": ["operations.ejecutar_jornada"],
        "visitas": ["operations.add_registroresiduo"],
        "omitir": ["operations.ejecutar_jornada"],
        "cerrar": ["operations.cerrar_jornada"],
        "resumen": ["operations.view_jornada"],
        "mias": ["operations.view_jornada"],
    }

    def get_queryset(self):
        user = self.request.user
        qs = (
            Jornada.objects.select_related("sector", "responsable")
            .defer("responsable__password")
            # Solo los campos que usa el serializer: con muchas jornadas, el volumen transferido manda (RTR2).
            .prefetch_related(
                Prefetch("personal", queryset=User.objects.only("id", "username", "first_name", "last_name")),
                "vehiculos",
                Prefetch("ruta", queryset=RUTA),
            )
            .annotate(
                puntos_planificados=Count("ruta", distinct=True),
                puntos_atendidos=Count("ruta", filter=Q(ruta__atendido=True), distinct=True),
            )
            .order_by("-fecha", "turno")
        )
        return filtrar_por_sector(qs, user, "sector", Q(personal=user))

    @action(detail=False)
    def mias(self, request):
        """Jornadas del día en las que participa el usuario (pantalla de campo)."""
        qs = self.get_queryset().filter(
            personal=request.user,
            fecha=timezone.localdate(),
            estado__in=[Jornada.Estado.CONFIRMADA, Jornada.Estado.EN_EJECUCION],
        )
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=True, methods=["post"])
    def asignar(self, request, pk=None):
        jornada = self.get_object()
        s = AsignacionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        services.asignar(
            request,
            jornada,
            s.validated_data["personal"],
            s.validated_data.get("vehiculos", []),
            s.validated_data["responsable"],
        )
        return Response(self.get_serializer(self.get_object()).data)

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        services.confirmar(request, self.get_object())
        return Response(self.get_serializer(self.get_object()).data)

    @action(detail=True, methods=["post"])
    def abrir(self, request, pk=None):
        services.abrir(request, self.get_object())
        return Response(self.get_serializer(self.get_object()).data)

    @action(detail=True, methods=["post"])
    def visitas(self, request, pk=None):
        jornada = self.get_object()
        s = VisitaSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        registros = services.registrar_visita(request, jornada, **s.validated_data)
        return Response(RegistroResiduoSerializer(registros, many=True).data, status=201)

    @action(detail=True, methods=["post"])
    def omitir(self, request, pk=None):
        s = OmisionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        services.omitir_punto(request, self.get_object(), **s.validated_data)
        return Response(self.get_serializer(self.get_object()).data)

    @action(detail=True, methods=["post"])
    def cerrar(self, request, pk=None):
        services.cerrar(request, self.get_object(), str(request.data.get("observaciones", "")))
        return Response(self.get_serializer(self.get_object()).data)

    @action(detail=True)
    def resumen(self, request, pk=None):
        return Response(services.resumen(self.get_object()))
