#!/bin/bash
set -x

echo "=== Переменные окружения ==="
printenv
echo "==========================="

echo "Ожидание базы данных..."
if ! ./wait-for-db.sh; then
    echo "ОШИБКА: База данных не доступна!"
    exit 1
fi

echo "=== Применение миграций ==="
python manage.py migrate --no-input

echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

echo "Проверка Django..."
python manage.py check

echo "=== Запуск Gunicorn ==="
gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug

sleep infinity  # Для диагностики (удалите после теста)