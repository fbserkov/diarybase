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
        db = Database()
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        text_save = 'Test text.'
        db.set(dt, text_save)

        filename = 'test.db'
        db.save(filename)
        del db
        db = Database()
        db.load(filename)
        text_load = db.get(dt)

        self.assertEqual(text_save, text_load)


if __name__ == '__main__':
    unittest.main()
