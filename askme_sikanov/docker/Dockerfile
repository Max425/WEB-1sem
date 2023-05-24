# Используем базовый образ Python
FROM python:3.9

# Установка зависимостей проекта
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта
COPY . /app/

# Запуск команды при запуске контейнера
CMD python manage.py runserver 0.0.0.0:8000
