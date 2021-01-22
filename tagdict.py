from database import db


class TagDict:
    @staticmethod
    def set_dict(tags: dict):
        db.set_tags(tags)

    @staticmethod
    def get_dict() -> dict:
        return db.get_tags()

    @staticmethod
    def add(tag: str):
        tags = db.get_tags()
        tags[len(tags)] = tag
