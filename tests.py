import unittest
from datetime import datetime

from database import Database, TEST_DB_NAME
from record import Record
from recordlist import RecordList
from spellchecker import SpellChecker
from tagdict import TagDict
from tags import TAGS

db = Database(TEST_DB_NAME)

TAGS[0] = 'no tag'
TAGS[1] = 'test tag'


class TestTagDict(unittest.TestCase):
    def setUp(self) -> None:
        self._tag_dict = TagDict(db)
        self._tag_dict.save()

    def test_add(self):
        self._tag_dict.add('no tag')
        self._tag_dict.add('test tag')
        self.assertEqual(
            {0: 'no tag', 1: 'test tag'}, self._tag_dict.get_dict())

    def test_save_and_load(self):
        test_dict = {1: 'no tag', 2: 'test tag'}
        self._tag_dict.set_dict(test_dict)
        self._tag_dict.save()
        td = TagDict(db)
        td.load()
        self.assertEqual(test_dict, td.get_dict())


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


class TestRecordList(unittest.TestCase):
    def setUp(self) -> None:
        self._record_list = RecordList(db)
        self._record_list.save()

    def test_add_and_str(self):
        dt_1 = datetime(year=2021, month=1, day=16, hour=19, minute=4)
        self._record_list.append(Record(dt_1, note='first note'))
        dt_2 = datetime(year=2021, month=1, day=16, hour=19, minute=20)
        self._record_list.append(Record(dt_2, note='second note'))

        self.assertEqual(
            '[16.01.2021 19:04:00] <no tag> first note\n'
            '[16.01.2021 19:20:00] <no tag> second note',
            str(self._record_list),
        )

    def test_many_str(self):
        self._record_list = RecordList(db, str_len=10)
        dt = datetime(year=2021, month=1, day=19, hour=19, minute=38)
        for _ in range(100):
            self._record_list.append(Record(dt, note='note'))

        self.assertEqual(
            10 * '[19.01.2021 19:38:00] <no tag> note\n' + 'last 10 from 100',
            str(self._record_list),
        )

    def test_save_and_load(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        r = Record(dt, note='note')
        self._record_list.append(r)
        self._record_list.save()

        record_list = RecordList(db)
        record_list.load()
        self.assertEqual(
            '[15.01.2021 21:13:00] <no tag> note', str(record_list))


class TestSpellChecker(unittest.TestCase):
    def setUp(self) -> None:
        self._sc = SpellChecker(db)
        self._sc.save()

    def test_empty(self):
        with self.assertRaises(Exception):
            self._sc.check_note('note')

    def test_update(self):
        self._sc.check_note('note', update=True)

    def test_save_and_load(self):
        self._sc.check_note('note', update=True)

        sc = SpellChecker(db)
        sc.load()
        with self.assertRaises(Exception):
            sc.check_note('note')

        self._sc.save()
        sc.load()
        sc.check_note('note')


@unittest.skip
class TestRecordManager(unittest.TestCase):
    def test_add(self):
        rm = RecordManager(db)
        dt = datetime(year=2021, month=1, day=21, hour=21, minute=15)
        rm.add_record(dt, tag='tag', note='note')
        self.assertEqual(
            '[21.01.2021 21:15:00] <tag> note\n', str(rm.get_record_list()))


if __name__ == '__main__':
    unittest.main()
