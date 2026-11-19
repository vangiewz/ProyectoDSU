#!/bin/sh
# RNF12: respaldo automático diario de la base, fuera de Neon (en el disco del servidor).
# Lo ejecuta el servicio "respaldo" de docker-compose.yml. Conserva los últimos $RESPALDO_DIAS días.
# Restaurar:  pg_restore --clean --if-exists --no-owner -d "<url-destino>" respaldos/dsu-AAAAMMDD-HHMM.dump
set -u
URL="${RESPALDO_DATABASE_URL:-$DATABASE_URL}"   # conviene la conexión directa de Neon (sin -pooler)
DIAS="${RESPALDO_DIAS:-14}"

while true; do
  archivo="/respaldos/dsu-$(date +%Y%m%d-%H%M).dump"
  if pg_dump "$URL" --format=custom --no-owner --file="$archivo.tmp"; then
    mv "$archivo.tmp" "$archivo"
    echo "$(date -Iseconds) respaldo listo: $archivo"
  else
    rm -f "$archivo.tmp"
    echo "$(date -Iseconds) ERROR: falló el respaldo" >&2
  fi
  find /respaldos -name 'dsu-*.dump' -mtime +"$DIAS" -delete
  sleep 86400
done
