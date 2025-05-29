set -x  # Включить подробное логирование

echo "=== Переменные окружения ==="
printenv
echo "==========================="

# Ожидание базы данных
echo "Ожидание базы данных..."
./wait-for-db.sh

echo "=== Применение миграций ==="
python manage.py migrate --no-input

echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

echo "Проверка Django..."
python manage.py check

# Временный запуск Gunicorn без exec + сохранение логов
echo "=== Запуск Gunicorn ==="
gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile /app/gunicorn-access.log \
    --error-logfile /app/gunicorn-error.log \
    --log-level debug &

# Сохраняем PID Gunicorn для возможного завершения
GUNICORN_PID=$!

echo "=== Запуск Gunicorn завершен (PID $GUNICORN_PID) ==="

# Удержание контейнера активным для диагностики
echo "Контейнер активен для диагностики. Используйте Shell для отладки."
tail -f /dev/null