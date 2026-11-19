from rest_framework import serializers

from ..models import ParametrosSistema


class ParametrosSistemaSerializer(serializers.ModelSerializer):
    """Los validadores del modelo acotan cada valor a su rango admitido (RF25 paso 2.2)."""

    class Meta:
        model = ParametrosSistema
        exclude = ["id"]
        read_only_fields = ["actualizado_en"]
