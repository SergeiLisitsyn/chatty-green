#!/bin/bash
set -x

echo "=== Проверка окружения ==="
python -c "import os; print('DATABASE_URL:', os.getenv('DATABASE_URL'))"

echo "=== Ожидание БД ==="
if ! ./wait-for-db.sh; then
    echo "❌ Ошибка: БД не доступна!" >&2
    exit 1
fi

echo "=== Применение миграций ==="
python manage.py migrate --no-input

# Создание суперпользователя
python create_admin.py

echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

echo "=== Запуск Gunicorn ==="
exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -