from datetime import datetime
from typing import Optional

from record import Record
from recordlist import RecordList
from tagdict import TagDict
from wordset import WordSet


class DiaryManager:
    def __init__(self):
        self.tag_dict = TagDict()
        self.word_set = WordSet()
        self.record_list = RecordList()

    def add_record(
            self, dt: Optional[datetime] = None, tag: str = '',
            is_active: Optional[bool] = None, note: str = '',
            update: bool = False,
    ):
        tag_id = self._tag_to_tag_id(tag)
        self.word_set.check_note(note, update)
        self.record_list.append(Record(dt, tag_id, is_active, note))

    def _tag_to_tag_id(self, tag) -> int:
        return self.tag_dict.get_id(tag)

    def replace_note(self, num_from_end: int, note: str, update=False):
        self.word_set.check_note(note, update)
        self.record_list.replace_note(num_from_end, note)
