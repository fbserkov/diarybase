import unittest
from datetime import datetime

from record import Record
from storage import Storage
from tags import TAGS

TAGS[0] = 'no tag'
TAGS[1] = 'test tag'


class TestNote(unittest.TestCase):
    def test_empty(self):
        r = Record()
        self.assertEqual('<no tag>', str(r)[22:])

    def test_dt(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=26)
        r = Record(dt)
        self.assertEqual('[18.01.2021 18:26:00] <no tag>', str(r))

    def test_tag_id(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=40)
        r = Record(dt, tag_id=1)
        self.assertEqual('[18.01.2021 18:40:00] <test tag>', str(r))

    def test_is_active(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=40)
        r = Record(dt, tag_id=1, is_active=True)
        self.assertEqual('[18.01.2021 18:40:00] <test tag: start>', str(r))
        r = Record(dt, tag_id=1, is_active=False)
        self.assertEqual('[18.01.2021 18:40:00] <test tag: end>', str(r))

    def test_note(self):
        dt = datetime(year=2021, month=1, day=18, hour=11, minute=11)
        r = Record(dt, note='note')
        self.assertEqual('[18.01.2021 11:11:00] <no tag> note', str(r))


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self._filename = 'test.db'
        self._storage = Storage(self._filename)

    def test_add_and_str(self):
        dt_1 = datetime(year=2021, month=1, day=16, hour=19, minute=4)
        self._storage.append(Record(dt_1, note='first note'))
        dt_2 = datetime(year=2021, month=1, day=16, hour=19, minute=20)
        self._storage.append(Record(dt_2, note='second note'))

        self.assertEqual(
            '[16.01.2021 19:04:00] <no tag> first note\n'
            '[16.01.2021 19:20:00] <no tag> second note',
            str(self._storage),
        )

    def test_many_str(self):
        self._storage = Storage(self._filename, str_len=10)
        dt = datetime(year=2021, month=1, day=19, hour=19, minute=38)
        for _ in range(100):
            self._storage.append(Record(dt, note='note'))

        self.assertEqual(
            10 * '[19.01.2021 19:38:00] <no tag> note\n' + 'last 10 from 100',
            str(self._storage),
        )

    def test_save_and_load(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        r = Record(dt, note='note')
        self._storage.append(r)
        self._storage.save()

        storage = Storage(self._filename)
        storage.load()
        self.assertEqual('[15.01.2021 21:13:00] <no tag> note', str(storage))


if __name__ == '__main__':
    unittest.main()
