from datetime import datetime
from typing import Optional

TAGS = {0: 'not specified'}


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
        str_dt = self._dt.strftime('%d.%m.%Y %H:%M:%S')
        return f'[{str_dt}] ({TAGS[self._tag_id]}) ' + self._note
