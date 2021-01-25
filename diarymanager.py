from datetime import datetime
from typing import Optional

from record import Record
from recordlist import RecordList
from tagdict import TagDict


class DiaryManager:
    def __init__(self):
        self._tag_dict = TagDict()
        self._record_list = RecordList()

    def get_record_list(self):
        return self._record_list

    def add_record(
            self, dt: Optional[datetime] = None, tag: str = '',
            is_active: Optional[bool] = None, note: str = '',
    ):
        tag_id = self._tag_to_tag_id(tag)
        self._record_list.append(Record(dt, tag_id, is_active))

    def _tag_to_tag_id(self, tag) -> int:
        return self._tag_dict.get_id(tag)
