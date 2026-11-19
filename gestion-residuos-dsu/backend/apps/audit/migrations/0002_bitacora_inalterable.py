from django.db import migrations

# RBD21: la bitácora no puede modificarse ni eliminarse, ni siquiera por SQL directo.
SQL = """
CREATE OR REPLACE FUNCTION audit_auditlog_inalterable() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'La bitacora de auditoria es inalterable (operacion % rechazada)', TG_OP;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_auditlog_inalterable
BEFORE UPDATE OR DELETE ON audit_auditlog
FOR EACH ROW EXECUTE FUNCTION audit_auditlog_inalterable();

CREATE TRIGGER audit_auditlog_sin_truncate
BEFORE TRUNCATE ON audit_auditlog
FOR EACH STATEMENT EXECUTE FUNCTION audit_auditlog_inalterable();
"""

REVERSE = """
DROP TRIGGER IF EXISTS audit_auditlog_sin_truncate ON audit_auditlog;
DROP TRIGGER IF EXISTS audit_auditlog_inalterable ON audit_auditlog;
DROP FUNCTION IF EXISTS audit_auditlog_inalterable();
"""


class Migration(migrations.Migration):
    dependencies = [("audit", "0001_initial")]
    operations = [migrations.RunSQL(SQL, REVERSE)]
