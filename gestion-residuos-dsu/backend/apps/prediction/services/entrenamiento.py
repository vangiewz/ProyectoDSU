"""Entrenamiento, evaluación, publicación y reversión del Random Forest Regressor (RF22, RD5, RD13)."""

import logging
import threading
from datetime import timedelta
from functools import lru_cache
from io import BytesIO
from pathlib import Path

import joblib
import numpy as np
from django.conf import settings
from django.db import close_old_connections, connection, transaction
from django.db.models import Max
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from apps.audit.models import AuditLog
from apps.audit.services import registrar
from apps.catalogs.models import ParametrosSistema
from config.concurrencia import bloquear_proceso

from ..models import ModeloEntrenado
from . import datos

log = logging.getLogger(__name__)
E = ModeloEntrenado.Estado

# Hiperparámetros propuestos (RF22 3.1) y rango admitido para cada uno.
# Con el histórico de demostración rinden lo mismo que 200/14/3 con un artefacto cuatro veces menor.
PROPUESTOS = {"n_estimators": 100, "max_depth": 12, "min_samples_leaf": 5}
LIMITES = {"n_estimators": (10, 500), "max_depth": (2, 40), "min_samples_leaf": (1, 50)}
PROPORCION_PRUEBA = 0.2


def _es(x: float, decimales: int) -> str:
    """Número con coma decimal, como se lee en Bolivia."""
    return f"{x:.{decimales}f}".replace(".", ",")


VENCIMIENTO_EN_CURSO = timedelta(minutes=30)  # RTR12: un entrenamiento completo dura como máximo 10 min.


class Rechazo(Exception):
    """El conjunto de datos o las métricas no permiten publicar (RF22 exc. 1–3)."""


def validar_hiperparametros(data) -> dict:
    hiper = {}
    for nombre, propuesto in PROPUESTOS.items():
        valor = data.get(nombre, propuesto)
        minimo, maximo = LIMITES[nombre]
        try:
            valor = int(valor)
        except (TypeError, ValueError) as err:
            raise ValidationError({nombre: "Debe ser un número entero."}) from err
        if not minimo <= valor <= maximo:
            raise ValidationError({nombre: f"Debe estar entre {minimo} y {maximo}."})
        hiper[nombre] = valor
    return hiper


def iniciar(usuario=None, hiperparametros=None) -> ModeloEntrenado | None:
    """Registra una versión EN_CURSO, o None si ya hay un entrenamiento activo."""
    with transaction.atomic():
        bloquear_proceso(2)
        activos = ModeloEntrenado.objects.select_for_update().filter(estado=E.EN_CURSO)
        activos.filter(inicio__lt=timezone.now() - VENCIMIENTO_EN_CURSO).update(
            estado=E.FALLIDO, fin=timezone.now(), mensaje="Entrenamiento abandonado (tiempo de espera agotado)."
        )
        if activos.filter(estado=E.EN_CURSO).exists():
            return None
        version = (ModeloEntrenado.objects.aggregate(v=Max("version"))["v"] or 0) + 1
        return ModeloEntrenado.objects.create(
            version=version, entrenado_por=usuario, hiperparametros=hiperparametros or dict(PROPUESTOS)
        )


def _evaluar(modelo: ModeloEntrenado, parametros: ParametrosSistema):
    """Pasos 1 a 4 de RF22. Devuelve el pipeline reentrenado con todo el histórico."""
    df = datos.serie_diaria()
    modelo.registros = int(df["registros"].sum()) if not df.empty else 0
    if modelo.registros < parametros.min_registros_entrenamiento:
        raise Rechazo(
            f"Hay {modelo.registros} registros depurados y se necesitan al menos "
            f"{parametros.min_registros_entrenamiento} para entrenar."
        )
    df = datos.con_temporales(datos.con_historicas(df)).dropna(subset=["promedio_28d"])
    if df["kg"].nunique() <= 1:
        raise Rechazo("La cantidad generada es constante en todo el histórico; no hay nada que aprender.")
    modelo.variables = [v for v in datos.VARIABLES if df[v].notna().any() and df[v].nunique() > 1]
    if not modelo.variables:
        raise Rechazo("Todas las variables predictoras son constantes o están vacías.")

    # Partición cronológica (RF22 paso 2): las fechas más recientes quedan para la prueba.
    fechas = np.sort(df["fecha"].unique())
    corte = fechas[int(len(fechas) * (1 - PROPORCION_PRUEBA))]
    entrenamiento, prueba = df[df["fecha"] < corte], df[df["fecha"] >= corte]
    if entrenamiento.empty or prueba.empty:
        raise Rechazo("El histórico no abarca suficientes fechas para separar entrenamiento y prueba.")
    modelo.corte = corte.astype("datetime64[D]").item()
    modelo.observaciones_entrenamiento, modelo.observaciones_prueba = len(entrenamiento), len(prueba)

    X = modelo.variables
    pipe = datos.pipeline(X, modelo.hiperparametros)
    pipe.fit(entrenamiento[X], entrenamiento["kg"])
    estimado = pipe.predict(prueba[X])
    modelo.mae = float(mean_absolute_error(prueba["kg"], estimado))
    modelo.mse = float(mean_squared_error(prueba["kg"], estimado))
    modelo.rmse = float(np.sqrt(modelo.mse))
    modelo.r2 = float(r2_score(prueba["kg"], estimado))
    nombres = pipe.named_steps["codificacion"].get_feature_names_out()
    importancias = pipe.named_steps["bosque"].feature_importances_
    modelo.importancias = {
        str(n): round(float(i), 4) for n, i in sorted(zip(nombres, importancias, strict=True), key=lambda x: -x[1])
    }
    # Con la evaluación hecha, el modelo publicable aprende también de las fechas más recientes.
    pipe.fit(df[X], df["kg"])
    return pipe


