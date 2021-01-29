from database import db
from diarymanager import DiaryManager


def load_and_save(to_wrap):
    def wrapper(*args):
        db.load()
        result = to_wrap(*args)
        db.save()
        return result
    return wrapper


class GUIManager:
    def __init__(self):
        self.diary_manager = DiaryManager()
        self.diary_manager.record_list.set_str_len(100)

    @load_and_save
    def add_record(self):
        self.diary_manager.add_record()

    @load_and_save
    def delete_last_record(self):
        self.diary_manager.record_list.delete_last_record()

    @load_and_save
    def str_record_list(self) -> str:
        return str(self.diary_manager.record_list)
