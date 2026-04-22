#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos para WhiteNoise
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate