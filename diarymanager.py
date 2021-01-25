from record import Record
from recordlist import RecordList


class DiaryManager:
    def __init__(self):
        self._record_list = RecordList()

    def get_record_list(self):
        return self._record_list

    def add_record(self, *args, **kwargs):
        self._record_list.append(Record(*args, **kwargs))

    @staticmethod
    def _tag_to_tag_id(kwargs):
        pass
