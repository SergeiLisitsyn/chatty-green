
FROM python:3.12-slim
WORKDIR /app
COPY entrypoint.sh .
CMD ["/bin/sh", "entrypoint.sh"]  # Явный вызов через sh