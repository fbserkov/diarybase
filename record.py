from datetime import datetime
from typing import Optional

from tagdict import TagDict
from datetime_format import datetime_to_str

tag_dict = TagDict()


class Record:
    def __init__(
            self, dt: Optional[datetime] = None, tag_id: int = 0,
            is_active: Optional[bool] = None, note: str = '',
    ):
        self._dt = dt if dt else datetime.now()
        self._tag_id = tag_id
        self._note = note
        self._is_active = is_active

    def __eq__(self, other):
        return (
            self._dt == other.get_dt() and
            self._tag_id == other.get_tag_id() and
            self._note == other.get_note()
        )

    def __str__(self):
        result = '[' + datetime_to_str(self._dt) + ']'
        result += ' <' + self._tag_id_and_is_active_to_str() + '>'
        if self._note:
            result += ' ' + self._note
        return result

    def _tag_id_and_is_active_to_str(self):
        result = tag_dict[self._tag_id]
        if self._is_active is None:
            return result
        if self._is_active:
            return result + ': start'
        return result + ': end'

    def get_dt(self) -> datetime:
        return self._dt

    def get_tag_id(self) -> int:
        return self._tag_id

    def set_tag_id(self, _id: int) -> None:
        self._tag_id = _id

    def get_note(self) -> str:
        return self._note

    def is_active(self) -> Optional[bool]:
        return self._is_active
