from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.analytics.models import EjecucionETL
from apps.analytics.services import etl
from apps.catalogs.models import ParametrosSistema


class Command(BaseCommand):
    help = "Ejecuta el proceso ETL (RF15). Con --programado respeta la periodicidad configurada; usar desde cron."

    def add_arguments(self, parser):
        parser.add_argument("--programado", action="store_true", help="Omite la ejecución si aún no toca.")

    def handle(self, *args, programado=False, **opts):
        if programado:
            horas = ParametrosSistema.actual().etl_periodicidad_horas
            ultima = EjecucionETL.objects.exclude(estado=EjecucionETL.Estado.FALLIDA).order_by("-inicio").first()
            if ultima and ultima.inicio > timezone.now() - timedelta(hours=horas):
                self.stdout.write(f"Última ejecución hace menos de {horas} h; no corresponde ejecutar.")
                return
        ejecucion = etl.iniciar()
        if ejecucion is None:
            self.stdout.write("Ya hay una ejecución en curso.")
            return
        ejecucion = etl.ejecutar(ejecucion)
        self.stdout.write(
            f"{ejecucion.get_estado_display()}: {ejecucion.procesados} procesados, {ejecucion.aceptados} aceptados, "
            f"{ejecucion.observados} observados. {ejecucion.mensaje}"
        )
