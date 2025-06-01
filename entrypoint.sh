#!/bin/bash
set -x

echo "=== Переменные окружения ==="
printenv
echo "==========================="

# Ожидание БД с обработкой ошибок
echo "Ожидание базы данных..."
if ! ./wait-for-db.sh; then
    echo "ОШИБКА: Не удалось подключиться к БД!"
    exit 1
fi

# Миграции
echo "=== Применение миграций ==="
python manage.py migrate --no-input || exit 1

# Статика
echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear || echo "Предупреждение: collectstatic завершился с ошибкой"

# Проверка Django
echo "Проверка Django..."
python manage.py check || exit 1

# Запуск Gunicorn (используем PORT от Render)
echo "=== Запуск Gunicorn ==="
exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug