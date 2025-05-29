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

# Проверка работы приложения перед запуском
echo "Проверка Django..."
python manage.py check

echo "=== Запуск Gunicorn ==="
exec gunicorn your_project.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug