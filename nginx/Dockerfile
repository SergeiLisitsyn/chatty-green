# 1-й этап – только чтобы забрать статику
FROM chatty_green_web:latest AS static-src


# 2-й этап – финальный Nginx
FROM  nginx:1.27-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=static-src /app/static /static

