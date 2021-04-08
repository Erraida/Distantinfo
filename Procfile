web: gunicorn DistantInform.wsgi
worker: celery -A DistantInform.celery.app worker -l info -B
release: python manage.py makemigrations
