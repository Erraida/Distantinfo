import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DistantInform.settings')
app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'send-report-every-single-minute': {  # Название
        'task': 'editor.tasks.Lecture_check',  # Вызов задачи
        'schedule': 60,  # Время цикла в секундах
    },
}

# celery -A DistantInform.celery.app  worker -P solo -E|| Запуск обработки задач
# celery -A DistantInform.celery.app  beat -l INFO  || Запуск обработки расписаний
