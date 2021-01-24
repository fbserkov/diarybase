import os
import pickle


class Database:
    def __init__(self):
        self._filename = os.getenv('DIARYBASE_DBNAME')
        self._data = None

    def __getitem__(self, item: str):
        return self._data[item]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def clear(self):
        self._data = {}

    def load(self):
        try:
            with open(self._filename, 'rb') as file:
                self._data = pickle.load(file)
        except FileNotFoundError:
            self.clear()

    def save(self):
        with open(self._filename, 'wb') as file:
            pickle.dump(self._data, file)


db: Database = Database()
