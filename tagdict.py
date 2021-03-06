from typing import List, Tuple

from datageter import DataGetter


class TagDict(DataGetter):
    def __init__(self) -> None:
        DataGetter.__init__(self)
        self._data_key = 'tags'
        self._data_type = dict

    def __getitem__(self, item: int) -> str:
        try:
            return self._get_data()[item]
        except KeyError:
            return 'KeyError: ' + str(item)

    def __str__(self) -> str:
        return '\n'.join(
            f'{_id}) {tag}' for _id, tag in self.get_sorted_items())

    def get_sorted_items(self) -> List[Tuple[int, str]]:
        return sorted(
            self._get_data().items(),
            key=lambda item: item[1].lower(),
        )

    def add(self, tag: str) -> int:
        _id = self.get_id(tag)
        if _id == -1:
            _id = self._get_next_id()
            self._get_data()[_id] = tag
        return _id

    def rename(self, tag: str, name: str) -> None:
        _id = self.get_id(tag)
        if _id != -1:
            tags: dict = self._get_data()
            tags[_id] = name

    def delete(self, tag: str) -> None:
        _id = self.get_id(tag)
        if _id != -1:
            tags: dict = self._get_data()
            tags.pop(_id)

    def set_id(self, new_id: int, tag: str) -> int:
        tags: dict = self._get_data()
        old_id = self.get_id(tag)
        if old_id == -1:
            old_id = self.add(tag)
            self.set_id(new_id, tag)
        elif new_id in tags:
            tags[new_id], tags[old_id] = tag, tags[new_id]
        else:
            self.delete(tag)
            tags[new_id] = tag
        return old_id

    def get_id(self, tag: str) -> int:
        for _id, _tag in self._get_data().items():
            if tag == _tag:
                return _id
        return -1

    def _get_next_id(self) -> int:
        tags: dict = self._get_data()
        count = 0
        while True:
            if count not in tags:
                return count
            count += 1
