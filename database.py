import shelve

MAIN_DB_NAME = 'main.db'
TEST_DB_NAME = 'test.db'


class Database:
    def __init__(self, filename):
        self._filename = filename

    def save(self, key, records):
        with shelve.open(self._filename) as d:
            d[key] = records

    def load(self, key):
        with shelve.open(self._filename) as d:
            return d[key]


db = Database(MAIN_DB_NAME)
