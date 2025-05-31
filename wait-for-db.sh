#!/bin/sh
set -e

# Всегда используем параметры из DATABASE_URL
DB_HOST=$(echo "$DATABASE_URL" | sed -e 's/.*@\([^:]*\):.*/\1/')
DB_PORT=$(echo "$DATABASE_URL" | sed -e 's/.*:\([0-9]*\)\/.*/\1/')

echo "Ожидание PostgreSQL ($DB_HOST:$DB_PORT)..."

# Используем psql вместо netcat для надежной проверки
until PGPASSWORD=$(echo "$DATABASE_URL" | cut -d'@' -f1 | cut -d':' -f3) \
      psql -h "$DB_HOST" -p "$DB_PORT" \
      -U $(echo "$DATABASE_URL" | cut -d'/' -f3 | cut -d':' -f1) \
      -d $(echo "$DATABASE_URL" | cut -d'/' -f4) \
      -c "SELECT 1;" > /dev/null 2>&1; do
  sleep 1
  echo "⏳ Ожидание PostgreSQL..."
done

echo "✅ PostgreSQL доступен и отвечает на запросы"