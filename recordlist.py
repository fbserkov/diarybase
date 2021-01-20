from pickle import dump, load

from record import Record


class RecordList:
    def __init__(self, filename, str_len=100):
        self._filename = filename
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

    def save(self):
        with open(self._filename, 'wb') as file:
            dump(self._records, file)

    def load(self):
        with open(self._filename, 'rb') as file:
            self._records = load(file)
