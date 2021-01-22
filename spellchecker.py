from database import db


class SpellChecker:
    def check_note(self, note: str, update=False):
        result = self._get_note_set(note) - db.get_words()
        if result:
            if update:
                db.get_words().update(result)
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
