
FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей (включая netcat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd && \
    ca-certificates \
    rm -rf /var/lib/apt/lists/*

# Копируем зависимости первыми (для кэширования)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn  # Явно добавляем gunicorn!

# Копируем остальные файлы
COPY . .

# Делаем скрипты исполняемыми
RUN chmod +x entrypoint.sh wait-for-db.sh

CMD ["./entrypoint.sh"]