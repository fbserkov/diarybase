from datetime import datetime
from typing import List, Optional, Tuple

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

    def update_record(
            self, index: int, dt: Optional[datetime], tag: str,
            is_active: Optional[bool], note: str,
            update: bool = False,
    ):
        tag_id = self._tag_to_tag_id(tag)
        self.word_set.check_note(note, update)
        self.record_list[index] = Record(dt, tag_id, is_active, note)

    def _tag_to_tag_id(self, tag) -> int:
        return self.tag_dict.get_id(tag)

    def tag_stat(self) -> str:
        tag_id_stat = self.record_list.get_tag_id_stat()
        for tag_id in self.tag_dict:
            if tag_id not in tag_id_stat:
                tag_id_stat[tag_id] = 0
        result = [(v, self.tag_dict[k]) for k, v in tag_id_stat.items()]
        result.sort(reverse=True)
        return '\n'.join(f'{item[0]} {item[1]}' for item in result)

    def set_tag_id(self, new_id: int, tag: str):
        old_id = self.tag_dict.set_id(new_id, tag)
        self.record_list.swap_tag_id(old_id, new_id)

    def tag_filter(
            self, tag: Optional[str] = None) -> Tuple[List[int], List[str]]:
        if tag is None:
            return (
                list(range(len(self.record_list))),
                [str(record) for record in self.record_list],
            )
        else:
            return self.record_list.filter_record(
                tag_id=self.tag_dict.get_id(tag))
