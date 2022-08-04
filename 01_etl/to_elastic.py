import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ES_PORT = int(os.environ.get('es_port'))
ES_HOST = os.environ.get('es_host')
INDEX_NAME = os.environ.get('index_name')

es_client = Elasticsearch('http://{host}:{port}'.format(
    host=ES_HOST, port=ES_PORT)
)


def upload_to_elastic(data: dict):
    actions = []
    for item in data:
        actors_names = []
        writers_names = []
        actors = []
        writers = []
        director = ''
        for i in data[item]['persons']:
            if i[0] == 'director':
                director = i[2]
            elif i[0] == 'actor':
                actors_names.append(i[2])
                actors.append({"id": i[1], "name": i[2]})
            elif i[0] == 'writer':
                writers_names.append(i[2])
                writers.append({"id": i[1], "name": i[2]})
        dat = {
            "id": item, "imdb_rating": data[item]['fw'][2],
            "genre": data[item]['genre'], "title": data[item]['fw'][0],
            "description": data[item]['fw'][1], "director": director,
            "actors_names": actors_names, "writers_names": writers_names,
            "actors": actors, "writers": writers
        }
        index = {"index": {"_index": "movies", "_id": item}}
        actions.append(index)
        actions.append(dat)
    es_client.bulk(index=INDEX_NAME, operations=actions)
