from pickle import dump, load


class Database:
    def __init__(self, filename):
        self._filename = filename

    def save(self, records):
        with open(self._filename, 'wb') as file:
            dump(records, file)

    def load(self):
        with open(self._filename, 'rb') as file:
            return load(file)
