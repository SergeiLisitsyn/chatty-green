#!/bin/bash

# Проверим, заданы ли переменные
if [ -z "$PG_HOST" ] || [ -z "$PG_PORT" ]; then
  echo "❌ Переменные окружения PG_HOST и PG_PORT не заданы!" >&2
  exit 1
fi

echo "⏳ Ожидание подключения к БД $PG_HOST:$PG_PORT..."

for i in {1..60}; do
  if nc -z "$PG_HOST" "$PG_PORT"; then
    echo "✅ База данных доступна — продолжаем."
    exit 0
  fi
  echo "Попытка $i: ждём 1 секунду..."
  sleep 1
done

echo "❌ Таймаут: база данных так и не ответила через 60 секунд." >&2
exit 1

