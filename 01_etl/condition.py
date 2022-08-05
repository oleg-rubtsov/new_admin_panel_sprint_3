import abc
import json
import os
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        with open(self.file_path, 'r+') as outfile:
            try:
                data = json.load(outfile)
                data.update(state)
                outfile.seek(0)
                json.dump(data, outfile)
            except ValueError:
                json.dump(state, outfile)

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        if os.stat(self.file_path).st_size == 0:
            return {}
        with open(self.file_path) as json_file:
            data = json.load(json_file)
            if key in data:
                return data[key]
            else:
                return None


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path


class State:
    """
    Класс для хранения состояния при работе с данными,
    чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу
    с БД или распределённым хранилищем.
    """
    def __init__(self, storage: JsonFileStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        data = {}
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        return self.storage.retrieve_state(key)
