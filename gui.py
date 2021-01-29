import tkinter as tk

from const import DELETE, PRINT
from guimanager import GUIManager
from gui_proc import PROC_LIST


class GUI:
    def __init__(self):
        root = tk.Tk()
        self.gui_manager = GUIManager()
        self.text = None
        self.create_widgets()
        root.mainloop()

    def create_widgets(self):
        for i in range(len(PROC_LIST)):
            tk.Button(text=PROC_LIST[i][0], command=PROC_LIST[i][1]).pack()
        self.text = tk.Text()
        tk.Button(text=DELETE, command=self.delete_last_record).pack()
        tk.Button(text=PRINT, command=self.print_record_list).pack()
        self.text.pack()

    def delete_last_record(self):
        self.gui_manager.delete_last_record()

    def print_record_list(self):
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', self.gui_manager.str_record_list())
        self.text.see(tk.END)


GUI()
