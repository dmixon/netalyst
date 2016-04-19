from tkinter import *
master = Tk()

def states():
    print(var.get())

var = IntVar()
c1 = Checkbutton(master, text="test", variable=var)
c1.pack()
b1 = Button(master, text="Show", command=states)
b1.pack()
mainloop()
