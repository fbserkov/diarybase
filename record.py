from datetime import datetime


class Record:
    def __init__(self, dt=None, text=None):
        self._dt = dt if dt else datetime.now()
        self._text = text

    def __str__(self):
        str_dt = self._dt.strftime('%d.%m.%Y %H:%M:%S')
        return f'[{str_dt}] ' + self._text
