import unittest
from datetime import datetime

from note import Note
from storage import Storage


class TestNote(unittest.TestCase):
    def test_str(self):
        note = Note('Text.')
        self.assertEqual('Text.', str(note))


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self._filename = 'test.db'
        self._storage = Storage(self._filename)

    def test_set_and_get(self):
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

    def test_reset_to_existing_datetime(self):
        dt = datetime(year=2021, month=1, day=16, hour=19, minute=46)
        correct_note = Note('Correct text.')
        self._storage.set(dt, Note('Incorrect text.'))
        self._storage.set(dt, correct_note, reset=True)
        note_load = self._storage.get(dt)
        self.assertEqual(correct_note, note_load)

    def test_str(self):
        dt_1 = datetime(year=2021, month=1, day=16, hour=19, minute=4)
        self._storage.set(dt_1, Note('First text for display.'))
        dt_2 = datetime(year=2021, month=1, day=16, hour=19, minute=20)
        self._storage.set(dt_2, Note('Second text for display.'))

        self.assertEqual(
            '[16.01.2021 19:04:00] First text for display.\n'
            '[16.01.2021 19:20:00] Second text for display.\n',
            str(self._storage),
        )


if __name__ == '__main__':
    unittest.main()
