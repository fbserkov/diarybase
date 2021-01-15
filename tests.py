from datetime import datetime
import unittest


class TestDiaryBase(unittest.TestCase):
    def test_initial(self):
        db = Database()
        dt = datetime(year=2021, month=1, day=15, hour=19, minute=46),
        text_in = 'This is test text.'

        db.add(dt, text_in)
        text_out = db.get(dt)

        self.assertEqual(text_out, text_in)


if __name__ == '__main__':
    unittest.main()
