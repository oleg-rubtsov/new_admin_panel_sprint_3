import logging
import os
import time
from functools import wraps

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from load_from_postgres import load_from_postgres

load_dotenv()

logger = logging.getLogger(__name__)

INITIAL_DATE = str(os.environ.get('initial_date', default='2021-01-01'))


def backoff(Exception, start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    logger.warning(f"{ex}")
                    time.sleep(sleep_time)
                    if sleep_time < border_sleep_time:
                        sleep_time *= 2 ** factor
                    else:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper


@backoff(Exception)
def psycopg2_connection():
    dsl = {
        'dbname': os.environ.get('dbname', default=None),
        'user': os.environ.get('user', default=None),
        'password': os.environ.get('password', default=None),
        'host': os.environ.get('host', default=None),
        'port': os.environ.get('port', default=None)
    }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        return pg_conn


if __name__ == '__main__':
    load_from_postgres(psycopg2_connection(), INITIAL_DATE)
