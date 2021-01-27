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

    def test_delete(self):
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual(1, self._tag_dict.add('test tag'))

        self.assertEqual('test tag', self._tag_dict[1])
        self._tag_dict.delete('test tag')
        self.assertEqual('KeyError: 1', self._tag_dict[1])

    def test_add_after_delete(self):
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual(1, self._tag_dict.add('first tag'))
        self.assertEqual(2, self._tag_dict.add('second tag'))

        self._tag_dict.delete('first tag')
        self.assertEqual(1, self._tag_dict.add('third tag'))

    def test_get_id(self):
        self.assertEqual(-1, self._tag_dict.get_id('no tag'))
        self.assertEqual(-1, self._tag_dict.get_id('test tag'))
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self.assertEqual(1, self._tag_dict.add('test tag'))
        self.assertEqual(0, self._tag_dict.get_id('no tag'))
        self.assertEqual(1, self._tag_dict.get_id('test tag'))

    def test_set_id(self):
        self._tag_dict.set_id(10, 'first tag')  # not used, not exist
        self.assertEqual('first tag', self._tag_dict[10])

        self._tag_dict.set_id(20, 'first tag')  # not used, tag is exist
        self.assertEqual('KeyError: 10', self._tag_dict[10])
        self.assertEqual('first tag', self._tag_dict[20])

        self._tag_dict.set_id(20, 'second tag')  # id is used, not exist
        self.assertEqual('second tag', self._tag_dict[20])
        self.assertEqual('first tag', self._tag_dict[0])

        self._tag_dict.set_id(20, 'first tag')  # id is used, tag is exist
        self.assertEqual('first tag', self._tag_dict[20])
        self.assertEqual('second tag', self._tag_dict[0])

    def test_rename(self):
        self.assertEqual(0, self._tag_dict.add('no tag'))
        self._tag_dict.rename('no tag', 'No tag!')
        self.assertEqual(0, self._tag_dict.get_id('No tag!'))

    def test_str(self):
        self._tag_dict.add('tag C')
        self._tag_dict.add('tag b')
        self._tag_dict.add('tag A')
        self.assertEqual(
            '2) tag A\n'
            '1) tag b\n'
            '0) tag C',
            str(self._tag_dict),
        )

    def test_save_and_load(self):
        self._tag_dict.add('no tag')
        self._tag_dict.add('test tag')
        db.save()
        db.clear()

        db.load()
        td = TagDict()
        self.assertEqual(
            '0) no tag\n'
            '1) test tag',
            str(td),
        )

    def tearDown(self) -> None:
        db.clear()
        db.save()


