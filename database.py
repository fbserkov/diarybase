from datetime import datetime


class Database:
    _texts = {}

    @staticmethod
    def set(dt: datetime, text):
        Database._texts[dt] = text

    @staticmethod
    def get(dt: datetime):
        return Database._texts[dt]
