from typing import List, Tuple

from const import TEXT_AND_TAG
from database import db
from datetime_format import datetime_to_str
from diarymanager import DiaryManager


def load_and_save(to_wrap):
    def wrapper(*args, **kwargs):
        db.load()
        result = to_wrap(*args, **kwargs)
        db.save()
        return result
    return wrapper


class GUIManager:
    def __init__(self):
        self._diary_manager = DiaryManager()
        self.text_and_command_list = (
            (text, lambda name=tag: self.add_record_is_active_none(name))
            for text, tag in TEXT_AND_TAG
        )

    @load_and_save
    def add_record_is_active_none(self, name: str) -> None:
        self._diary_manager.add_record(tag=name)

    @load_and_save
    def delete_last_record(self) -> None:
        self._diary_manager.record_list.delete_last_record()

    @load_and_save
    def str_record_list(self) -> List[str]:
        result = []
        for record in self._diary_manager.record_list:
            result.append(str(record))
        return result

    @load_and_save
    def split_record(self, index: int) -> Tuple[str, str, str]:
        record = self._diary_manager.record_list[index]
        tag_id = record.get_tag_id()
        return (
            datetime_to_str(record.get_dt()),
            self._diary_manager.tag_dict[tag_id],
            record.get_note(),
        )

    @load_and_save
    def update_record(self, index: int, note: str) -> None:
        record = self._diary_manager.record_list[index]
        record.set_note(note)
