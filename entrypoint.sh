#!/bin/sh
set -x  # Включить логирование

echo "=== Проверка базы данных ==="
./wait-for-db.sh

echo "=== Применение миграций ==="
python manage.py migrate --no-input

# Создание суперпользователя (добавьте эти строки)
echo "=== Создание суперпользователя ==="
python create_admin.py

echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear

echo "=== Запуск сервера ==="
exec python manage.py runserver 0.0.0.0:8000  # Используйте exec для корректного завершенияя