import tkinter as tk

from const import DELETE, UPDATE
from gui_temp import TEXT, COMMAND
from guimanager import GUIManager


class GUI:
    def __init__(self):
        root = tk.Tk()
        self._gui_manager = GUIManager()

        self._listbox_var = None
        self._listbox = None
        self._entry_var = None
        self._entry = None

        self._create_widgets()
        self._update_record_list()
        root.mainloop()

    def _create_widgets(self):
        tk.Button(text=TEXT, command=self._add_update_call(COMMAND)).pack()
        for t, c in self._gui_manager.text_and_command_list:
            tk.Button(text=t, command=self._add_update_call(c)).pack()

        tk.Button(
            text=DELETE,
            command=self._add_update_call(self._delete_last_record),
        ).pack()
        tk.Button(text=UPDATE, command=self._update_record_list).pack()

        self._listbox_var = tk.StringVar()
        self._listbox = tk.Listbox(width=80, listvariable=self._listbox_var)
        self._listbox.bind('<<ListboxSelect>>', self._listbox_callback)
        self._listbox.pack()

        self._entry_var = tk.StringVar()
        self._entry = tk.Entry(width=80, textvariable=self._entry_var)
        self._entry.pack()

    def _add_update_call(self, to_wrap):
        def wrapper():
            to_wrap()
            self._update_record_list()
        return wrapper

    def _listbox_callback(self, event):
        index = event.widget.curselection()[0]
        self._entry_var.set(self._gui_manager.get_record(index))

    def _delete_last_record(self):
        self._gui_manager.delete_last_record()

    def _update_record_list(self):
        self._listbox_var.set(self._gui_manager.str_record_list())
        self._listbox.yview_moveto(1)


GUI()
