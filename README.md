# Django + Swagger + Celery + Redis

Тестовое задание

## Локальное развёртывание

1. Установите python и настройте виртуальную среду

   ```python -m venv venv```
   ```source venv/Scripts/activate```

2. Выполните установку зависимостей

   ```pip install -r requirements.txt```

3. Создайте файл .env в корневой директории проекта и добавьте следующие переменные окружения:

   ```POSTGRES_DB='your_db_name' ```
   ```POSTGRES_USER='your_db_user' ```
   ```POSTGRES_PASSWORD='your_db_password' ```
   ```CELERY_BROKER_URL='redis://localhost:6379/0' ```
   ```CELERY_RESULT_BACKEND='redis://localhost:6379/0' ```

4. Примените миграции и создайте суперпользователя:
   
   ```python manage.py migrate```
   ```python manage.py createsuperuser```

### Запуск

Выполните команды:
```python manage.py runserver```
```celery -A yourproject worker --loglevel=info```

По умолчанию приложение запустится на 8000-м порту и использованием sqlite (строку подключения можно поменять с помощью
переменных окружения - .env)

- http://localhost:8000
- http://localhost:8000/swagger/

## Запуск с помощью docker-compose

1. Создайте файл .env в корневой директории проекта и добавьте следующие переменные окружения:

   ```POSTGRES_DB='your_db_name' ```
   ```POSTGRES_USER='your_db_user' ```
   ```POSTGRES_PASSWORD='your_db_password' ```
   ```CELERY_BROKER_URL='redis://localhost:6379/0' ```
   ```CELERY_RESULT_BACKEND='redis://localhost:6379/0' ```

2. Выполнить команды:
 ```docker-compose up --build```
 ```docker-compose exec django python manage.py createsuperuser```
 ```docker-compose exec django python manage.py migrate```

При запуске контейнера приложения будут установлены все неустановленные зависимости 

По умолчанию приложение запустится на 8000-м порту и использованием postgres 

- http://localhost:8000
- http://localhost:8000/swagger/


