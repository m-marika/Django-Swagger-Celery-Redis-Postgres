# Указываем базовый образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем системные зависимости, включая libpq-dev
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY . /app/

# Экспортируем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Выполняем миграции и собираем статику при запуске контейнера
CMD ["python", "manage.py", "migrate"] && \
    ["python", "manage.py", "collectstatic", "--noinput"] && \
    ["python", "manage.py", "runserver", "0.0.0.0:8000"]
