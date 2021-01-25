from datageter import DataGetter


class TagDict(DataGetter):
    def __init__(self):
        DataGetter.__init__(self)
        self._data_key = 'tags'
        self._data_type = dict

    def __getitem__(self, item: int) -> str:
        try:
            return self._get_data()[item]
        except KeyError:
            return 'KeyError: ' + str(item)

    def add(self, tag: str) -> int:
        if self._tag_is_exist(tag):
            _id = self.get_id(tag)
        else:
            tags = self._get_data()
            _id = len(tags)
            tags[_id] = tag
        return _id

    def get_id(self, tag):
        for _id, _tag in self._get_data().items():
            if tag == _tag:
                return _id
        return 0

    def _tag_is_exist(self, tag) -> bool:
        tags: dict = self._get_data()
        return tag in tags.values()
