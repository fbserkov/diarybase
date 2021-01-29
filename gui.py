import tkinter as tk

from guimanager import GUIManager
from gui_proc import PROC_LIST

root = tk.Tk()
gui_manager = GUIManager()

for i in range(len(PROC_LIST)):
    tk.Button(text=PROC_LIST[i][0], command=PROC_LIST[i][1]).pack()
for kwargs in gui_manager.get_button_kwargs():
    tk.Button(**kwargs).pack()

root.mainloop()
