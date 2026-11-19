#!/bin/sh
# Ensambla el sitio, lo publica en Vercel y apunta residata-bolivia.vercel.app a la nueva versión.
set -e
cd "$(dirname "$0")"
python construir.py >/dev/null
url=$(npx vercel deploy --prod --yes 2>/dev/null | grep -o 'https://residata-[a-z0-9]*-vangiews-projects.vercel.app' | head -1)
npx vercel alias set "$url" residata-bolivia.vercel.app >/dev/null
echo "Publicado: https://residata-bolivia.vercel.app ($url)"
