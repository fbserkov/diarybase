import tkinter as tk

from const import DELETE, UPDATE
from gui_temp import TEXT, COMMAND
from guimanager import GUIManager


class GUI:
    def __init__(self):
        root = tk.Tk()
        self.gui_manager = GUIManager()
        self.text = None
        self.create_widgets()
        self.update_record_list()
        root.mainloop()

    def create_widgets(self):
        tk.Button(text=TEXT, command=self._add_update_call(COMMAND)).pack()
        for t, c in self.gui_manager.text_and_command_list:
            tk.Button(text=t, command=self._add_update_call(c)).pack()
        self.text = tk.Text()
        tk.Button(
            text=DELETE,
            command=self._add_update_call(self.delete_last_record),
        ).pack()
        tk.Button(text=UPDATE, command=self.update_record_list).pack()
        self.text.pack()

    def _add_update_call(self, to_wrap):
        def wrapper():
            to_wrap()
            self.update_record_list()
        return wrapper

    def delete_last_record(self):
        self.gui_manager.delete_last_record()

    def update_record_list(self):
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', self.gui_manager.str_record_list())
        self.text.see(tk.END)


GUI()
