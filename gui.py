import tkinter as tk
from typing import Optional

from const import DELETE, SAVE, UPDATE
from guimanager import GUIManager


def add_update_call(to_wrap):
    def wrapper():
        to_wrap()
        record_list_frame.update_record_list()
    return wrapper


class MenuFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side=tk.LEFT)

        for text, command in gui_manager.text_and_command_list:
            tk.Button(self, text=text, command=add_update_call(command)).pack()
        tk.Button(
            self, text=DELETE,
            command=add_update_call(gui_manager.delete_last_record),
        ).pack()
        tk.Button(
            self, text=UPDATE,
            command=record_list_frame.update_record_list,
        ).pack()


class RecordListFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        self._listbox_var = tk.StringVar(frame)
        self.listbox = tk.Listbox(
            frame, width=80, listvariable=self._listbox_var)
        self.listbox.bind('<<ListboxSelect>>', self.select_callback)
        self.listbox.pack(side=tk.LEFT)
        sb = tk.Scrollbar(frame, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.update_record_list()

    def update_record_list(self):
        self._listbox_var.set(gui_manager.str_record_list())
        self.listbox.yview_moveto(fraction=1)

    @staticmethod
    def select_callback(event):
        curselection = event.widget.curselection()
        if curselection:
            record_frame.split_record(curselection[0])


class RecordFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(side=tk.BOTTOM)

        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT)
        self._dt_var = tk.StringVar(frame)
        self._tag_var = tk.StringVar(frame)
        tk.Entry(frame, width=20, textvariable=self._dt_var).pack()
        tk.Entry(frame, width=20, textvariable=self._tag_var).pack()
        self.is_active_frame = IsActiveFrame(frame)
        self.is_active_frame.pack()

        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT)
        self._text = tk.Text(frame, width=40, height=4)
        self._text.pack(side=tk.LEFT)
        tk.Button(
            frame, text=SAVE,
            command=add_update_call(self._save_record),
        ).pack(side=tk.LEFT)

    def split_record(self, index):
        dt, tag, is_active, note = gui_manager.split_record(index)
        self._dt_var.set(dt)
        self._tag_var.set(tag)
        self.is_active_frame.set(is_active)
        self._text.delete('1.0', tk.END)
        self._text.insert('1.0', note)

    def _save_record(self):
        curselection = record_list_frame.listbox.curselection()
        if curselection:
            error = not gui_manager.update_record(
                index=curselection[0],
                str_dt=self._dt_var.get(),
                tag=self._tag_var.get(),
                is_active=self.is_active_frame.get(),
                note=self._text.get('1.0', tk.END + '-1c'),
            )
            if error:
                self._text.insert('1.0', 'ValueError\n')
        else:
            gui_manager.add_record(
                tag=self._tag_var.get(),
                note=self._text.get('1.0', tk.END + '-1c'),
            )


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
