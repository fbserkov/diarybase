class Note:
    def __init__(self, text):
        self._text = text

    def __str__(self):
        return self._text

    def __eq__(self, other):
        return self._text == str(other)
