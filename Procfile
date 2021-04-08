web: gunicorn DistantInform.wsgi
worker : celery -A DistantInform.celery.app  worker -P solo -E
python manage.py celeryd -v 2 -B -s celery -E -l INFO
release: python manage.py makemigrations
