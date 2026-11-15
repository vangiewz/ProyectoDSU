"""Proceso de extracción, transformación y carga (RF15) con Pandas y NumPy (RD6).

Incremental: procesa los registros de residuos que aún no tienen hecho analítico. Nunca modifica
el plano transaccional; los duplicados se excluyen del analítico y los atípicos se cargan marcados.
"""

import logging
import threading
from datetime import timedelta
from decimal import Decimal

import numpy as np
import pandas as pd
from django.db import close_old_connections, connection, transaction
from django.utils import timezone

from apps.audit.models import AuditLog
from apps.audit.services import registrar
from apps.catalogs.models import ParametrosSistema, PeriodoAcademico
from apps.operations.models import RegistroResiduo

from ..models import EjecucionETL, HechoResiduo, RegistroDescartado

log = logging.getLogger(__name__)
E = EjecucionETL.Estado

# Un registro es atípico si supera Q3 + 1,5·IQR de su punto y tipo, con al menos esta cantidad de muestras.
MIN_MUESTRAS_ATIPICO = 8
# Una ejecución "en curso" más vieja que esto se considera abandonada (caída del proceso).
VENCIMIENTO_EN_CURSO = timedelta(minutes=30)


def extraer() -> pd.DataFrame:
    """Registros transaccionales sin hecho analítico, con los datos de sus dimensiones."""
    filas = RegistroResiduo.objects.filter(hecho__isnull=True, descarte__isnull=True).values(
        "id",
        "fecha_hora",
        "punto_id",
        "punto__sector_id",
        "tipo_residuo_id",
        "jornada_id",
        "unidad_id",
        "unidad__magnitud",
        "unidad__factor_conversion",
        "cantidad",
        "registrado_por_id",
    )
    return pd.DataFrame.from_records(filas)


def marcar_duplicados(df: pd.DataFrame) -> pd.Series:
    """Mismo operario, punto, tipo, unidad y cantidad dentro del mismo minuto: doble envío.

    ponytail: solo compara dentro de la tanda; un reenvío que cae en la tanda siguiente no se detecta.
    """
    clave = df.assign(minuto=df["fecha_hora"].dt.floor("min"))
    return clave.duplicated(
        subset=["registrado_por_id", "punto_id", "tipo_residuo_id", "unidad_id", "cantidad", "minuto"], keep="first"
    )


def asignar_periodo(fechas: pd.Series, periodos: list[tuple[int, object, object]]) -> pd.Series:
    resultado = pd.Series([None] * len(fechas), index=fechas.index, dtype=object)
    for pk, inicio, fin in periodos:
        resultado[(fechas >= inicio) & (fechas <= fin)] = pk
    return resultado


def marcar_atipicos(df: pd.DataFrame, historico: pd.DataFrame) -> pd.Series:
    """IQR por punto, tipo y magnitud sobre el histórico ya cargado más los registros nuevos."""
    base = pd.concat([historico, df[["punto_id", "tipo_residuo_id", "magnitud", "cantidad_base"]]], ignore_index=True)
    grupos = base.groupby(["punto_id", "tipo_residuo_id", "magnitud"])["cantidad_base"]
    limites = (grupos.quantile(0.75) + 1.5 * (grupos.quantile(0.75) - grupos.quantile(0.25))).rename("limite")
    conteo = grupos.size().rename("n")
    unido = df.join(limites, on=["punto_id", "tipo_residuo_id", "magnitud"]).join(
        conteo, on=["punto_id", "tipo_residuo_id", "magnitud"]
    )
    return (unido["n"] >= MIN_MUESTRAS_ATIPICO) & (unido["cantidad_base"] > unido["limite"])


def transformar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["punto_id", "tipo_residuo_id", "unidad_id", "cantidad", "unidad__factor_conversion"]).copy()
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], utc=True).dt.tz_convert(str(timezone.get_current_timezone()))
    df["duplicado"] = marcar_duplicados(df)
    # Estandarización a la base de la magnitud (kg o L) con el factor registrado (RBD9).
    df["magnitud"] = df["unidad__magnitud"]
    df["cantidad_base"] = (df["cantidad"].astype(float) * df["unidad__factor_conversion"].astype(float)).round(3)
    # Variables temporales (RBD11).
    df["fecha"] = df["fecha_hora"].dt.date
    df["dia_semana"] = df["fecha_hora"].dt.dayofweek
    df["mes"] = df["fecha_hora"].dt.month
    df["semana_anio"] = df["fecha_hora"].dt.isocalendar().week.astype(int)
    df["anio"] = df["fecha_hora"].dt.year
    periodos = list(PeriodoAcademico.objects.values_list("pk", "fecha_inicio", "fecha_fin"))
    df["periodo_id"] = asignar_periodo(df["fecha"], periodos)
    historico = pd.DataFrame.from_records(
        HechoResiduo.objects.values("punto_id", "tipo_residuo_id", "magnitud", "cantidad_base"),
        columns=["punto_id", "tipo_residuo_id", "magnitud", "cantidad_base"],
    ).astype({"cantidad_base": float})
    validos = ~df["duplicado"]
    df["atipico"] = False
    df.loc[validos, "atipico"] = marcar_atipicos(df[validos], historico)
    return df


