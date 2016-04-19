import tkinter as Tkinter
from ttkcalendar import *


def test():
    import sys
    root = Tkinter.Tk()
    root.title('Ttk Calendar')
    ttkcal = Calendar(firstweekday=calendar.SUNDAY)
    ttkcal.pack(expand=1, fill='both')

    #x = ttkcal.selection()  #this and the following line are what i inserted
    #print ('x is: %s) % x  #or perhaps return x

    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')
    root.mainloop()

if __name__ == '__main__':
    test()
