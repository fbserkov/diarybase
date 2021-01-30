from typing import List

from const import TEXT_AND_TAG
from database import db
from diarymanager import DiaryManager
from record import Record


def load_and_save(to_wrap):
    def wrapper(*args):
        db.load()
        result = to_wrap(*args)
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
    def get_record(self, index) -> Record:
        return self._diary_manager.record_list[index]
