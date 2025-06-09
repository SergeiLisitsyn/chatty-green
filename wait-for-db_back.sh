#!/bin/bash
set -e

# Автоматическое извлечение хоста и порта из DATABASE_URL
DB_HOST=$(python -c "from urllib.parse import urlparse; import os; u = urlparse(os.getenv('DATABASE_URL')); print(u.hostname)")
DB_PORT=$(python -c "from urllib.parse import urlparse; import os; u = urlparse(os.getenv('DATABASE_URL')); print(u.port or 5432)")

timeout=30
interval=1

echo "Ожидание PostgreSQL ($DB_HOST:$DB_PORT)..."

for i in $(seq 1 $timeout); do
    if timeout 1 bash -c "cat < /dev/null > /dev/tcp/$DB_HOST/$DB_PORT" 2>/dev/null; then
        echo "✅ PostgreSQL доступен!"
        exit 0
    fi
    echo "⏳ Попытка $i/$timeout..."
    sleep $interval
done

echo "❌ Таймаут подключения к БД!"
exit 1