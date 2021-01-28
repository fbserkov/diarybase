import tkinter as tk

from gui_proc import PROC_LIST, TAGS


root = tk.Tk()
for i in range(len(PROC_LIST)):
    tk.Button(text=TAGS[i], command=PROC_LIST[i]).pack()
root.mainloop()
