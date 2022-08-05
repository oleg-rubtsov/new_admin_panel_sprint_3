FROM python:3.7

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN  python -m pip install --upgrade pip \
     && pip install psycopg2-binary \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
