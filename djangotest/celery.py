from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем Django настройки в Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangotest.settings')

app = Celery('djangotest')

# Используем настройки Django для Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение тасков в приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