def entrenar(modelo: ModeloEntrenado) -> ModeloEntrenado:
    """Corre RF22 completo y deja constancia de parámetros, métricas y resultado (paso 5.3, RNF25)."""
    parametros = ParametrosSistema.actual()
    modelo.umbral_r2 = parametros.umbral_r2_modelo
    try:
        pipe = _evaluar(modelo, parametros)
        if modelo.r2 < float(parametros.umbral_r2_modelo):
            raise Rechazo(
                f"R² = {_es(modelo.r2, 3)} no alcanza el umbral de {_es(float(parametros.umbral_r2_modelo), 2)}; "
                "se conserva la versión vigente."
            )
        buffer = BytesIO()
        joblib.dump(pipe, buffer, compress=3)
        modelo.artefacto = buffer.getvalue()
        _guardar_en_disco(modelo.pk, modelo.artefacto)
        modelo.estado = E.APROBADO
        modelo.mensaje = f"R² = {_es(modelo.r2, 3)}, RMSE = {_es(modelo.rmse, 2)} kg. Versión publicada."
    except Rechazo as motivo:
        modelo.estado, modelo.mensaje = E.RECHAZADO, str(motivo)
    except Exception as exc:  # noqa: BLE001 — cualquier fallo queda registrado con la versión.
        log.exception("Fallo del entrenamiento")
        modelo.estado, modelo.mensaje = E.FALLIDO, f"Error durante el entrenamiento: {exc}"
    modelo.fin = timezone.now()
    with transaction.atomic():
        if modelo.estado == E.APROBADO:
            ModeloEntrenado.objects.filter(vigente=True).update(vigente=False)
            modelo.vigente = True
        modelo.save()
    registrar(
        None,
        AuditLog.Operacion.PROCESO,
        modelo,
        usuario=modelo.entrenado_por,
        detalle=f"Entrenamiento v{modelo.version} {modelo.get_estado_display()}: {modelo.mensaje}",
    )
    return modelo


def entrenar_en_segundo_plano(modelo: ModeloEntrenado) -> None:
    """No bloquea la petición ni la captura en campo (RD10, RNF5).

    ponytail: hilo dentro del proceso web, igual que el ETL; pasar a una cola de tareas
    (Celery/RQ) si el entrenamiento llega a competir por CPU con la operación.
    """

    def correr():
        close_old_connections()
        try:
            entrenar(modelo)
        finally:
            connection.close()

    threading.Thread(target=correr, name=f"entrenamiento-{modelo.pk}", daemon=True).start()


def publicar(request, modelo: ModeloEntrenado) -> ModeloEntrenado:
    """Vuelve vigente una versión aprobada; permite revertir a una anterior (RD13)."""
    if modelo.estado != E.APROBADO:
        raise ValidationError("Solo puede publicarse una versión aprobada.")
    if modelo.vigente:
        raise ValidationError("Esta versión ya es la vigente.")
    with transaction.atomic():
        anterior = ModeloEntrenado.objects.select_for_update().filter(vigente=True).first()
        ModeloEntrenado.objects.filter(vigente=True).update(vigente=False)
        modelo.vigente = True
        modelo.save(update_fields=["vigente"])
    registrar(
        request,
        AuditLog.Operacion.TRANSICION,
        modelo,
        antes={"vigente": anterior.version if anterior else None},
        despues={"vigente": modelo.version},
        detalle=f"Publicación de la versión {modelo.version}",
    )
    return modelo


def vigente() -> ModeloEntrenado:
    modelo = ModeloEntrenado.objects.filter(vigente=True).first()
    if modelo is None:
        raise ValidationError("No existe un modelo publicado vigente: entrene y publique uno primero.")
    return modelo


def _archivo(pk: int) -> Path:
    return Path(settings.MODELOS_DIR) / f"modelo-{pk}.joblib"


def _guardar_en_disco(pk: int, contenido: bytes) -> None:
    archivo = _archivo(pk)
    archivo.parent.mkdir(parents=True, exist_ok=True)
    temporal = archivo.with_suffix(".tmp")
    temporal.write_bytes(contenido)
    temporal.replace(archivo)  # nunca queda un archivo a medio escribir


@lru_cache(maxsize=2)
def cargar(pk: int):
    """Pipeline de una versión. La BD es la fuente; la copia en disco evita volver a descargarlo (RTR11).

    Una versión nunca cambia, así que se cachea por clave en disco y en memoria.
    """
    if not _archivo(pk).exists():
        _guardar_en_disco(pk, bytes(ModeloEntrenado.objects.values_list("artefacto", flat=True).get(pk=pk)))
    return joblib.load(_archivo(pk))
