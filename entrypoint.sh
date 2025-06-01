#!/bin/bash
set -x  # Режим отладки

echo "=== Старт entrypoint ==="

# Ожидание БД (с таймаутом)
if ! ./wait-for-db.sh; then
    echo "ОШИБКА: Не удалось подключиться к БД!" >&2
    exit 1
fi

# Миграции (пропускаем при ошибке)
echo "=== Применение миграций ==="
python manage.py migrate --no-input || echo "Предупреждение: миграции не применены"

# Статика
echo "=== Сбор статики ==="
python manage.py collectstatic --no-input --clear || echo "Предупреждение: ошибка сбора статики"

# Проверка Django
if ! python manage.py check; then
    echo "ОШИБКА: Проверка Django не пройдена!" >&2
    exit 1
fi

# Главный процесс (используем PORT от Render)
echo "=== Запуск Gunicorn ==="
exec gunicorn chatty.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug