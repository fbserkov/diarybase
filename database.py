from datetime import datetime
from pickle import dump, load


class Database:
    def __init__(self, filename=None):
        self._filename = filename
        self._records = {}

    def save(self):
        if self._filename:
            with open(self._filename, 'wb') as file:
                dump(self._records, file)

    def load(self):
        if self._filename:
            with open(self._filename, 'rb') as file:
                self._records = load(file)

    def set(self, dt: datetime, text):
        self._records[dt] = text

    def get(self, dt: datetime):
        return self._records[dt]
