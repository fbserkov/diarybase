import tkinter as tk

from const import DELETE, UPDATE
from gui_temp import TEXT, COMMAND
from guimanager import GUIManager


class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._gui_manager = GUIManager()

        self._listbox_var = tk.StringVar(master=self)
        self._listbox = tk.Listbox(
            master=self, width=80, listvariable=self._listbox_var)
        self._entry_var = tk.StringVar(master=self)
        self._entry = tk.Entry(
            master=self, width=80, textvariable=self._entry_var)

        self._create_widgets()
        self._update_record_list()
        self.pack()

    def _create_widgets(self):
        tk.Button(
            master=self, text=TEXT,
            command=self._add_update_call(COMMAND),
        ).pack()
        for t, c in self._gui_manager.text_and_command_list:
            tk.Button(master=self, text=t, command=self._add_update_call(c)).pack()

        tk.Button(
            master=self, text=DELETE,
            command=self._add_update_call(self._delete_last_record),
        ).pack()
        tk.Button(
            master=self, text=UPDATE,
            command=self._update_record_list,
        ).pack()

        self._listbox.bind('<<ListboxSelect>>', self._listbox_callback)
        self._listbox.pack()
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


root = tk.Tk()
GUI(master=root)
root.mainloop()
