from decimal import Decimal

from rest_framework import serializers

from ..models import UnidadMedida


class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = "__all__"
        read_only_fields = ["is_active"]
        extra_kwargs = {"factor_conversion": {"min_value": Decimal("0.000001")}}

    def validate(self, attrs):
        # RF6 exc. 3: no alterar la conversión de una unidad ya usada en el histórico.
        u = self.instance
        if u and u.registros.exists():
            for campo in ("factor_conversion", "magnitud"):
                if campo in attrs and attrs[campo] != getattr(u, campo):
                    raise serializers.ValidationError(
                        {campo: "La unidad ya tiene registros históricos; cree una unidad nueva."}
                    )
        return attrs
