import os
import unittest
from datetime import datetime

from database import db
from diarymanager import DiaryManager
from record import Record
from recordlist import RecordList
from tagdict import TagDict
from wordset import WordSet


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        db.load()

    def test_no_file(self):
        os.remove('test.db')
        db.load()

    def test_set_and_get(self):
        key = 'key'
        value = 'value'
        db[key] = value
        self.assertEqual(value, db[key])

    def test_save_and_load(self):
        key = 'key'
        value = 'value'
        db[key] = value
        db.save()
        db.clear()

        with self.assertRaises(KeyError):
            value = db[key]
        db.load()
        self.assertEqual(value, db[key])

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestTagDict(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        self._tag_dict = TagDict()

    def test_getitem(self):
        self.assertEqual('KeyError: 0', self._tag_dict[0])

    def test_add(self):
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual(1, self._tag_dict.add('test tag'))
        self.assertEqual('no tag', self._tag_dict[0])
        self.assertEqual('test tag', self._tag_dict[1])

    def test_add_the_same(self):
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual('no tag', self._tag_dict[0])
        self.assertEqual('KeyError: 1', self._tag_dict[1])

    def test_get_id(self):
        self.assertEqual(0, self._tag_dict.get_id('no tag'))
        self.assertEqual(0, self._tag_dict.get_id('test tag'))
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual(1, self._tag_dict.add('test tag'))
        self.assertEqual(0, self._tag_dict.get_id('no tag'))
        self.assertEqual(1, self._tag_dict.get_id('test tag'))

    def test_save_and_load(self):
        self._tag_dict.add('no tag')
        self._tag_dict.add('test tag')
        db.save()
        db.clear()

        db.load()
        td = TagDict()
        self.assertEqual('no tag', td[0])
        self.assertEqual('test tag', td[1])

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestNote(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        td = TagDict()
        td.add('no tag')
        td.add('test tag')

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
        self.assertEqual(
            '[18.01.2021 18:40:00] <test tag: start>', str(r))
        r = Record(dt, tag_id=1, is_active=False)
        self.assertEqual(
            '[18.01.2021 18:40:00] <test tag: end>', str(r))

    def test_note(self):
        dt = datetime(year=2021, month=1, day=18, hour=11, minute=11)
        r = Record(dt, note='test')
        self.assertEqual('[18.01.2021 11:11:00] <no tag> test', str(r))

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestRecordList(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        td = TagDict()
        td.add('no tag')
        td.add('test tag')
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

    def test_save_and_load(self):
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


class TestWordSet(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        self._word_set = WordSet()

    def test_check_note(self):
        with self.assertRaises(Exception):
            self._word_set.check_note('test')

    def test_check_note_update(self):
        self._word_set.check_note('test', update=True)

    def test_save_and_load(self):
        self._word_set.check_note('test', update=True)
        db.load()
        with self.assertRaises(Exception):
            self._word_set.check_note('test')

        self._word_set.check_note('test', update=True)
        db.save()
        db.clear()

        db.load()
        sc = WordSet()
        sc.check_note('test')

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestDiaryManager(unittest.TestCase):
    def setUp(self) -> None:
        db.load()
        self._tag_dict = TagDict()
        self._diary_manager = DiaryManager()

    def test_add_record(self):
        self._diary_manager.add_record()
        self.assertEqual(
            '<KeyError: 0>', str(self._diary_manager.get_record_list())[22:])

    def test_add_record_dt(self):
        dt = datetime(year=2021, month=1, day=21, hour=21, minute=15)
        self._diary_manager.add_record(dt)
        self.assertEqual(
            '[21.01.2021 21:15:00] <KeyError: 0>',
            str(self._diary_manager.get_record_list()),
        )

    def test_add_record_dt_tag(self):
        self._tag_dict.add('tag')
        dt = datetime(year=2021, month=1, day=25, hour=12, minute=37)
        self._diary_manager.add_record(dt, 'tag')
        self.assertEqual(
            '[25.01.2021 12:37:00] <tag>',
            str(self._diary_manager.get_record_list()),
        )

    def tearDown(self) -> None:
        db.clear()
        db.save()


if __name__ == '__main__':
    unittest.main()
