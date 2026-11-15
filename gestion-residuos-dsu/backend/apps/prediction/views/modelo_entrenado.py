from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import ModeloEntrenado
from ..serializers import ModeloEntrenadoSerializer
from ..services import entrenamiento


class ModeloEntrenadoViewSet(viewsets.ReadOnlyModelViewSet):
    """RF22: versiones del modelo con sus métricas, entrenamiento en segundo plano y publicación o reversión."""

    queryset = ModeloEntrenado.objects.select_related("entrenado_por").defer("artefacto")
    serializer_class = ModeloEntrenadoSerializer
    filterset_fields = ["estado", "vigente"]
    action_perms = {"entrenar": ["prediction.entrenar_modelo"], "publicar": ["prediction.publicar_modelo"]}

    @action(detail=False)
    def propuestos(self, request):
        """Hiperparámetros propuestos y su rango admitido (RF22 paso 3.1)."""
        return Response({"valores": entrenamiento.PROPUESTOS, "limites": entrenamiento.LIMITES})

    @action(detail=False, methods=["post"])
    def entrenar(self, request):
        hiper = entrenamiento.validar_hiperparametros(request.data)
        modelo = entrenamiento.iniciar(request.user, hiper)
        if modelo is None:
            return Response({"detail": "Ya hay un entrenamiento en curso."}, status=status.HTTP_409_CONFLICT)
        entrenamiento.entrenar_en_segundo_plano(modelo)
        return Response(self.get_serializer(modelo).data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def publicar(self, request, pk=None):
        return Response(self.get_serializer(entrenamiento.publicar(request, self.get_object())).data)
