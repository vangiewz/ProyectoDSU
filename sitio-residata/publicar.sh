#!/bin/sh
# Para ejecución manual del titular: publica solo recursos públicos en un proyecto previamente vinculado.
set -e
cd "$(dirname "$0")"
python preparar_publicacion.py
if [ ! -f dist/.vercel/project.json ]; then
  echo 'Primero inicie sesión en la cuenta propietaria y ejecute: vercel link --cwd sitio-residata/dist'
  echo 'Seleccione el proyecto EXISTENTE residata. No cree otro proyecto ni cambie alias sin revisión.'
  exit 1
fi
cd dist
npx vercel deploy --prod
echo 'Verifique la URL de producción y todas las rutas. Este script no cambia alias ni DNS.'
