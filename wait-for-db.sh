#!/bin/sh
set -e

# Определяем параметры подключения в зависимости от среды
if [ -n "$DATABASE_URL" ]; then
    # Режим Render.com - извлекаем параметры из DATABASE_URL
    DB_HOST=$(echo "$DATABASE_URL" | sed -e 's/.*@\([^:]*\):.*/\1/')
    DB_PORT=$(echo "$DATABASE_URL" | sed -e 's/.*:\([0-9]*\)\/.*/\1/')
    echo "Render.com режим: DB_HOST=$DB_HOST, DB_PORT=$DB_PORT"
else
    # Режим Docker Compose - используем переменные из .env
    DB_HOST="${PG_HOST:-db}"
    DB_PORT="${PG_PORT:-5432}"
    echo "Docker Compose режим: DB_HOST=$DB_HOST, DB_PORT=$DB_PORT"
fi

# Проверка значений
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
    echo "⛔ Ошибка: Не удалось определить параметры подключения к БД"
    echo "DATABASE_URL=$DATABASE_URL"
    echo "PG_HOST=$PG_HOST, PG_PORT=$PG_PORT"
    exit 1
fi

TIMEOUT=60
COUNT=0

echo "Ожидание PostgreSQL ($DB_HOST:$DB_PORT) (таймаут: ${TIMEOUT}с)..."
until nc -z "$DB_HOST" "$DB_PORT"; do
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $TIMEOUT ]; then
        echo "⛔ Таймаут подключения к PostgreSQL!"
        exit 1
    fi
    echo "⏳ Ожидание ($COUNT/$TIMEOUT)..."
    sleep 1
done

echo "✅ PostgreSQL доступен"

# Дополнительная проверка для Docker Compose
if [ -z "$DATABASE_URL" ] && [ "$DB_HOST" = "db" ]; then
    echo "Выполнение дополнительной проверки для Docker Compose..."
    until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$PG_USER" -d "$PG_NAME"; do
        sleep 1
        echo "⏳ Ожидание инициализации БД..."
    done
    echo "✅ БД полностью готова к работе"
fi