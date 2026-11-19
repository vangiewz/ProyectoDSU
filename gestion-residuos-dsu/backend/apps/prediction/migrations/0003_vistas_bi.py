from django.db import migrations

# RNF26 / RI14 / RD8: predicciones vigentes y recomendaciones para los tableros de Power BI, sin datos personales.
SQL = """
CREATE OR REPLACE VIEW bi_predicciones AS
WITH ultimo AS (
    SELECT punto_id, MAX(lote_id) AS lote_id FROM prediction_prediccion GROUP BY punto_id
)
SELECT pr.id, pr.fecha, s.codigo AS sector_codigo, s.nombre AS sector,
       p.codigo AS punto_codigo, p.nombre AS punto, t.nombre AS tipo_residuo, t.clasificacion,
       pr.cantidad_kg, pr.margen_kg, m.version AS modelo_version, l.creado_en AS generada_en
FROM prediction_prediccion pr
JOIN ultimo u ON u.punto_id = pr.punto_id AND u.lote_id = pr.lote_id
JOIN prediction_loteprediccion l ON l.id = pr.lote_id
JOIN prediction_modeloentrenado m ON m.id = l.modelo_id
JOIN campus_sector s ON s.id = pr.sector_id
JOIN campus_puntorecoleccion p ON p.id = pr.punto_id
JOIN catalogs_tiporesiduo t ON t.id = pr.tipo_residuo_id
WHERE pr.fecha >= CURRENT_DATE;

CREATE OR REPLACE VIEW bi_recomendaciones AS
SELECT r.id, r.creada_en, s.codigo AS sector_codigo, s.nombre AS sector, p.codigo AS punto_codigo,
       r.tipo, r.urgencia, r.estado, r.resuelta_en
FROM prediction_recomendacion r
JOIN campus_sector s ON s.id = r.sector_id
JOIN campus_puntorecoleccion p ON p.id = r.punto_id;
"""

REVERSE = "DROP VIEW IF EXISTS bi_recomendaciones, bi_predicciones;"


class Migration(migrations.Migration):
    dependencies = [("prediction", "0002_permisos_roles"), ("campus", "0001_initial"), ("catalogs", "0003_parametrossistema_alerta_capacidad_pct_and_more")]
    operations = [migrations.RunSQL(SQL, REVERSE)]
