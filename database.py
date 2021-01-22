import os
from pickle import dump, load


class Database:
    def __init__(self):
        self._filename = os.getenv('DIARYBASE_DBNAME')
        self._tags = None
        self._records = None
        self._words = None

    def clear(self):
        self._tags = {}
        self._records = []
        self._words = set()

    def load(self):
        try:
            with open(self._filename, 'rb') as file:
                data = load(file)
            self._tags, self._records, self._words = data
        except FileNotFoundError:
            self.clear()

    def save(self):
        data = self._tags, self._records, self._words
        with open(self._filename, 'wb') as file:
            dump(data, file)

    def get_tags(self) -> dict:
        return self._tags

    def set_tags(self, tags: dict):
        self._tags = tags

    def get_records(self) -> list:
        return self._records

    def get_words(self) -> set:
        return self._words

    def set_words(self, words: set):
        self._words = words


db: Database = Database()
