import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import time
from tkinter import ttk
from tkinter import *
import paramiko
import pymysql
from datetest import *
from datetime import datetime

#This represents the beta of the main Netalyst program. Currently some parameters are hard coded, those will be selected by 
#the user in the final build. Additionally, error handling will be added and a final configuration page will be inserted
#(within which users can select hosts to be logged to)

matplotlib.rcParams['axes.color_cycle'] = ['r', 'b', 'g']
LARGE_FONT= ("Verdana", 12)
f = plt.figure()
db = pymysql.connect("localhost","root","PASSWORD","DATABASE NAME")
cursor = db.cursor()


#Function to create live graph - currently it is hard coded in, but the finished product will allow
#for the user to input IP, username, and password (or select from list if they have already saved it

def animated_barplot(i):
    ssh = paramiko.SSHClient()
    ssh2 = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('IP ADDRESS',username='USERNAME',password='PASSWORD')
    ssh2.connect('IP ADDRESS',username='USERNAME',password='PASSWORD')
    
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
            #time.sleep(.25)
        
        t = int(y[1] - y[0])
        t2 = int(y2[1] - y2[0])
        #print(t)
        #print(t2)    
        a.bar(1, t, width=1)
        a.bar(2, t2, width=1, color='r')
        f.canvas.draw()
        f.canvas.start_event_loop(timeout=.01)

#Creation of GUI - will include final config page in finished product

class Testing(Tk):
    def __init__(self, *args, **kwargs):


        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Netalyst client")
        
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
    
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack()
        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = tk.Button(self, text="Show Live Graph", command=self.create_window)
        button2.pack()

#Creates separate window for live graph
    
    def create_window(self):
                
        t = Toplevel(self)
        canvas2 = FigureCanvasTkAgg(f, t)
        canvas2.show()
        canvas2.get_tk_widget().pack(side=BOTTOM, fill=BOTH,expand=True)
        canvas2._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        ani = animation.FuncAnimation(f, animated_barplot, interval=20, blit=True, repeat=False)


#Static graphing page - currently user may input date and select from list of hostnames to graph. 
#Final version will also include selection of month or date range. Will also decide on whether or not 
#I want to include functionality for bar graphing and scatter plots here as well

class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.label = Label(self, text="Page One!!!", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button.pack()

#Function to create live graph for day based on data input below
        
        def getdate():
             
            plt.close()
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_xlabel('Hour')
            ax.set_ylabel('Megabytes received')
            c = 0
            colarray = ['red','blue','green']
            patchlist = []

            for host in self.datehost :
                d = ''.join(dentry.get())
                dashstring = '-'.join([d[:4], d[4:6], d[6:]])
                dashstring += "%"
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
                
                ax.plot(harr, bytearr)
                patch = mpatches.Patch(color=colarray[c])
                patchlist.append(patch)
                c+=1
            
            
            #fig.suptitle('Traffic for %s, %s, and %s for %s' % (tuple(self.datehost), date.strftime('%A, %B %d')), fontsize=14, fontweight='bold')
            plt.legend(patchlist, (self.datehost))
            plt.show()
  
 #Fill array based upon hosts user has selected logging for, then present those in a drop down menu to be selected
           	
        hostquery = """SELECT DISTINCT HOSTNAME FROM RXGRAPH"""
        cursor.execute(hostquery)
        hostdata = cursor.fetchall()
        self.hostarr = []
        self.datehost = []

        for hrow in hostdata :
            h = hrow[0]
            self.hostarr.append(h)
        
        mb = Menubutton(self, text="hosts")
        mb.menu = Menu(mb, tearoff = 5)
        mb["menu"] = mb.menu
        t = 0
        for hst in self.hostarr :
            self.hostarr[t] = IntVar()
            mb.menu.add_checkbutton(label=hst,variable=self.hostarr[t],command=lambda hst=hst: self.execute(hst))
            t +=1

        mb.pack()

#Allow user to select date for graph
        label3 = Label(self, text="Day, in format MM-DD-YYYY")
        label3.pack()
        dentry = DateEntry(self, font=('Helvetica', 20, tk.NORMAL), border=0)
        dentry.pack()
        button2 = ttk.Button(self, text = "Get date!", command=lambda: getdate())
        button2.pack() 

#Fill addtional array with hosts chosen above
    def execute(self, name):
        print(name)
        self.datehost.append(name)

app = Testing()
app.mainloop()
