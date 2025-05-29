#!/bin/sh
set -e

host="${DATABASE_HOST:-db}"
port="${DATABASE_PORT:-5432}"

echo "Ожидание PostgreSQL ($host:$port)..."
until nc -z "$host" "$port"; do
  sleep 1
done

echo "PostgreSQL доступен"