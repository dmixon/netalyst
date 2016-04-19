import tkinter as tk


class DateEntry(tk.Frame):
    def __init__(self, master, frame_look={}, **look):
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)

        args = {'relief': tk.FLAT}
        args.update(look)

        self.entry_1 = tk.Entry(self, width=2, **args)
        self.label_1 = tk.Label(self, text='-', **args)
        self.entry_2 = tk.Entry(self, width=2, **args)
        self.label_2 = tk.Label(self, text='-', **args)
        self.entry_3 = tk.Entry(self, width=4, **args)

        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.entry_3.pack(side=tk.LEFT)

        self.entry_1.bind('<KeyRelease>', self._e1_check)
        self.entry_2.bind('<KeyRelease>', self._e2_check)
        self.entry_3.bind('<KeyRelease>', self._e3_check)

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, cont[:-1])

    def _e1_check(self, e):
        cont = self.entry_1.get()
        if len(cont) >= 2:
            self.entry_2.focus()
        if len(cont) > 2 or not cont[-1].isdigit():
            self._backspace(self.entry_1)
            self.entry_1.focus()

    def _e2_check(self, e):
        cont = self.entry_2.get()
        if len(cont) >= 2:
            self.entry_3.focus()
        if len(cont) > 2 or not cont[-1].isdigit():
            self._backspace(self.entry_2)
            self.entry_2.focus()

    def _e3_check(self, e):
        cont = self.entry_2.get()
        if len(cont) > 4 or not cont[-1].isdigit():
            self._backspace(self.entry_3)

    def get(self):
        return self.entry_3.get(), self.entry_1.get(), self.entry_2.get()


if __name__ == '__main__':
    def show_contents(e):
        print (dentry.get())

    win = tk.Tk()
    win.title('DateEntry demo')

    dentry = DateEntry(win, font=('Helvetica', 40, tk.NORMAL), border=0)
    dentry.pack()

    win.bind('<Return>', show_contents)
    win.mainloop()
