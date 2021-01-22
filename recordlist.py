from database import db
from record import Record

from tags import TAGS


class RecordList:
    def __init__(self, str_len: int = 100):
        self._str_len = str_len
        self._records = []

    def __len__(self):
        return len(self._records)

    def __str__(self):
        str_records = self._records[-self._str_len:]
        result = '\n'.join(record.to_str(TAGS) for record in str_records)
        return self._get_len_prompt(result)

    def _get_len_prompt(self, result) -> str:
        length = len(self._records)
        if self._str_len < length:
            return result + f'\nlast {self._str_len} from {length}'
        return result

    def append(self, r: Record):
        self._records.append(r)

    def load(self):
        self._records = db.load('records')

    def save(self):
        db.save('records', self._records)
