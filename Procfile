web: gunicorn DistantInform.wsgi
<<<<<<< HEAD
worker : celery -A DistantInform.celery.app  worker -P solo -E
python manage.py celeryd -v 2 -B -s celery -E -l INFO
=======
worker: celery -A DistantInform.celery.app worker -l info -B

>>>>>>> 52b387ca6cc463e94dbf20500bc745ddb3fade8a
