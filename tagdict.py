from database import db


class TagDict:
    def __init__(self):
        self._tags = {}

    def load(self):
        self._tags = db.load('tags')

    def save(self):
        db.save('tags', self._tags)

    def set_dict(self, tags: dict):
        self._tags = tags

    def get_dict(self) -> dict:
        return self._tags

    def add(self, tag: str):
        self._tags[len(self._tags)] = tag
