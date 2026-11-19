"""Conjunto de datos del modelo (RF22 paso 1): serie diaria por punto y tipo, y sus variables predictoras.

Observación = kg recolectados en un punto, de un tipo de residuo, en un día. Se usa el mismo cálculo
para entrenar y para predecir, de modo que las variables signifiquen lo mismo en ambos momentos.
"""

from datetime import date, timedelta

import pandas as pd
from django.db.models import Count, Sum
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from apps.analytics.models import HechoResiduo
from apps.catalogs.models import PeriodoAcademico

CATEGORICAS = ["sector_id", "punto_id", "tipo_residuo_id"]
# Historia reciente del punto y tipo: promedio de los 28 días previos (cantidad histórica) y
# visitas con registro por semana en ese lapso (frecuencia de recolección).
HISTORICAS = ["promedio_28d", "frecuencia_semanal"]
TEMPORALES = ["dia_semana", "dia_mes", "mes", "semana_anio", "en_periodo"]
VARIABLES = CATEGORICAS + HISTORICAS + TEMPORALES
VENTANA_DIAS = 28


def serie_diaria(desde: date | None = None, puntos=None) -> pd.DataFrame:
    """Kg por punto, tipo y fecha desde el plano analítico; excluye volumen y atípicos marcados por el ETL."""
    qs = HechoResiduo.objects.filter(magnitud=HechoResiduo.Magnitud.PESO, atipico=False)
    if desde:
        qs = qs.filter(fecha__gte=desde)
    if puntos is not None:
        qs = qs.filter(punto_id__in=puntos)
    filas = qs.values("sector_id", "punto_id", "tipo_residuo_id", "fecha").annotate(
        kg=Sum("cantidad_base"), registros=Count("id")
    )
    df = pd.DataFrame.from_records(filas, columns=[*CATEGORICAS, "fecha", "kg", "registros"])
    return df.astype({"kg": float}).assign(fecha=pd.to_datetime(df["fecha"]))


def con_temporales(df: pd.DataFrame) -> pd.DataFrame:
    f = df["fecha"].dt
    en_periodo = pd.Series(0, index=df.index)
    for inicio, fin in PeriodoAcademico.objects.values_list("fecha_inicio", "fecha_fin"):
        en_periodo[(df["fecha"] >= pd.Timestamp(inicio)) & (df["fecha"] <= pd.Timestamp(fin))] = 1
    return df.assign(
        dia_semana=f.dayofweek,
        dia_mes=f.day,
        mes=f.month,
        semana_anio=f.isocalendar().week.astype(int),
        en_periodo=en_periodo,
    )


def con_historicas(df: pd.DataFrame) -> pd.DataFrame:
    """Ventana de los 28 días anteriores a cada observación, sin incluirla (evita fuga del objetivo)."""
    df = df.sort_values(["punto_id", "tipo_residuo_id", "fecha"]).reset_index(drop=True)
    ventana = df.groupby(["punto_id", "tipo_residuo_id"]).rolling(f"{VENTANA_DIAS}D", on="fecha", closed="left")["kg"]
    # El resultado sale en el mismo orden que df (ordenado por las claves del grupo y la fecha).
    df["promedio_28d"] = ventana.mean().to_numpy()
    df["frecuencia_semanal"] = ventana.count().fillna(0).to_numpy() * 7 / VENTANA_DIAS
    return df


def estado_actual(hoy: date, puntos) -> pd.DataFrame:
    """Historia reciente de cada punto y tipo al día de hoy: base para construir las fechas futuras (RF23 2.1)."""
    df = serie_diaria(hoy - timedelta(days=VENTANA_DIAS - 1), puntos)
    if df.empty:
        return pd.DataFrame(columns=[*CATEGORICAS, *HISTORICAS])
    return (
        df.groupby(CATEGORICAS)["kg"]
        .agg(promedio_28d="mean", visitas="count")
        .reset_index()
        .assign(frecuencia_semanal=lambda d: d["visitas"] * 7 / VENTANA_DIAS)
        .drop(columns="visitas")
    )


def dias_habituales(hoy: date, puntos) -> dict[int, set[int]]:
    """Días de la semana en que cada punto suele tener registros (últimas 8 semanas)."""
    df = serie_diaria(hoy - timedelta(days=56), puntos)
    return {int(p): set(g["fecha"].dt.dayofweek) for p, g in df.groupby("punto_id")}


def pipeline(variables: list[str], hiperparametros: dict) -> Pipeline:
    """Codificación ordinal de las categóricas (RF22 1.4) y Random Forest Regressor (RD5)."""
    categoricas = [c for c in CATEGORICAS if c in variables]
    return Pipeline(
        [
            (
                "codificacion",
                ColumnTransformer(
                    [
                        (
                            "categoricas",
                            OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                            categoricas,
                        )
                    ],
                    remainder="passthrough",
                    verbose_feature_names_out=False,
                ),
            ),
            ("bosque", RandomForestRegressor(**hiperparametros, random_state=42, n_jobs=2)),
        ]
    )
