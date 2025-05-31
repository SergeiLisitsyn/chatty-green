#!/bin/bash
set -x

echo "=== Переменные окружения ==="
printenv
echo "==========================="

echo "Ожидание базы данных..."
./wait-for-db.sh

echo "=== Применение миграций ==="
python manage.py migrate --no-input

echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

echo "Проверка Django..."
python manage.py check

echo "=== Запуск Gunicorn ==="
exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug