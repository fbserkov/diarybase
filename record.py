from datetime import datetime
from typing import Optional

from datetime_format import dt_to_str


class Record:
    def __init__(
            self, dt: Optional[datetime] = None, tag_id: int = 0,
            is_active: Optional[bool] = None, note: str = '',
    ):
        self._dt = dt if dt else datetime.now()
        self._tag_id = tag_id
        self._note = note
        self._is_active = is_active

    def get_dt(self) -> datetime:
        return self._dt

    def get_note(self) -> Optional[str]:
        return self._note

    def set_note(self, note: str) -> None:
        self._note = note

    def is_active(self) -> Optional[bool]:
        return self._is_active

    def to_str(self, tags: dict):
        result = '[' + dt_to_str(self._dt) + ']'
        result += ' <' + self._tag_id_and_is_active_to_str(tags) + '>'
        if self._note:
            result += ' ' + self._note
        return result

    def _tag_id_and_is_active_to_str(self, tags: dict):
        result = tags[self._tag_id]
        if self._is_active is None:
            return result
        if self._is_active:
            return result + ': start'
        return result + ': end'
