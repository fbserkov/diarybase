import os
import pickle


class Database:
    def __init__(self):
        self._filename = os.getenv('DIARYBASE_DBNAME')
        self._data = None

        self._tags = None
        self._records = None
        self._words = None

    def clear(self):
        self._data = {}

        self._tags = {}
        self._records = []
        self._words = set()

    def load(self):
        try:
            with open(self._filename, 'rb') as file:
                data = pickle.load(file)
            self._data, self._tags, self._records, self._words = data
        except FileNotFoundError:
            self.clear()

    def save(self):
        data = self._data, self._tags, self._records, self._words
        with open(self._filename, 'wb') as file:
            pickle.dump(data, file)

    def get(self, key: str) -> dict:
        return self._data[key]

    def set(self, key: str, value):
        self._data[key] = value

    def get_records(self) -> list:
        return self._records

    def get_words(self) -> set:
        return self._words

    def set_words(self, words: set):
        self._words = words


db: Database = Database()
