import unittest
from datetime import datetime

from record import Record
from storage import Storage


class TestNote(unittest.TestCase):
    def test_str(self):
        dt = datetime(year=2021, month=1, day=18, hour=11, minute=11)
        r = Record(dt, 'Text.')
        self.assertEqual('[18.01.2021 11:11:00] Text.', str(r))


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self._filename = 'test.db'
        self._storage = Storage(self._filename)

    def test_add_and_str(self):
        dt_1 = datetime(year=2021, month=1, day=16, hour=19, minute=4)
        self._storage.append(Record(dt_1, 'First text.'))
        dt_2 = datetime(year=2021, month=1, day=16, hour=19, minute=20)
        self._storage.append(Record(dt_2, 'Second text.'))

        self.assertEqual(
            '[16.01.2021 19:04:00] First text.\n'
            '[16.01.2021 19:20:00] Second text.',
            str(self._storage),
        )

    def test_save_and_load(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        r = Record(dt, 'Text.')
        self._storage.append(r)
        self._storage.save()

        storage = Storage(self._filename)
        storage.load()
        self.assertEqual('[15.01.2021 21:13:00] Text.', str(storage))


if __name__ == '__main__':
    unittest.main()
