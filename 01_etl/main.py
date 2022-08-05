import logging
import sys
import time
import typing
from functools import wraps

import psycopg2
from psycopg2.extras import DictCursor

from load_from_postgres import load_from_postgres
from settings import Settings

settings = Settings()

backoff_logger = logging.getLogger(__name__)


def backoff(
    exception: Exception,
    backoff_logger: logging.Logger = logging.getLogger(__name__),
    start_sleep_time: float = settings.start_sleep_time,
    factor: int = settings.factor,
    border_sleep_time: int = settings.border_sleep_time,
    max_attemts: int = settings.max_attemts
) -> typing.Callable:
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time, attemts = start_sleep_time, max_attemts
            while True:
                if attemts == 0:
                    sys.exit(0)
                try:
                    return func(*args, **kwargs)
                except exception as ex:
                    attemts -= 1
                    backoff_logger.warning("Unexpected error occured.", exc_info=ex)
                    time.sleep(sleep_time)
                    if sleep_time < border_sleep_time:
                        sleep_time *= 2 ** factor
                    else:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper


@backoff(Exception, backoff_logger)
def psycopg2_connection():
    dsl = {
        'dbname': settings.dbname,
        'user': settings.user,
        'password': settings.password,
        'host': settings.host,
        'port': settings.port
    }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        return pg_conn


if __name__ == '__main__':
    while True:
        load_from_postgres(psycopg2_connection(), settings.initial_date)
        time.sleep(settings.delay)
