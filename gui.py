import tkinter as tk

from const import DELETE, PRINT
from guimanager import GUIManager
from gui_proc import PROC_LIST

root = tk.Tk()
gui_manager = GUIManager()

for i in range(len(PROC_LIST)):
    tk.Button(text=PROC_LIST[i][0], command=PROC_LIST[i][1]).pack()

text = tk.Text()


def delete_last_record():
    gui_manager.delete_last_record()


def print_record_list():
    text.delete('1.0', tk.END)
    text.insert('1.0', gui_manager.str_record_list())
    text.see(tk.END)


tk.Button(text=DELETE, command=delete_last_record).pack()
tk.Button(text=PRINT, command=print_record_list).pack()

text.pack()
root.mainloop()
