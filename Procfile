web: gunicorn DistantInform.wsgi
worker: celery worker --app=DistantInform.celery.app
python manage.py celeryd -v 2 -B -s celery -E -l INFO
release: python manage.py makemigrations
