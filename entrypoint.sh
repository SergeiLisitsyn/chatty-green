#!/bin/sh
# Ожидание базы данных
./wait-for-db.sh

# Миграции (только для web-сервиса)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    python manage.py migrate --no-input
fi

# Выполнение переданной команды
exec "$@"