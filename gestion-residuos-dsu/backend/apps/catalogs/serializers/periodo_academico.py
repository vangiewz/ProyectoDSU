from rest_framework import serializers

from ..models import PeriodoAcademico


class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAcademico
        fields = "__all__"

    def validate(self, attrs):
        inicio = attrs.get("fecha_inicio", getattr(self.instance, "fecha_inicio", None))
        fin = attrs.get("fecha_fin", getattr(self.instance, "fecha_fin", None))
        if inicio >= fin:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la de inicio.")
        solapados = PeriodoAcademico.objects.filter(fecha_inicio__lte=fin, fecha_fin__gte=inicio)
        if self.instance:
            solapados = solapados.exclude(pk=self.instance.pk)
        if solapados.exists():
            raise serializers.ValidationError("El periodo se superpone con otro periodo académico.")
        return attrs
