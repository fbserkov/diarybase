import unittest
from datetime import datetime

from database import db
from record import Record
from recordlist import RecordList
from spellchecker import SpellChecker
from tagdict import TagDict
from tags import TAGS

TAGS[0] = 'no tag'
TAGS[1] = 'test tag'


class TestTagDict(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        self._tag_dict = TagDict()

    def test_get_dict(self):
        self.assertEqual({}, self._tag_dict.get_dict())

    def test_add(self):
        self._tag_dict.add('no tag')
        self._tag_dict.add('test tag')
        self.assertEqual(
            {0: 'no tag', 1: 'test tag'}, self._tag_dict.get_dict())

    def test_set_dict(self):
        a_dict = {1: 'no tag', 2: 'test tag'}
        self._tag_dict.set_dict(a_dict)
        self.assertEqual(a_dict, self._tag_dict.get_dict())

    def test_db(self):
        a_dict = {1: 'no tag', 2: 'test tag'}
        self._tag_dict.set_dict(a_dict)
        db.save()
        db.clear()

        db.load()
        td = TagDict()
        self.assertEqual(a_dict, td.get_dict())

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestNote(unittest.TestCase):
    def test_empty(self):
        r = Record()
        self.assertEqual('<no tag>', r.to_str(TAGS)[22:])

    def test_dt(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=26)
        r = Record(dt)
        self.assertEqual('[18.01.2021 18:26:00] <no tag>', r.to_str(TAGS))

    def test_tag_id(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=40)
        r = Record(dt, tag_id=1)
        self.assertEqual('[18.01.2021 18:40:00] <test tag>', r.to_str(TAGS))

    def test_is_active(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=40)
        r = Record(dt, tag_id=1, is_active=True)
        self.assertEqual(
            '[18.01.2021 18:40:00] <test tag: start>', r.to_str(TAGS))
        r = Record(dt, tag_id=1, is_active=False)
        self.assertEqual(
            '[18.01.2021 18:40:00] <test tag: end>', r.to_str(TAGS))

    def test_note(self):
        dt = datetime(year=2021, month=1, day=18, hour=11, minute=11)
        r = Record(dt, note='test')
        self.assertEqual('[18.01.2021 11:11:00] <no tag> test', r.to_str(TAGS))


class TestRecordList(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        self._record_list = RecordList()

    def test_append(self):
        self._record_list.append(Record())
        self.assertEqual(1, len(self._record_list))

    def test_str(self):
        dt = datetime(year=2021, month=1, day=16, hour=19, minute=4)
        self._record_list.append(Record(dt, note='first note'))
        dt = datetime(year=2021, month=1, day=16, hour=19, minute=20)
        self._record_list.append(Record(dt, note='second note'))

        self.assertEqual(
            '[16.01.2021 19:04:00] <no tag> first note\n'
            '[16.01.2021 19:20:00] <no tag> second note',
            str(self._record_list),
        )

    def test_str_len(self):
        self._record_list = RecordList(str_len=5)
        dt = datetime(year=2021, month=1, day=19, hour=19, minute=38)
        for _ in range(10):
            self._record_list.append(Record(dt, note='test'))

        self.assertEqual(
            5 * '[19.01.2021 19:38:00] <no tag> test\n' + 'last 5 from 10',
            str(self._record_list),
        )

    def test_sort_dt(self):
        dt = datetime(year=2021, month=1, day=23, hour=17, minute=37)
        self._record_list.append(Record(dt))
        dt = datetime(year=2021, month=1, day=23, hour=17, minute=36)
        self._record_list.append(Record(dt))

        self._record_list.sort()
        self.assertEqual(
            '[23.01.2021 17:36:00] <no tag>\n'
            '[23.01.2021 17:37:00] <no tag>',
            str(self._record_list),
        )

    def test_sort_is_active(self):
        dt = datetime(year=2021, month=1, day=23, hour=17, minute=36)
        self._record_list.append(Record(dt, is_active=True))  # start
        dt = datetime(
            year=2021, month=1, day=23, hour=17, minute=36, microsecond=1)
        self._record_list.append(Record(dt, tag_id=1, is_active=False))  # end

        self._record_list.sort()
        self.assertEqual(
            '[23.01.2021 17:36:00] <test tag: end>\n'
            '[23.01.2021 17:36:00] <no tag: start>',
            str(self._record_list),
        )

    def test_sort_is_active_none(self):
        dt = datetime(year=2021, month=1, day=23, hour=18, minute=6)
        self._record_list.append(Record(dt, is_active=True))  # start
        dt = datetime(
            year=2021, month=1, day=23, hour=18, minute=6, microsecond=1)
        self._record_list.append(Record(dt, tag_id=1))

        self._record_list.sort()
        self.assertEqual(
            '[23.01.2021 18:06:00] <test tag>\n'
            '[23.01.2021 18:06:00] <no tag: start>',
            str(self._record_list),
        )

    def test_db(self):
        dt = datetime(year=2021, month=1, day=15, hour=21, minute=13)
        r = Record(dt, note='test')
        self._record_list.append(r)
        db.save()
        db.clear()

        db.load()
        record_list = RecordList()
        self.assertEqual(
            '[15.01.2021 21:13:00] <no tag> test', str(record_list))

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestSpellChecker(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        self._sc = SpellChecker()

    def test_empty(self):
        with self.assertRaises(Exception):
            self._sc.check_note('test')

    def test_update(self):
        self._sc.check_note('test', update=True)

    def test_db(self):
        self._sc.check_note('test', update=True)
        db.load()
        with self.assertRaises(Exception):
            self._sc.check_note('test')

        self._sc.check_note('test', update=True)
        db.save()
        db.clear()

        db.load()
        sc = SpellChecker()
        sc.check_note('test')

    def tearDown(self) -> None:
        db.clear()
        db.save()


@unittest.skip
class TestRecordManager(unittest.TestCase):
    def test_add(self):
        rm = RecordManager()
        dt = datetime(year=2021, month=1, day=21, hour=21, minute=15)
        rm.add_record(dt, tag='tag', note='note')
        self.assertEqual(
            '[21.01.2021 21:15:00] <tag> note\n', str(rm.get_record_list()))


if __name__ == '__main__':
    unittest.main()
