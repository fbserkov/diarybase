from datageter import DataGetter


class TagDict(DataGetter):
    def __init__(self):
        DataGetter.__init__(self)
        self._data_key = 'tags'
        self._data_type = dict

    def __getitem__(self, item):
        return self._get_data()[item]

    def add(self, tag: str):
        tags = self._get_data()
        tags[len(tags)] = tag

    def get_id(self, tag):
        for _id, _tag in self._get_data().items():
            if tag == _tag:
                return _id
        return 0
