from database import Database


class SpellChecker:
    def __init__(self, db: Database):
        self._db = db
        self._words = set()

    def load(self):
        self._words = self._db.load('words')

    def save(self):
        self._db.save('words', self._words)

    def check_note(self, note, update=False):
        result = self._get_note_set(note) - self._words
        if result:
            if update:
                self._words.update(result)
            else:
                raise Exception(result)

    def _get_note_set(self, note):
        result = set()
        if not note:
            return result

        note = self._filter_characters(note.lower())
        for word in note.split(' '):
            if word and not word.isdigit():
                result.add(word)
        return result

    @staticmethod
    def _filter_characters(note):
        for character in '!"$%()+,-./:;=>?°€№⅓❤':
            note = note.replace(character, ' ')
        return note
