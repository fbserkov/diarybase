class TagDict:
    def __init__(self, db):
        self._db = db
        self._tags = {}

    def load(self):
        self._tags = self._db.load('tags')

    def save(self):
        self._db.save('tags', self._tags)
