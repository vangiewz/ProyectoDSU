from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.audit.services import registrar

from ..services import reportes as svc
from ..services.indicadores import leer_alcance

FORMATOS = {
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pdf": "application/pdf",
}


class ReportesView(APIView):
    """RF27: vista previa en JSON y exportación a Excel o PDF; cada emisión queda en la bitácora."""

    action_perms = {None: ["analytics.generar_reporte"]}

    def get(self, request, tipo: str):
        alcance = leer_alcance(request.query_params)
        reporte = svc.generar(tipo, request.user, alcance)
        formato = request.query_params.get("formato", "json")
        if formato == "json":
            return Response(
                {
                    "titulo": reporte.titulo,
                    "columnas": reporte.columnas,
                    "filas": reporte.filas,
                    "numericas": sorted(reporte.numericas),
                }
            )
        if formato not in FORMATOS:
            raise ValidationError("Formato no soportado: use xlsx o pdf.")
        contenido = (svc.a_excel if formato == "xlsx" else svc.a_pdf)(reporte, alcance)
        registrar(
            request,
            AuditLog.Operacion.EXPORTAR,
            entidad="reporte",
            detalle=f"{reporte.titulo} ({formato}), "
            f"{alcance.desde:%d/%m/%Y}-{alcance.hasta:%d/%m/%Y}, {len(reporte.filas)} filas",
        )
        respuesta = HttpResponse(contenido, content_type=FORMATOS[formato])
        disposicion = "inline" if formato == "pdf" else "attachment"
        respuesta["Content-Disposition"] = f'{disposicion}; filename="{svc.nombre_archivo(tipo, alcance, formato)}"'
        return respuesta
