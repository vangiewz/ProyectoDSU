from django.db import migrations

# RNF26 / RI14: estructuras analíticas depuradas para Microsoft Power BI, sin datos personales.
SQL = """
CREATE OR REPLACE VIEW bi_hechos_residuos AS
SELECT h.id, h.fecha, h.fecha_hora, h.anio, h.mes, h.semana_anio, h.dia_semana,
       s.codigo AS sector_codigo, s.nombre AS sector,
       p.codigo AS punto_codigo, p.nombre AS punto, p.latitud, p.longitud,
       t.nombre AS tipo_residuo, t.clasificacion, t.aprovechable,
       h.magnitud, h.cantidad_base, h.cantidad_original, u.simbolo AS unidad_original,
       pa.nombre AS periodo_academico, h.atipico, h.jornada_id
FROM analytics_hechoresiduo h
JOIN campus_sector s ON s.id = h.sector_id
JOIN campus_puntorecoleccion p ON p.id = h.punto_id
JOIN catalogs_tiporesiduo t ON t.id = h.tipo_residuo_id
JOIN catalogs_unidadmedida u ON u.id = h.unidad_id
LEFT JOIN catalogs_periodoacademico pa ON pa.id = h.periodo_id;

CREATE OR REPLACE VIEW bi_jornadas AS
SELECT j.id, j.fecha, j.turno, j.estado, s.codigo AS sector_codigo, s.nombre AS sector,
       COUNT(jp.id) AS puntos_planificados,
       COUNT(jp.id) FILTER (WHERE jp.atendido) AS puntos_atendidos,
       COUNT(jp.id) FILTER (WHERE jp.atendido = false) AS puntos_omitidos,
       j.hora_inicio, j.hora_fin
FROM operations_jornada j
JOIN campus_sector s ON s.id = j.sector_id
LEFT JOIN operations_jornadapunto jp ON jp.jornada_id = j.id
GROUP BY j.id, s.codigo, s.nombre;

CREATE OR REPLACE VIEW bi_incidencias AS
SELECT i.id, i.fecha_hora, i.tipo, i.gravedad, i.estado, p.codigo AS punto_codigo,
       s.nombre AS sector, i.atendida_en
FROM operations_incidencia i
JOIN campus_puntorecoleccion p ON p.id = i.punto_id
JOIN campus_sector s ON s.id = p.sector_id;

CREATE OR REPLACE VIEW bi_puntos AS
SELECT p.id, p.codigo, p.nombre, s.codigo AS sector_codigo, s.nombre AS sector,
       p.latitud, p.longitud, p.capacidad_kg, p.estado, p.is_active
FROM campus_puntorecoleccion p
JOIN campus_sector s ON s.id = p.sector_id;
"""

REVERSE = "DROP VIEW IF EXISTS bi_puntos, bi_incidencias, bi_jornadas, bi_hechos_residuos;"


class Migration(migrations.Migration):
    dependencies = [("analytics", "0002_permisos_roles"), ("operations", "0001_initial"), ("catalogs", "0002_parametrossistema")]
    operations = [migrations.RunSQL(SQL, REVERSE)]
