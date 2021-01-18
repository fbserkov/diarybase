from datetime import datetime
from typing import Optional

from tags import TAGS


class Record:
    def __init__(
            self, dt: Optional[datetime] = None, tag_id: int = 0,
            is_active: Optional[bool] = None, note: str = '',
    ):
        self._dt = dt if dt else datetime.now()
        self._tag_id = tag_id
        self._note = note
        self._is_active = is_active

    def __str__(self):
        result = '[' + self._dt_to_str() + ']'
        result += ' (' + self._tag_id_and_is_active_to_str() + ')'
        if self._note:
            result += ' ' + self._note
        return result

    def _dt_to_str(self):
        return self._dt.strftime('%d.%m.%Y %H:%M:%S')

    def _tag_id_and_is_active_to_str(self):
        result = TAGS[self._tag_id]
        if self._is_active is None:
            return result
        if self._is_active:
            return result + ': start'
        return result + ': end'
