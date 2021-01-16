import unittest
from datetime import datetime

from database import Database


class TestDiaryBase(unittest.TestCase):
    def setUp(self) -> None:
        self._filename = 'test.db'
        self._db = Database(self._filename)

    def test_initial(self):
        dt = datetime(year=2021, month=1, day=15, hour=19, minute=46)
        text_in = 'Test text.'

        self._db.set(dt, text_in)
        text_out = self._db.get(dt)

        self.assertEqual(text_out, text_in)

    def test_save_and_load(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        text_save = 'Test text.'
        self._db.set(dt, text_save)

        self._db.save()
        db = Database(self._filename)
        db.load()
        text_load = db.get(dt)

        self.assertEqual(text_save, text_load)

    def test_set_to_existing_datetime(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=46)
        text = 'Test text.'

        self._db.set(dt, text)
        with self.assertRaises(Exception):
            self._db.set(dt, text)


if __name__ == '__main__':
    unittest.main()
