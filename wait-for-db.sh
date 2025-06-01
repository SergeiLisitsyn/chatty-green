#!/bin/bash
set -e

host="${DB_HOST:-db}"
port="${DB_PORT:-5432}"
max_retries=30
retry_interval=2

echo "Ожидание PostgreSQL ($host:$port)..."

for ((i=1; i<=$max_retries; i++)); do
    if nc -z -w 1 "$host" "$port"; then
        echo "✅ PostgreSQL доступен!"
        exit 0
    fi
    echo "⏳ Попытка $i/$max_retries..."
    sleep $retry_interval
done

echo "❌ Ошибка: PostgreSQL не доступен после $max_retries попыток!"
exit 1