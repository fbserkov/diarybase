from pickle import dump, load

from record import Record


class Storage:
    def __init__(self, filename):
        self._filename = filename
        self._records = []

    def __len__(self):
        return len(self._records)

    def __str__(self):
        return '\n'.join(str(record) for record in self._records)

    def append(self, r: Record):
        self._records.append(r)

    def save(self):
        with open(self._filename, 'wb') as file:
            dump(self._records, file)

    def load(self):
        with open(self._filename, 'rb') as file:
            self._records = load(file)
