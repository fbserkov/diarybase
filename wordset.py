from datageter import DataGetter


class WordSet(DataGetter):
    def __init__(self):
        DataGetter.__init__(self)
        self._data_type = set
        self._data_key = 'words'

    def check_note(self, note: str, update=False):
        result = self._get_note_set(note) - self._get_data()
        if result:
            if update:
                self._get_data().update(result)
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
