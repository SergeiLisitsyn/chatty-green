#!/bin/bash
set -x

echo "=== Старт entrypoint ==="
python manage.py check || exit 1

# Замените 10000 на $PORT для Render
exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 2 \
    --access-logfile - \
    --error-logfile -