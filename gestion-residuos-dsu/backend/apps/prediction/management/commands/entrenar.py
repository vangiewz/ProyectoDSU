from django.core.management.base import BaseCommand

from apps.prediction.services import entrenamiento


class Command(BaseCommand):
    help = "Entrena, evalúa y, si supera el umbral de R², publica una nueva versión del modelo (RF22)."

    def add_arguments(self, parser):
        for nombre, valor in entrenamiento.PROPUESTOS.items():
            parser.add_argument(f"--{nombre.replace('_', '-')}", type=int, default=valor, dest=nombre)

    def handle(self, *args, **opts):
        hiper = entrenamiento.validar_hiperparametros({k: opts[k] for k in entrenamiento.PROPUESTOS})
        modelo = entrenamiento.iniciar(hiperparametros=hiper)
        if modelo is None:
            self.stdout.write("Ya hay un entrenamiento en curso.")
            return
        modelo = entrenamiento.entrenar(modelo)
        self.stdout.write(f"Versión {modelo.version} {modelo.get_estado_display()}: {modelo.mensaje}")
        if modelo.importancias:
            self.stdout.write(
                "Importancia de variables: " + ", ".join(f"{k} {v:.3f}" for k, v in modelo.importancias.items())
            )
