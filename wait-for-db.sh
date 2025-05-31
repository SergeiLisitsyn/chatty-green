#!/bin/sh
set -e

# Извлекаем параметры из DATABASE_URL
DB_HOST=$(echo "$DATABASE_URL" | sed -e 's/.*@\([^:]*\):.*/\1/')
DB_PORT=$(echo "$DATABASE_URL" | sed -e 's/.*:\([0-9]*\)\/.*/\1/')

TIMEOUT=60
COUNT=0

echo "Ожидание PostgreSQL ($DB_HOST:$DB_PORT) (таймаут: ${TIMEOUT}с)..."

# Используем bash-встроенный TCP-сокет вместо netcat
until (timeout 1 bash -c "cat < /dev/null > /dev/tcp/$DB_HOST/$DB_PORT") &> /dev/null; do
    COUNT=$((COUNT+1))
    if [ $COUNT -ge $TIMEOUT ]; then
        echo "⛔ Таймаут подключения к PostgreSQL!"
        exit 1
    fi
    echo "⏳ Ожидание ($COUNT/$TIMEOUT)..."
    sleep 1
done

echo "✅ PostgreSQL доступен"