def cargar(df: pd.DataFrame, ejecucion: EjecucionETL) -> int:
    nuevos = [
        HechoResiduo(
            registro_id=int(r.id),
            fecha_hora=r.fecha_hora.to_pydatetime(),
            fecha=r.fecha,
            punto_id=int(r.punto_id),
            sector_id=int(r.punto__sector_id),
            tipo_residuo_id=int(r.tipo_residuo_id),
            jornada_id=int(r.jornada_id),
            unidad_id=int(r.unidad_id),
            cantidad_original=r.cantidad,
            magnitud=r.magnitud,
            cantidad_base=Decimal(str(r.cantidad_base)),
            dia_semana=int(r.dia_semana),
            mes=int(r.mes),
            semana_anio=int(r.semana_anio),
            anio=int(r.anio),
            periodo_id=None
            if r.periodo_id is None or (isinstance(r.periodo_id, float) and np.isnan(r.periodo_id))
            else int(r.periodo_id),
            atipico=bool(r.atipico),
            ejecucion=ejecucion,
        )
        for r in df[~df["duplicado"]].itertuples()
    ]
    HechoResiduo.objects.bulk_create(nuevos, batch_size=1000)
    RegistroDescartado.objects.bulk_create(
        RegistroDescartado(registro_id=int(i), motivo=RegistroDescartado.Motivo.DUPLICADO, ejecucion=ejecucion)
        for i in df.loc[df["duplicado"], "id"]
    )
    return len(nuevos)


def iniciar(usuario=None) -> EjecucionETL | None:
    """Registra una ejecución EN_CURSO, o None si ya hay otra activa (evita ejecuciones simultáneas)."""
    with transaction.atomic():
        activas = EjecucionETL.objects.select_for_update().filter(estado=E.EN_CURSO)
        activas.filter(inicio__lt=timezone.now() - VENCIMIENTO_EN_CURSO).update(
            estado=E.FALLIDA, fin=timezone.now(), mensaje="Ejecución abandonada (tiempo de espera agotado)."
        )
        if activas.filter(estado=E.EN_CURSO).exists():
            return None
        return EjecucionETL.objects.create(disparada_por=usuario)


def ejecutar(ejecucion: EjecucionETL) -> EjecucionETL:
    """Corre el ETL completo y deja el resultado en la bitácora del proceso (RF15 paso 4)."""
    try:
        df = extraer()
        if df.empty:
            ejecucion.estado, ejecucion.mensaje = E.SIN_CAMBIOS, "No hay registros nuevos desde la última ejecución."
        else:
            df = transformar(df)
            with transaction.atomic():
                cargados = cargar(df, ejecucion)
            ejecucion.procesados = len(df)
            ejecucion.duplicados = int(df["duplicado"].sum())
            ejecucion.atipicos = int(df["atipico"].sum())
            ejecucion.observados = ejecucion.duplicados + ejecucion.atipicos
            ejecucion.aceptados = cargados - ejecucion.atipicos
            umbral = float(ParametrosSistema.actual().etl_umbral_observados_pct)
            pct = ejecucion.observados * 100 / ejecucion.procesados
            if pct > umbral:
                ejecucion.estado = E.CON_ALERTA
                ejecucion.mensaje = (
                    f"{pct:.1f}% de registros observados supera el umbral de {umbral:.1f}%. Revise los atípicos."
                )
            else:
                ejecucion.estado, ejecucion.mensaje = E.EXITOSA, f"{cargados} registro(s) cargados al plano analítico."
    except Exception as exc:  # noqa: BLE001 — cualquier fallo queda registrado en la bitácora del proceso.
        log.exception("Fallo del ETL")
        ejecucion.estado, ejecucion.mensaje = E.FALLIDA, f"Error durante la ejecución: {exc}"
    ejecucion.fin = timezone.now()
    ejecucion.save()
    registrar(
        None,
        AuditLog.Operacion.PROCESO,
        ejecucion,
        usuario=ejecucion.disparada_por,
        detalle=f"ETL {ejecucion.get_estado_display()}: {ejecucion.procesados} procesados, "
        f"{ejecucion.observados} observados",
    )
    return ejecucion


def ejecutar_en_segundo_plano(ejecucion: EjecucionETL) -> None:
    """Bajo demanda sin bloquear la petición ni la captura en campo (RD10, RNF5).

    ponytail: hilo dentro del proceso web; pasar a una cola (Celery/Redis) al llegar el entrenamiento
    del modelo.
    """

    def correr():
        close_old_connections()
        try:
            ejecutar(ejecucion)
        finally:
            connection.close()

    threading.Thread(target=correr, name=f"etl-{ejecucion.pk}", daemon=True).start()
