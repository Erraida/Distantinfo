web: gunicorn DistantInform.wsgi
worker: celery -A DistantInform.celery.app worker -B -l info
