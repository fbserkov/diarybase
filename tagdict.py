from database import db


class TagDict:
    # @staticmethod
    # def set_dict(tags: dict):
    #     db.set('tags', tags)

    @staticmethod
    def get_dict() -> dict:
        try:
            return db.get('tags')
        except KeyError:
            db.set('tags', {})
            return db.get('tags')

    def add(self, tag: str):
        tags = self.get_dict()
        tags[len(tags)] = tag