class TestRecord(unittest.TestCase):
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
        self.assertEqual(dt, r.get_dt())
        self.assertEqual('[18.01.2021 18:26:00] <no tag>', str(r))

    def test_tag_id(self):
        dt = datetime(year=2021, month=1, day=18, hour=18, minute=40)
        r = Record(dt, tag_id=1)
        self.assertEqual(1, r.get_tag_id())
        self.assertEqual('[18.01.2021 18:40:00] <test tag>', str(r))
        r.set_tag_id(0)
        self.assertEqual('[18.01.2021 18:40:00] <no tag>', str(r))

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
        self.assertEqual('test', r.get_note())
        self.assertEqual('[18.01.2021 11:11:00] <no tag> test', str(r))
        r.set_note('Test!')
        self.assertEqual('[18.01.2021 11:11:00] <no tag> Test!', str(r))

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
        dt = datetime(year=2021, month=1, day=19, hour=19, minute=38)
        for _ in range(10):
            self._record_list.append(Record(dt, note='test'))

        self._record_list.set_str_len(5)
        self.assertEqual(
            '[19.01.2021 19:38:00] <no tag> test\n' * 5 +
            'last 5 from 10',
            str(self._record_list),
        )
        self._record_list.set_str_len(50)
        self.assertEqual(
            '[19.01.2021 19:38:00] <no tag> test\n' * 9 +
            '[19.01.2021 19:38:00] <no tag> test',
            str(self._record_list),
        )

    def test_delete_last_record(self):
        dt = datetime(year=2021, month=1, day=25, hour=16, minute=21)
        self._record_list.append(Record(dt, note='first'))
        dt = datetime(year=2021, month=1, day=25, hour=16, minute=23)
        self._record_list.append(Record(dt, note='second'))

        self.assertEqual(
            '[25.01.2021 16:21:00] <no tag> first\n'
            '[25.01.2021 16:23:00] <no tag> second',
            str(self._record_list),
        )
        self._record_list.delete_last_record()
        self.assertEqual(
            '[25.01.2021 16:21:00] <no tag> first',
            str(self._record_list),
        )

    def test_replace_note(self):
        dt = datetime(year=2021, month=1, day=25, hour=19, minute=47)
        self._record_list.append(Record(dt, note='first'))
        dt = datetime(year=2021, month=1, day=25, hour=19, minute=47)
        self._record_list.append(Record(dt, note='second'))

        self.assertEqual(
            '[25.01.2021 19:47:00] <no tag> first\n'
            '[25.01.2021 19:47:00] <no tag> second',
            str(self._record_list),
        )
        self._record_list.replace_note(num_from_end=1, note='Second!')
        self.assertEqual(
            '[25.01.2021 19:47:00] <no tag> first\n'
            '[25.01.2021 19:47:00] <no tag> Second!',
            str(self._record_list),
        )
        self._record_list.replace_note(num_from_end=2, note='First!')
        self.assertEqual(
            '[25.01.2021 19:47:00] <no tag> First!\n'
            '[25.01.2021 19:47:00] <no tag> Second!',
            str(self._record_list),
        )

    def test_swap_tag_id(self):
        dt = datetime(year=2021, month=1, day=26, hour=21, minute=42)
        self._record_list.append(Record(dt, note='first'))
        dt = datetime(year=2021, month=1, day=26, hour=21, minute=43)
        self._record_list.append(Record(dt, tag_id=1, note='second'))

        self.assertEqual(
            '[26.01.2021 21:42:00] <no tag> first\n'
            '[26.01.2021 21:43:00] <test tag> second',
            str(self._record_list),
        )
        self._record_list.swap_tag_id(0, 1)
        self.assertEqual(
            '[26.01.2021 21:42:00] <test tag> first\n'
            '[26.01.2021 21:43:00] <no tag> second',
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

    def test_note_filter(self):
        dt = datetime(year=2021, month=1, day=25, hour=19, minute=32)
        self._record_list.append(Record(dt, note='ABC'))
        self._record_list.append(Record(dt, note='BCD'))
        self._record_list.append(Record(dt, note='CDA'))

        self.assertEqual(
            '[25.01.2021 19:32:00] <no tag> ABC\n'
            '[25.01.2021 19:32:00] <no tag> CDA',
            self._record_list.note_filter('A'),
        )
        self.assertEqual(
            '[25.01.2021 19:32:00] <no tag> ABC\n'
            '[25.01.2021 19:32:00] <no tag> BCD',
            self._record_list.note_filter('B'),
        )
        self.assertEqual(
            '[25.01.2021 19:32:00] <no tag> ABC\n'
            '[25.01.2021 19:32:00] <no tag> BCD\n'
            '[25.01.2021 19:32:00] <no tag> CDA',
            self._record_list.note_filter('C'),
        )
        self.assertEqual(
            '[25.01.2021 19:32:00] <no tag> BCD\n'
            '[25.01.2021 19:32:00] <no tag> CDA',
            self._record_list.note_filter('D'),
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
            '<KeyError: -1>', str(self._diary_manager.record_list)[22:])

    def test_add_record_dt(self):
        dt = datetime(year=2021, month=1, day=21, hour=21, minute=15)
        self._diary_manager.add_record(dt)
        self.assertEqual(
            '[21.01.2021 21:15:00] <KeyError: -1>',
            str(self._diary_manager.record_list),
        )

    def test_add_record_tag(self):
        self._tag_dict.add('tag')
        dt = datetime(year=2021, month=1, day=25, hour=12, minute=37)
        self._diary_manager.add_record(dt, 'tag')
        self.assertEqual(
            '[25.01.2021 12:37:00] <tag>',
            str(self._diary_manager.record_list),
        )

    def test_add_record_is_active(self):
        self._tag_dict.add('tag')
        dt = datetime(year=2021, month=1, day=25, hour=15, minute=34)
        self._diary_manager.add_record(dt, 'tag', is_active=True)
        dt = datetime(year=2021, month=1, day=25, hour=15, minute=37)
        self._diary_manager.add_record(dt, 'tag', is_active=False)
        self.assertEqual(
            '[25.01.2021 15:34:00] <tag: start>\n'
            '[25.01.2021 15:37:00] <tag: end>',
            str(self._diary_manager.record_list),
        )

    def test_add_record_note(self):
        self._tag_dict.add('tag')
        dt = datetime(year=2021, month=1, day=25, hour=12, minute=39)
        with self.assertRaises(Exception):
            self._diary_manager.add_record(dt, 'tag', note='test note')

        self._diary_manager.add_record(
            dt, 'tag', note='test note', update=True)
        self.assertEqual(
            '[25.01.2021 12:39:00] <tag> test note',
            str(self._diary_manager.record_list),
        )

    def test_replace_note(self):
        dt = datetime(year=2021, month=1, day=25, hour=19, minute=57)
        self._diary_manager.add_record(dt, note='first', update=True)

        self.assertEqual(
            '[25.01.2021 19:57:00] <KeyError: -1> first',
            str(self._diary_manager.record_list),
        )
        with self.assertRaises(Exception):
            self._diary_manager.replace_note(num_from_end=1, note='second')

        self._diary_manager.replace_note(
            num_from_end=1, note='second', update=True)
        self.assertEqual(
            '[25.01.2021 19:57:00] <KeyError: -1> second',
            str(self._diary_manager.record_list),
        )

    def tearDown(self) -> None:
        db.clear()
        db.save()


if __name__ == '__main__':
    unittest.main()
