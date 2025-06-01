#!/bin/sh
set -x

echo "=== Тест Gunicorn ==="
exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 1 \
    --access-logfile - \
    --error-logfile -