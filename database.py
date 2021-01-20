import shelve


class Database:
    def __init__(self, filename):
        self._filename = filename

    def save(self, key, records):
        with shelve.open(self._filename) as d:
            d[key] = records

    def load(self, key):
        with shelve.open(self._filename) as d:
            return d[key]
