#!/bin/bash
set -euxo pipefail

echo "=== [$(date)] Старт entrypoint.sh ==="
echo "=== Переменные окружения ==="
printenv | sort
echo "==========================="

# Ожидание БД
if [ -f ./wait-for-db.sh ]; then
  echo "Ожидание базы данных..."
  chmod +x ./wait-for-db.sh
  ./wait-for-db.sh
else
  echo "⚠️ wait-for-db.sh не найден, пропускаем проверку БД"
fi

# Миграции
echo "=== Применение миграций ==="
python manage.py migrate --no-input

# Статика
echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

# Проверка конфигурации
echo "Проверка Django..."
python manage.py check

# Проверка порта
echo "Проверка доступности порта ${PORT:-10000}..."
if ss -tuln | grep ":${PORT:-10000}"; then
  echo "⛔ Порт ${PORT:-10000} уже занят!"
  exit 1
fi

# Запуск Gunicorn
echo "=== Запуск Gunicorn ==="
WORKERS=${WEB_CONCURRENCY:-$(( $(nproc) * 2 + 1 ))}
TIMEOUT=${GUNICORN_TIMEOUT:-120}

exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers $WORKERS \
    --timeout $TIMEOUT \
    --access-logfile - \
    --error-logfile - \
    --log-level debug