from datetime import timedelta

from datageter import DataGetter
from record import Record


class RecordList(DataGetter):
    def __init__(self, str_len: int = 500):
        DataGetter.__init__(self)
        self._data_key = 'records'
        self._data_type = list
        self._str_len = str_len

    def __getitem__(self, item):
        return self._get_data()[item]

    def __len__(self):
        return len(self._get_data())

    def __str__(self):
        last_records = self._get_data()[-self._str_len:]
        result = '\n'.join(str(record) for record in last_records)
        return self._get_len_prompt(result)

    def _get_len_prompt(self, result) -> str:
        length = len(self._get_data())
        if self._str_len < length:
            return result + f'\nlast {self._str_len} from {length}'
        return result

    def set_str_len(self, str_len: int):
        self._str_len = str_len

    def append(self, r: Record):
        self._get_data().append(r)

    def delete_last_record(self):
        self._get_data().pop()

    def replace_note(self, num_from_end: int, note: str):
        record = self._get_data()[-num_from_end]
        record.set_note(note)

    def swap_tag_id(self, id_1, id_2):
        for record in self:
            if record.get_tag_id() == id_1:
                record.set_tag_id(id_2)
            elif record.get_tag_id() == id_2:
                record.set_tag_id(id_1)

    def get_tag_id_stat(self) -> dict:
        result = {}
        for record in self:
            tag_id = record.get_tag_id()
            result[tag_id] = result[tag_id] + 1 if tag_id in result else 1
        return result

    def sort(self):
        records = self._get_data()
        records.sort(key=lambda r: (
            self._round_to_seconds_tenths(r), self._none_is_false(r)))

    @staticmethod
    def _round_to_seconds_tenths(record):
        dt = record.get_dt()
        td = timedelta(microseconds=dt.microsecond % 100000)
        return dt - td

    @staticmethod
    def _none_is_false(record):
        if record.is_active():
            return True
        return False

    def filter_record(self, **kwargs) -> str:
        records = self._filter(**kwargs)
        return '\n'.join(str(r) for r in records)

    def _filter(self, **kwargs):
        for record in self._get_data():
            if self._is_filtered(record, **kwargs):
                yield record

    @staticmethod
    def _is_filtered(r: Record, **kwargs) -> bool:
        if 'tag_id' in kwargs:
            if r.get_tag_id() != kwargs['tag_id']:
                return False
        if 'fragment' in kwargs:
            note = r.get_note()
            if not note:
                return False
            if kwargs['fragment'] not in note:
                return False
        return True
