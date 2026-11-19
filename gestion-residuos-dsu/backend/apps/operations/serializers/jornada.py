from django.db import transaction
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.permissions import exigir_sector
from apps.campus.models import PuntoRecoleccion

from ..models import Jornada, JornadaPunto, Vehiculo


class JornadaPuntoSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(source="punto.codigo", read_only=True)
    nombre = serializers.CharField(source="punto.nombre", read_only=True)
    latitud = serializers.DecimalField(source="punto.latitud", max_digits=9, decimal_places=6, read_only=True)
    longitud = serializers.DecimalField(source="punto.longitud", max_digits=9, decimal_places=6, read_only=True)

    class Meta:
        model = JornadaPunto
        fields = [
            "id",
            "punto",
            "codigo",
            "nombre",
            "latitud",
            "longitud",
            "orden",
            "atendido",
            "sin_generacion",
            "motivo_omision",
            "atendido_en",
        ]


class JornadaSerializer(serializers.ModelSerializer):
    """RF11: la ruta se envía como lista ordenada de ids de puntos en `puntos`."""

    puntos = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=PuntoRecoleccion.objects.select_related("sector")
    )
    ruta = JornadaPuntoSerializer(many=True, read_only=True)
    sector_nombre = serializers.CharField(source="sector.nombre", read_only=True)
    turno_display = serializers.CharField(source="get_turno_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    responsable_nombre = serializers.CharField(source="responsable.get_full_name", read_only=True, default=None)
    personal_detalle = serializers.SerializerMethodField()
    puntos_planificados = serializers.IntegerField(read_only=True)
    puntos_atendidos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Jornada
        fields = "__all__"
        read_only_fields = [
            "estado",
            "planificada_por",
            "responsable",
            "personal",
            "vehiculos",
            "hora_inicio",
            "hora_fin",
            "observaciones_cierre",
        ]

    def get_personal_detalle(self, obj):
        return [{"id": u.id, "nombre": u.get_full_name() or u.username} for u in obj.personal.all()]

    def validate_sector(self, sector):
        if not sector.is_active:
            raise serializers.ValidationError("El sector está desactivado.")
        exigir_sector(self.context["request"].user, sector)
        return sector

    def validate(self, attrs):
        if self.instance and self.instance.estado not in (Jornada.Estado.PLANIFICADA, Jornada.Estado.CONFIRMADA):
            raise serializers.ValidationError("La jornada ya está en ejecución o cerrada; no puede modificarse.")
        sector = attrs.get("sector", getattr(self.instance, "sector", None))
        puntos = attrs.get("puntos")
        if puntos is None and self.instance is not None and "sector" in attrs:
            puntos = [parada.punto for parada in self.instance.ruta.select_related("punto")]
        if puntos is not None:
            if not puntos:
                raise serializers.ValidationError({"puntos": "La ruta debe incluir al menos un punto."})
            if len(set(puntos)) != len(puntos):
                raise serializers.ValidationError({"puntos": "La ruta tiene puntos repetidos."})
            for p in puntos:
                if not p.is_active:
                    raise serializers.ValidationError({"puntos": f"El punto {p.codigo} está desactivado."})
                if p.sector_id != sector.id:
                    raise serializers.ValidationError({"puntos": f"El punto {p.codigo} no pertenece al sector."})
        elif self.instance is None:
            raise serializers.ValidationError({"puntos": "La ruta debe incluir al menos un punto."})
        return attrs

    def _guardar_ruta(self, jornada, puntos):
        jornada.ruta.all().delete()
        JornadaPunto.objects.bulk_create(
            JornadaPunto(jornada=jornada, punto=p, orden=i) for i, p in enumerate(puntos, start=1)
        )

    @transaction.atomic
    def create(self, validated_data):
        puntos = validated_data.pop("puntos")
        jornada = Jornada.objects.create(planificada_por=self.context["request"].user, **validated_data)
        self._guardar_ruta(jornada, puntos)
        return jornada

    @transaction.atomic
    def update(self, instance, validated_data):
        puntos = validated_data.pop("puntos", None)
        jornada = super().update(instance, validated_data)
        if puntos is not None:
            self._guardar_ruta(jornada, puntos)
        return jornada


class AsignacionSerializer(serializers.Serializer):
    personal = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.prefetch_related("groups"))
    vehiculos = serializers.PrimaryKeyRelatedField(many=True, queryset=Vehiculo.objects.all(), required=False)
    responsable = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
