from datetime import datetime
from pickle import dump, load

from note import Note


class Storage:
    def __init__(self, filename):
        self._filename = filename
        self._notes = {}

    def save(self):
        with open(self._filename, 'wb') as file:
            dump(self._notes, file)

    def load(self):
        with open(self._filename, 'rb') as file:
            self._notes = load(file)

    def set(self, dt: datetime, note: Note):
        if dt in self._notes:
            raise Exception('This datetime has already been taken.')
        self._notes[dt] = note

    def get(self, dt: datetime) -> Note:
        return self._notes[dt]
