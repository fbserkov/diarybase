import unittest
from datetime import datetime

from note import Note
from storage import Storage


class TestDiaryBase(unittest.TestCase):
    def setUp(self) -> None:
        self._filename = 'test.db'
        self._storage = Storage(self._filename)

    def test_initial(self):
        dt = datetime(year=2021, month=1, day=15, hour=19, minute=46)
        note_in = Note('Text.')
        self._storage.set(dt, note_in)
        note_out = self._storage.get(dt)
        self.assertEqual(note_in, note_out)

    def test_save_and_load(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        note_save = Note('Text.')
        self._storage.set(dt, note_save)
        self._storage.save()

        storage = Storage(self._filename)
        storage.load()
        note_load = storage.get(dt)
        self.assertEqual(note_save, note_load)

    def test_set_to_existing_datetime(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=46)
        self._storage.set(dt, Note('First text.'))
        with self.assertRaises(Exception):
            self._storage.set(dt, Note('Second text.'))


if __name__ == '__main__':
    unittest.main()
