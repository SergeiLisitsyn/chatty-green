
FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей (включая netcat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости первыми (для кэширования)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  #

# Копируем остальные файлы
COPY . .

# Делаем скрипты исполняемыми
RUN chmod +x entrypoint.sh wait-for-db.sh
EXPOSE 8000
CMD ["./entrypoint.sh"]