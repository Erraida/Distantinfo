import os
from datetime import datetime

from celery import shared_task

from .models import Lecture


@shared_task
def add(x, y):
    date = datetime.today()
    art_hidden = Lecture.objects.all()
    print(datetime.now().time())



@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

# celery -A DistantInform.celery.app  worker -P solo -E
