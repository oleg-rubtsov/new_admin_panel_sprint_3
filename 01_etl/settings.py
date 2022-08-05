from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    dbname: str = Field(..., env='dbname')
    user: str = Field(..., env='user')
    password: str = Field(..., env='password')
    host: str = Field(..., env='host')
    port: str = Field(..., env='port')

    es_host: str = Field(..., env='es_host')
    es_port: str = Field(..., env='es_port')
    index_name: str = Field(..., env='index_name')

    initial_date: str = '2021-01-01'
    delay: int = 3600

    max_attemts: int = 10
    border_sleep_time: int = 1
    factor: int = 2
    start_sleep_time: float = 0.1

    condition_file: str = 'condition_file.txt'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        fields = {
            'initial_date': {
                'env': 'initial_date',
            },
            'delay': {
                'env': 'delay',
            },
        }
