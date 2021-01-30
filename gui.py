import tkinter as tk

from const import DELETE, UPDATE
from gui_temp import TEXT, COMMAND
from guimanager import GUIManager

gui_manager = GUIManager()


def add_update_call(to_wrap):
    def wrapper():
        to_wrap()
        lbf.update_record_list()
    return wrapper


class ButtonFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(
            master=self, text=TEXT, command=add_update_call(COMMAND),
        ).pack()
        for t, c in gui_manager.text_and_command_list:
            tk.Button(
                master=self, text=t, command=add_update_call(c)).pack()
        tk.Button(
            master=self, text=DELETE,
            command=add_update_call(gui_manager.delete_last_record),
        ).pack()
        tk.Button(
            master=self, text=UPDATE, command=lbf.update_record_list).pack()


class ListboxFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.listbox_var = tk.StringVar(master=self)
        self.listbox = tk.Listbox(
            master=self, width=80, listvariable=self.listbox_var)
        self.listbox.bind('<<ListboxSelect>>', self._listbox_callback)
        self.listbox.pack()

        self.entry_var = tk.StringVar(master=self)
        self.entry = tk.Entry(
            master=self, width=80, textvariable=self.entry_var)
        self.entry.pack()

        self.update_record_list()

    def _listbox_callback(self, event):
        index = event.widget.curselection()[0]
        self.entry_var.set(gui_manager.get_record(index))

    def update_record_list(self):
        self.listbox_var.set(gui_manager.str_record_list())
        self.listbox.yview_moveto(1)


root = tk.Tk()
lbf = ListboxFrame(master=root)
bf = ButtonFrame(master=root)
bf.pack()
lbf.pack()
root.mainloop()
