FROM python:3.12-slim

WORKDIR /app

# Системные пакеты
# Установка диагностических утилит:
#   procps    - для ps, top, free
#   net-tools - для netstat, ifconfig
#   iputils-ping - для ping
#   curl      - для HTTP-запросов
#   vim-tiny  - для просмотра файлов
RUN apt-get update && apt-get install -y \
    procps \
    net-tools \
    iputils-ping \
    curl \
    vim-tiny \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python-зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Скрипты
COPY entrypoint.sh wait-for-db.sh ./
RUN chmod +x entrypoint.sh wait-for-db.sh

COPY wait-for-db.py ./
RUN chmod +x wait-for-db.py

# --- переменная окружения для этапа build ---
ENV RUN_MIGRATIONS="false" \
    DOCKERIZED=1 \
    PYTHONUNBUFFERED=1

# Код проекта
COPY . .

# Если нужно собирать статику, раскомментируй:
# RUN mkdir -p /static && python manage.py collectstatic --no-input
EXPOSE 10000

# Команда запуска (та же что и в docker-compose)
#CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --no-input --clear && gunicorn chatty.wsgi:application --bind 0.0.0.0:10000"]

CMD ["./entrypoint.sh", "echo 'Контейнер запущен!'"]
#ENTRYPOINT ["./entrypoint.sh"]
# Временная замена сложного entrypoint
