FROM python:3.7

WORKDIR /etl

COPY requirements.txt requirements.txt

RUN  python -m pip install --upgrade pip \
     && pip install psycopg2-binary \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python", "./main.py"]
