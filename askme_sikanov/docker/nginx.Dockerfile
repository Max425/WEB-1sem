# Используем базовый образ Nginx
FROM nginx:latest

# Копирование конфигурационного файла Nginx
COPY nginx.conf /etc/nginx/nginx.conf
