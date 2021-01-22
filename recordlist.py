from database import db
from record import Record


class RecordList:
    def __init__(self, str_len: int = 100):
        self._str_len = str_len
        self._records = []

    def __len__(self):
        return len(self._records)

    def __str__(self):
        str_records = self._records[-self._str_len:]
        self._append_len_prompt(str_records)
        return '\n'.join(str(record) for record in str_records)

    def _append_len_prompt(self, str_records):
        length = len(self._records)
        if self._str_len < length:
            str_records.append(f'last {self._str_len} from {length}')

    def append(self, r: Record):
        self._records.append(r)

    def load(self):
        self._records = db.load('records')

    def save(self):
        db.save('records', self._records)
