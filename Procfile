web: gunicorn DistantInform.wsgi
worker: celery worker --app=DistantInform.celery.app -beat
release: python manage.py makemigrations
