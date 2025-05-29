#!/bin/sh
# Отладочный вывод
echo "=== Переменные окружения ==="
printenv
echo "==========================="

# Ожидание базы данных
./wait-for-db.sh
set -x  # Включить подробное логирование

echo "=== Применение миграций ==="
python manage.py migrate --no-input

echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

echo "=== Запуск Gunicorn ==="
gunicorn your_project.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug
# Проверка работы порта
echo "Проверка порта 10000..."
timeout 10 sh -c 'until nc -z $0 $1; do sleep 1; done' 0.0.0.0 10000 || {
    echo "ПОРТ 10000 НЕ ОТКРЫТ!"
    exit 1
}

echo "✅ Порт 10000 успешно открыт"
wait

# Миграции (только для web-сервиса)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    python manage.py migrate --no-input
fi

# Выполнение переданной команды
exec "$@"