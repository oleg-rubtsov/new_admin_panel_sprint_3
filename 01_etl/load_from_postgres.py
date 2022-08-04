import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection

from condition import JsonFileStorage, State
from to_elastic import upload_to_elastic

load_dotenv()


def data_grouping(data: dict):
    tmp = {}
    for item in data:
        fw_id, title, description, rating, type, created_at, \
            updated_at, p_role, p_id, p_full_name, genre_name = item
        if fw_id not in tmp:
            tmp[fw_id] = {}
            tmp[fw_id]['fw'] = [
                title, description, rating, type, created_at, updated_at
            ]
            tmp[fw_id]['persons'] = [[p_role, p_id, p_full_name]]
            tmp[fw_id]['genre'] = [genre_name]
        else:
            if [p_role, p_id, p_full_name] not in tmp[fw_id]['persons']:
                tmp[fw_id]['persons'].append([p_role, p_id, p_full_name])
            if genre_name not in tmp[fw_id]['genre']:
                tmp[fw_id]['genre'].append(genre_name)
    return tmp


def sql_query_for_movies(id_films: dict):
    return "SELECT \
                fw.id as fw_id, \
                fw.title, \
                fw.description, \
                fw.rating, \
                fw.type, \
                fw.created_at, \
                fw.updated_at, \
                pfw.role, \
                p.id, \
                p.full_name, \
                g.name \
            FROM content.film_work fw \
            LEFT JOIN content.person_film_work pfw \
            ON pfw.film_work_id = fw.id \
            LEFT JOIN content.person p ON p.id = pfw.person_id \
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id \
            LEFT JOIN content.genre g ON g.id = gfw.genre_id \
            WHERE fw.id IN {id_films};".format(id_films=tuple(id_films))


def sql_query_for_related_data(table: str, content_id: str, base_id: dict):
    return "SELECT fw.id, fw.updated_at \
            FROM content.film_work fw \
            LEFT JOIN content.{table} dfw ON dfw.film_work_id = fw.id \
            WHERE dfw.{content_id} IN {base_id}\
            ORDER BY fw.updated_at \
            LIMIT 10000;".format(
                table=table, content_id=content_id, base_id=tuple(base_id)
            )


def sql_query_for_content(table: str, last_updated: int):
    return "SELECT id, updated_at FROM \
           content.{table} WHERE updated_at > '{last_updated}' \
           ORDER BY updated_at LIMIT 100;".format(
               table=table, last_updated=last_updated
            )


def loading(
    curs_postgres: psycopg2.extensions.cursor,
    state: State, INITIAL_DATE: str, data_items: dict
):
    while True:
        state_info = state.get_state(data_items['state_name'])
        last_updated = state_info if state_info else INITIAL_DATE
        curs_postgres.execute(
            sql_query_for_content(data_items['table'], last_updated)
        )
        data = curs_postgres.fetchall()
        base_id = [item[0] for item in data]
        if base_id:
            if 'related_table' in data_items.keys():
                curs_postgres.execute(
                    sql_query_for_related_data(
                        data_items['related_table'],
                        data_items['related_id_name'],
                        base_id
                    )
                )
                related_data = curs_postgres.fetchall()
                id_films = [item[0] for item in related_data]
            else:
                id_films = base_id
            curs_postgres.execute(sql_query_for_movies(id_films))
            films = curs_postgres.fetchall()
            upload_to_elastic(data_grouping(films))
            state.set_state(data_items['state_name'], str(data[-1][1]))
        else:
            break


def load_from_postgres(pg_conn: _connection, INITIAL_DATE: str):
    storage = JsonFileStorage('condition_file.txt')
    state = State(storage)
    curs_postgres = pg_conn.cursor()
    loading(
        curs_postgres, state, INITIAL_DATE,
        {
            'table': 'person',
            'related_table': 'person_film_work',
            'related_id_name': 'person_id',
            'state_name': 'persons_updated_at'
        }
    )
    loading(
        curs_postgres, state, INITIAL_DATE,
        {
            'table': 'genre',
            'related_table': 'genre_film_work',
            'related_id_name': 'genre_id',
            'state_name': 'genre_updated_at'
        }
    )
    loading(
        curs_postgres, state, INITIAL_DATE,
        {
            'table': 'film_work',
            'state_name': 'film_updated_at'
        }
    )
