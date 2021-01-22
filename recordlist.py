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
