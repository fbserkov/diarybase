import tkinter as tk
from typing import Optional

from guimanager import GUIManager


class MenuFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side=tk.LEFT)
        tk.Button(self, text='DEL', command=self._delete_callback).pack()
        tk.Button(self, text='INIT', command=self._update_callback).pack()

    @staticmethod
    def _delete_callback() -> None:
        index = record_list_frame.get_index()
        if index == -1:
            return
        gui_manager.delete_record(index)
        record_list_frame.update_listbox()
        record_list_frame.move_view_to_end()

    @staticmethod
    def _update_callback():
        record_list_frame.current_tag = None
        record_list_frame.update_listbox()
        record_list_frame.move_view_to_end()


class RecordListFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side=tk.RIGHT)
        self.current_tag = None

        frame = tk.Frame(self)
        frame.pack()
        self._listbox_var = tk.StringVar(frame)
        self._listbox = tk.Listbox(
            frame, width=80, height=20, listvariable=self._listbox_var)
        self._listbox.bind('<<ListboxSelect>>', self.select_callback)
        self._listbox.pack(side=tk.LEFT)
        sb = tk.Scrollbar(frame, command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self._index_list = None
        self.update_listbox()
        self.move_view_to_end()

    def update_listbox(self, tag: Optional[str] = None):
        if tag:
            self.current_tag = tag
        self._index_list, value = gui_manager.str_record_list(self.current_tag)
        self._listbox.selection_clear(0, tk.END)
        self._listbox_var.set(value)
        if not tag:
            record_frame.init()

    def move_view_to_end(self):
        self._listbox.yview_moveto(fraction=1)

    def select_callback(self, _):
        index = self.get_index()
        if index != -1:
            record_frame.split_record(index)

    def get_index(self) -> int:
        curselection = self._listbox.curselection()
        if curselection:
            return self._index_list[curselection[0]]
        return -1


class RecordFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side=tk.BOTTOM)

        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT)
        self._dt_var = tk.StringVar(frame)
        tk.Entry(frame, width=20, textvariable=self._dt_var).pack()
        self._tag_selector = TagSelector(frame)
        self._tag_selector.pack()
        self.is_active_frame = IsActiveFrame(frame)
        self.is_active_frame.pack()

        self._text = tk.Text(self, width=40, height=4)
        self._text.pack(side=tk.LEFT)

        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT)
        self._update_var = tk.IntVar(self)
        tk.Checkbutton(frame, text='update', variable=self._update_var).pack()
        tk.Button(frame, text='Save', command=self._save_callback).pack()

    def init(self):
        self._dt_var.set('')
        self._tag_selector.set('')
        self.is_active_frame.init()
        self._text.delete('1.0', tk.END)
        self._update_var.set(0)

    def split_record(self, index: int) -> None:
        dt, tag, is_active, note = gui_manager.split_record(index)
        self._dt_var.set(dt)
        self._tag_selector.set(tag)
        self.is_active_frame.set(is_active)
        self._text.delete('1.0', tk.END)
        self._text.insert('1.0', note)

    def _save_callback(self) -> None:
        index = record_list_frame.get_index()
        self._add_record() if index == -1 else self._update_record(index)

    def _add_record(self) -> None:
        exc = gui_manager.add_record(
            str_dt=self._dt_var.get(),
            tag=self._tag_selector.get(),
            is_active=self.is_active_frame.get(),
            note=self._text.get('1.0', tk.END + '-1c'),
            update=self._update_var.get(),
        )
        if exc:
            self._text.insert('1.0', exc)
        else:
            record_list_frame.update_listbox()
            record_list_frame.move_view_to_end()

    def _update_record(self, index: int) -> None:
        exc = gui_manager.update_record(
            index, str_dt=self._dt_var.get(),
            tag=self._tag_selector.get(),
            is_active=self.is_active_frame.get(),
            note=self._text.get('1.0', tk.END + '-1c'),
            update=self._update_var.get(),
        )
        if exc:
            self._text.insert('1.0', exc)
        else:
            record_list_frame.update_listbox()


class TagSelector(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._tag_var = tk.StringVar(self)
        _om = tk.OptionMenu(
            self, self._tag_var, *gui_manager.get_tags(),
            command=lambda _: record_list_frame.update_listbox(
                self._tag_var.get()),
        )
        _om.configure(width=20)
        _om.pack()

    def set(self, tag):
        self._tag_var.set(tag)

    def get(self):
        return self._tag_var.get()


class IsActiveFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.start_var = tk.IntVar(self)
        self.end_var = tk.IntVar(self)
        tk.Checkbutton(
            self, text='start', variable=self.start_var,
            command=lambda: self.end_var.set(0),
        ).pack(side=tk.LEFT)
        tk.Checkbutton(
            self, text='end', variable=self.end_var,
            command=lambda: self.start_var.set(0),
        ).pack(side=tk.LEFT)

    def init(self):
        self.start_var.set(0)
        self.end_var.set(0)

    def set(self, is_active: Optional[bool]):
        if is_active:
            self.start_var.set(1)
            self.end_var.set(0)
        elif is_active is None:
            self.start_var.set(0)
            self.end_var.set(0)
        else:
            self.start_var.set(0)
            self.end_var.set(1)

    def get(self) -> Optional[bool]:
        if self.start_var.get():
            return True
        if self.end_var.get():
            return False


root = tk.Tk()
gui_manager = GUIManager()

record_frame = RecordFrame(root)
record_list_frame = RecordListFrame(root)
MenuFrame(root)

root.mainloop()
