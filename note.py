class Note:
    def __init__(self, text):
        self._text = text

    def __eq__(self, other):
        return self._text == other.get_text()

    def get_text(self):
        return self._text
