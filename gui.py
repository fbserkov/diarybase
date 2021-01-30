import tkinter as tk

from const import DELETE, UPDATE
from gui_temp import TEXT, COMMAND
from guimanager import GUIManager


def add_update_call(to_wrap):
    def wrapper():
        to_wrap()
        lbf.update_record_list()
    return wrapper


class ButtonFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(self, text=TEXT, command=add_update_call(COMMAND)).pack()
        for t, c in gui_manager.text_and_command_list:
            tk.Button(self, text=t, command=add_update_call(c)).pack()
        tk.Button(
            self, text=DELETE,
            command=add_update_call(gui_manager.delete_last_record),
        ).pack()
        tk.Button(self, text=UPDATE, command=lbf.update_record_list).pack()
        self.pack(side=tk.LEFT)


class ListboxFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        frame = tk.Frame(self)
        frame.pack()

        self.listbox_var = tk.StringVar(frame)
        self.listbox = tk.Listbox(
            frame, width=80, listvariable=self.listbox_var)
        self.listbox.bind('<<ListboxSelect>>', self._listbox_callback)
        self.listbox.pack(side=tk.LEFT)

        sb = tk.Scrollbar(frame, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.entry_var = tk.StringVar(self)
        self.entry = tk.Entry(self, width=80, textvariable=self.entry_var)
        self.entry.pack()

        self.update_record_list()
        self.pack(side=tk.RIGHT)

    def _listbox_callback(self, event):
        index = event.widget.curselection()[0]
        self.entry_var.set(gui_manager.get_record(index))

    def update_record_list(self):
        self.listbox_var.set(gui_manager.str_record_list())
        self.listbox.yview_moveto(1)


root = tk.Tk()
gui_manager = GUIManager()
lbf = ListboxFrame(root)
ButtonFrame(root)
root.mainloop()
