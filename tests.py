import unittest
from datetime import datetime

from storage import Storage


class TestDiaryBase(unittest.TestCase):
    def setUp(self) -> None:
        self._filename = 'test.db'
        self._storage = Storage(self._filename)

    def test_initial(self):
        dt = datetime(year=2021, month=1, day=15, hour=19, minute=46)
        text_in = 'Test text.'
        self._storage.set(dt, text_in)
        text_out = self._storage.get(dt)
        self.assertEqual(text_out, text_in)

    def test_save_and_load(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        text_save = 'Test text.'
        self._storage.set(dt, text_save)
        self._storage.save()

        storage = Storage(self._filename)
        storage.load()
        text_load = storage.get(dt)
        self.assertEqual(text_save, text_load)

    def test_set_to_existing_datetime(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=46)
        self._storage.set(dt, 'Test text 1.')
        with self.assertRaises(Exception):
            self._storage.set(dt, 'Test text 2.')


if __name__ == '__main__':
    unittest.main()
