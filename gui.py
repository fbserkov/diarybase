import tkinter as tk

from const import DELETE, UPDATE
from gui_temp import TEXT, COMMAND
from guimanager import GUIManager


def add_update_call(to_wrap):
    def wrapper():
        to_wrap()
        record_list_frame.update_record_list()
    return wrapper


class MenuFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(self, text=TEXT, command=add_update_call(COMMAND)).pack()
        for t, c in gui_manager.text_and_command_list:
            tk.Button(self, text=t, command=add_update_call(c)).pack()
        tk.Button(
            self, text=DELETE,
            command=add_update_call(gui_manager.delete_last_record),
        ).pack()
        tk.Button(
            self, text=UPDATE,
            command=record_list_frame.update_record_list,
        ).pack()
        self.pack(side=tk.LEFT)


class RecordListFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        frame = tk.Frame(self)
        frame.pack()

        self.listbox_var = tk.StringVar(frame)
        self.listbox = tk.Listbox(
            frame, width=80, listvariable=self.listbox_var)
        self.listbox.bind('<<ListboxSelect>>', self._split_record)
        self.listbox.pack(side=tk.LEFT)

        sb = tk.Scrollbar(frame, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        frame = tk.Frame(self)
        frame.pack()

        self._dt_var = tk.StringVar(frame)
        self._tag_var = tk.StringVar(frame)
        self._note_var = tk.StringVar(frame)
        tk.Entry(frame, width=20, textvariable=self._dt_var).pack(side=tk.LEFT)
        tk.Entry(
            frame, width=20, textvariable=self._tag_var).pack(side=tk.LEFT)
        tk.Entry(
            frame, width=40, textvariable=self._note_var).pack(side=tk.LEFT)

        self.update_record_list()
        self.pack(side=tk.RIGHT)

    def _split_record(self, event):
        index = event.widget.curselection()[0]
        dt, tag, note = gui_manager.split_record(index)
        self._dt_var.set(dt)
        self._tag_var.set(tag)
        self._note_var.set(note)

    def update_record_list(self):
        self.listbox_var.set(gui_manager.str_record_list())
        self.listbox.yview_moveto(fraction=1)


root = tk.Tk()
gui_manager = GUIManager()
record_list_frame = RecordListFrame(root)
MenuFrame(root)
root.mainloop()
