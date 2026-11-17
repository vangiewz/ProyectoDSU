# Medidas existentes: revisar y conservar salvo corrección justificada

## bi_hechos_residuos — Total kg

```dax
CALCULATE(SUM(bi_hechos_residuos[cantidad_base]), bi_hechos_residuos[magnitud] = "PESO")
```

## bi_hechos_residuos — Total L

```dax
CALCULATE(SUM(bi_hechos_residuos[cantidad_base]), bi_hechos_residuos[magnitud] = "VOLUMEN")
```

## bi_hechos_residuos — Registros

```dax
COUNTROWS(bi_hechos_residuos)
```

## bi_hechos_residuos — Puntos con datos

```dax
DISTINCTCOUNT(bi_hechos_residuos[punto_codigo])
```

## bi_hechos_residuos — Promedio kg por punto

```dax
DIVIDE([Total kg], [Puntos con datos])
```

## bi_hechos_residuos — Total kg año anterior

```dax
CALCULATE([Total kg], SAMEPERIODLASTYEAR(Calendario[Fecha]))
```

## bi_hechos_residuos — Variación vs año anterior

```dax
DIVIDE([Total kg] - [Total kg año anterior], [Total kg año anterior])
```

## bi_hechos_residuos — Participación aprovechable

```dax
DIVIDE(CALCULATE([Total kg], bi_hechos_residuos[aprovechable] = TRUE()), [Total kg])
```

## bi_jornadas — Jornadas cerradas

```dax
CALCULATE(COUNTROWS(bi_jornadas), bi_jornadas[estado] = "CERRADA")
```

## bi_jornadas — Cobertura

```dax
DIVIDE(SUM(bi_jornadas[puntos_atendidos]), SUM(bi_jornadas[puntos_planificados]))
```

## bi_incidencias — Incidencias

```dax
COUNTROWS(bi_incidencias)
```

## bi_incidencias — Incidencias pendientes

```dax
CALCULATE(COUNTROWS(bi_incidencias), bi_incidencias[estado] = "PENDIENTE")
```

## bi_predicciones — Generación proyectada kg

```dax
SUM(bi_predicciones[cantidad_kg])
```

## bi_predicciones — Margen proyectado kg

```dax
SQRT(SUMX(bi_predicciones, bi_predicciones[margen_kg] ^ 2))
```

## bi_recomendaciones — Recomendaciones pendientes

```dax
CALCULATE(COUNTROWS(bi_recomendaciones), bi_recomendaciones[estado] = "PENDIENTE")
```

## bi_recomendaciones — Recomendaciones aceptadas

```dax
CALCULATE(COUNTROWS(bi_recomendaciones), bi_recomendaciones[estado] = "ACEPTADA")
```
