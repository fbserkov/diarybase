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

    def __iter__(self):
        return iter(self._get_data())

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

    def append(self, r: Record):
        self._get_data().append(r)

    def delete_last_record(self):
        self._get_data().pop()

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
