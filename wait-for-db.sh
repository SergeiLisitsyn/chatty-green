#!/bin/bash
set -e

host="${DB_HOST:-db}"
port="${DB_PORT:-5432}"
timeout=30

echo "Ожидание PostgreSQL ($host:$port)..."

while ! nc -z -w 1 "$host" "$port"; do
    timeout=$((timeout - 1))
    if [ $timeout -le 0 ]; then
        echo "Таймаут подключения к БД!" >&2
        exit 1
    fi
    sleep 1
done

echo "База данных доступна!"