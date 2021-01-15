import unittest
from datetime import datetime

from database import Database


class TestDiaryBase(unittest.TestCase):
    def test_initial(self):
        db = Database()
        dt = datetime(year=2021, month=1, day=15, hour=19, minute=46)
        text_in = 'Test text.'

        db.set(dt, text_in)
        text_out = db.get(dt)

        self.assertEqual(text_out, text_in)

    def test_save_and_load(self):
        filename = 'test.db'
        db = Database(filename)
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        text_save = 'Test text.'
        db.set(dt, text_save)

        db.save()
        db = Database(filename)
        db.load()
        text_load = db.get(dt)

        self.assertEqual(text_save, text_load)

    def test_set_to_existing_datetime(self):
        db = Database()
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=46)
        text = 'Test text.'

        db.set(dt, text)
        with self.assertRaises(Exception):
            db.set(dt, text)


if __name__ == '__main__':
    unittest.main()
