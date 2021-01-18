from datetime import datetime
from pickle import dump, load

from note import Note


class Storage:
    def __init__(self, filename):
        self._filename = filename
        self._notes = []

    def __str__(self):
        return '\n'.join(str(note) for note in self._notes)

    def append(self, note: Note):
        self._notes.append(note)

    def save(self):
        with open(self._filename, 'wb') as file:
            dump(self._notes, file)

    def load(self):
        with open(self._filename, 'rb') as file:
            self._notes = load(file)
