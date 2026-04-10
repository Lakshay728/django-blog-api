web: python manage.py migrate && python manage.py createsu && gunicorn mysite.wsgi:application
worker: celery -A mysite worker --loglevel=info