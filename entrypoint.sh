#!/bin/sh
# Отладочный вывод
echo "=== Переменные окружения ==="
printenv
echo "==========================="

# Ожидание базы данных
./wait-for-db.sh
#gunicorn chatty.wsgi:application --bind 0.0.0.0:${PORT:-10000}
# Миграции (только для web-сервиса)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    python manage.py migrate --no-input
fi

# Выполнение переданной команды
exec "$@"