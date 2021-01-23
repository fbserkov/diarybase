from datetime import timedelta

from database import db
from record import Record

from tags import TAGS


class RecordList:
    def __init__(self, str_len: int = 500):
        self._str_len = str_len

    def __len__(self):
        return len(db.get_records())

    def __str__(self):
        last_records = db.get_records()[-self._str_len:]
        result = '\n'.join(record.to_str(TAGS) for record in last_records)
        return self._get_len_prompt(result)

    def _get_len_prompt(self, result) -> str:
        length = len(db.get_records())
        if self._str_len < length:
            return result + f'\nlast {self._str_len} from {length}'
        return result

    @staticmethod
    def append(r: Record):
        db.get_records().append(r)

    def sort(self):
        records = db.get_records()
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
