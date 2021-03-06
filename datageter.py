from database import db


class DataGetter:
    def __init__(self):
        self._data_key = None
        self._data_type = None

    def __iter__(self):
        return iter(self._get_data())

    def _get_data(self):
        if not (self._data_key and self._data_type):
            raise Exception
        try:
            return db[self._data_key]
        except KeyError:
            db[self._data_key] = self._data_type()
            return db[self._data_key]
