import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import tkinter as tk
from tkinter import ttk
import paramiko
import pymysql
from datetest import *
from datetime import datetime

LARGE_FONT= ("Verdana", 12)
f = plt.figure()
db = pymysql.connect("localhost","root","Strace18!","NETDB")
cursor = db.cursor()

def animated_barplot(i):
    ssh = paramiko.SSHClient()
    ssh2 = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.254.37',username='dmixon',password='Strace18!')
    ssh2.connect('192.168.254.27',username='dmixon',password='Strace18!')
    
    while True:
        
        f.clf()
        y = []
        y2 = []
        a = f.add_subplot(111)
        a.axis([0, 6, 0, 200])
        for i in range(2):
            stdin, stdout, stderr = ssh.exec_command("cat /sys/class/net/eth0/statistics/rx_bytes")
            stdin2, stdout2, stderr2 = ssh2.exec_command("cat /sys/class/net/eth0/statistics/rx_bytes")
            p = stdout.readlines()
            p2 = stdout2.readlines()
            p = "".join(filter(lambda char: char!= "/n", p))
            p2 = "".join(filter(lambda char: char!= "/n", p2))
            q = int(p)
            q2 = int(p2)
            x = int(q / 1024)
            x2 = int(q2 / 1024)
            y.append(x)
            y2.append(x2)
            time.sleep(.25)
        
        t = int(y[1] - y[0])
        t2 = int(y2[1] - y2[0])
        #print(t)
        #print(t2)    
        a.bar(1, t, width=1)
        a.bar(2, t2, width=1, color='r')
        f.canvas.draw()
        f.canvas.start_event_loop(timeout=.01)
        #print (pause)



class Testing(tk.Tk):
    def __init__(self, *args, **kwargs):


        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Netalyst client")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {} 
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
         
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack()
        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()
       
        canvas2 = FigureCanvasTkAgg(f, self)

        canvas2.show()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, 
                                    expand=True)
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button.pack()
        
        def getdate():
            d = ''.join(dentry.get())
            dashstring = '-'.join([d[:4], d[4:6], d[6:]])
            dashstring += "%"
            host = e1.get()
            query = """SELECT * FROM RXGRAPH WHERE date LIKE %s AND HOSTNAME LIKE %s"""
            var = (dashstring, host)
            cursor.execute(query, var)
            data = cursor.fetchall()
            datearr = []
            bytearr = []
            harr = []
            d = 0

            for row in data :
                date = row[0]
                hostname = row[1]
                bytesrec = row[2]
                datearr.append(date)
                bytearr.append(bytesrec)

            for i in datearr:
                hour = datearr[d].strftime('%H')
                harr.append(int(hour))
                d+=1

            fig = plt.figure(1)
            #fig.suptitle('Traffic for %s for %s' % (host, date.strftime('%A, %B %d')), fontsize=14, fontweight='bold')
            ax = fig.add_subplot(211)
            #ax.set_xlabel('Hour')
            #ax.set_ylabel('Megabytes received')
            ax.plot(harr, bytearr)
            plt.show()

        label2 = tk.Label(self, text="Hostname:")
        label2.pack()
        e1 = tk.Entry(self)
        e1.pack()
        label3 = tk.Label(self, text="Day, in format MM-DD-YYYY")
        label3.pack()
        dentry = DateEntry(self, font=('Helvetica', 20, tk.NORMAL), border=0)
        dentry.pack()
        button2 = ttk.Button(self, text = "Get date!", command=lambda: getdate())
        button2.pack() 
        
app = Testing()
ani = animation.FuncAnimation(f, animated_barplot, interval=20, blit=True, repeat=False)
app.mainloop()
