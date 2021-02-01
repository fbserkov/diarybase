from typing import List, Optional, Tuple

from const import TEXT_TAG_IS_ACTIVE
from database import db
from datetime_format import datetime_to_str, str_to_datetime
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
            (
                text, lambda t=tag, ia=is_active:
                self.add_record(t, ia),
            )
            for text, tag, is_active in TEXT_TAG_IS_ACTIVE
        )

    @load_and_save
    def get_tags(self):
        items = self._diary_manager.tag_dict.get_sorted_items()
        return (tag for _, tag in items)

    @load_and_save
    def add_record(
            self, tag: str = '', is_active: Optional[bool] = None,
            note: str = '', update=False,
    ) -> Optional[Exception]:
        try:
            self._diary_manager.add_record(
                tag=tag, is_active=is_active, note=note, update=update)
        except Exception as exc:
            return exc

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
    def split_record(self, index: int) -> Tuple[str, str, Optional[bool], str]:
        record = self._diary_manager.record_list[index]
        tag_id = record.get_tag_id()
        return (
            datetime_to_str(record.get_dt()),
            self._diary_manager.tag_dict[tag_id],
            record.is_active(),
            record.get_note(),
        )

    @load_and_save
    def update_record(
            self, index: int, str_dt: str, tag: str,
            is_active: Optional[bool], note: str, update=False,
    ) -> Optional[Exception]:
        if str_dt:
            try:
                dt = str_to_datetime(str_dt)
            except Exception as exc:
                return exc
        else:
            dt = None
        try:
            self._diary_manager.update_record(
                index, dt, tag, is_active, note, update)
        except Exception as exc:
            return exc
