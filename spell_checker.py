from database import Database
from recordlist import RecordList


def main():
    db = Database('main.db')
    storage = RecordList(db)
    storage.load()
    records_spellchecking(storage)


def records_spellchecking(storage):
    dic = get_dic_set()
    records = get_records_set(storage)
    print(records - dic)


def record_spellchecking(record):
    dic = get_dic_set()
    record = get_record_set(record)
    if record - dic:
        raise Exception(record - dic)


def get_dic_set():
    with open('dic.txt') as file:
        return {word.rstrip() for word in file.readlines()}


def get_records_set(storage):
    result = set()
    for record in storage._records:
        result.update(get_record_set(record))
    return result


def get_record_set(record):
    result = set()
    note = record.get_note()
    if not note:
        return result

    note = filter_characters(note.lower())
    for word in note.split(' '):
        if word and not word.isdigit():
            result.add(word)
    return result


def filter_characters(note):
    for character in '!"$%()+,-./:;=>?°€№⅓❤':
        note = note.replace(character, ' ')
    return note


if __name__ == '__main__':
    main()
