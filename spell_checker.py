def check_note(note):
    result = _get_note_set(note) - _get_dic_set()
    if result:
        raise Exception(result)


def _get_dic_set():
    with open('dic.txt') as file:
        return {word.rstrip() for word in file.readlines()}


def _get_note_set(note):
    result = set()
    if not note:
        return result

    note = _filter_characters(note.lower())
    for word in note.split(' '):
        if word and not word.isdigit():
            result.add(word)
    return result


def _filter_characters(note):
    for character in '!"$%()+,-./:;=>?°€№⅓❤':
        note = note.replace(character, ' ')
    return note
