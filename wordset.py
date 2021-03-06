from datageter import DataGetter


class WordSet(DataGetter):
    def __init__(self):
        DataGetter.__init__(self)
        self._data_key = 'words'
        self._data_type = set

    def check_note(self, note: str, update=False):
        words: set = self._get_data()
        result = self._get_note_set(note) - words
        if result:
            if update:
                words.update(result)
            else:
                raise Exception(result)

    def _get_note_set(self, note):
        result = set()
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
