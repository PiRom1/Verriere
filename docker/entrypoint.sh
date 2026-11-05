#!/bin/sh
# Démarrage : migrations, fichiers statiques, puis le serveur.
# 1 worker (il possède les GPIO), 4 threads (l'interface répond pendant un relevé).
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
exec gunicorn Verriere.wsgi:application --bind 0.0.0.0:8000 \
     --worker-class gthread --workers 1 --threads 4 --timeout 120 \
     --access-logfile - --error-logfile -
