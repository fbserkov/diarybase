from datetime import datetime
from pickle import dump, load


class Storage:
    def __init__(self, filename):
        self._filename = filename
        self._records = {}

    def save(self):
        with open(self._filename, 'wb') as file:
            dump(self._records, file)

    def load(self):
        with open(self._filename, 'rb') as file:
            self._records = load(file)

    def set(self, dt: datetime, text):
        if dt in self._records:
            raise Exception('This datetime has already been taken.')
        self._records[dt] = text

    def get(self, dt: datetime):
        return self._records[dt]
