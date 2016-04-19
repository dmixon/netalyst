import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import time
from time import strptime
from tkinter import ttk
from tkinter import *
import paramiko
import pymysql
import calendar
from datetest import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from datetime import datetime

#This is the main Netalyst GUI. Within a user will be able to see a live graph of hosts which they select, or query upon data that has been logged (based on day, month, or time interval). Additionally, there will be a configuration page within which a usercan request to start logging, as well as save parameters for host (such as IP, username, and password). 

matplotlib.rcParams['axes.color_cycle'] = ['r', 'b', 'g']
LARGE_FONT= ("Verdana", 12)
f = plt.figure()
db = pymysql.connect("localhost","root","Strace18!","NETDB")
cursor = db.cursor()

#Function that creates live bar graph - currently parameters are hard coded, but will be selected by user in the final build.


#Main GUI implementation
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
        hostlabel = tk.Label(self, text="Nickname (or hostname):")
        hostlabel.pack()
        self.hostentry = tk.Entry(self, bd = 5)
        self.hostentry.pack()
        iplabel = tk.Label(self, text="Enter ip address:")
        iplabel.pack()
        self.ipentry = tk.Entry(self, bd = 5)
        self.ipentry.pack()
        userlabel = tk.Label(self, text="Enter username:")
        userlabel.pack()
        self.userentry = tk.Entry(self, bd = 5)
        self.userentry.pack()
        passlabel = tk.Label(self, text="Enter password:")
        passlabel.pack()
        self.passentry = tk.Entry(self, bd = 5, show="*")
        self.passentry.pack()
        self.dictlist = []
        button3 = tk.Button(self, text="Add to live graph list", command=lambda: self.createdict())
        button3.pack()
        button2 = tk.Button(self, text="Show Live Graph", command=self.create_window)
        button2.pack()

    def createdict(self):
        d = {'Hostname': '', 'IP': '', 'Username': '', 'Pass': ''}
        d['Hostname'] = self.hostentry.get()
        d['IP'] = self.ipentry.get()
        d['Username'] = self.userentry.get()
        d['Pass'] = self.passentry.get()
        self.hostentry.delete(0, 'end')
        self.ipentry.delete(0, 'end')
        self.userentry.delete(0, 'end')
        self.passentry.delete(0, 'end')
        self.dictlist.append(d)
        print(self.dictlist[0]['Hostname']) 
              
    def animated_barplot(self, i):
        print(self.dictlist[0])
        print(self.dictlist[1])
        ssh = paramiko.SSHClient()
        ssh2 = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.dictlist[0]['IP'],username=self.dictlist[0]['Username'],password=self.dictlist[0]['Pass'])
        ssh2.connect(self.dictlist[1]['IP'],username=self.dictlist[1]['Username'],password=self.dictlist[1]['Pass'])

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
        
#Function to create separate window and begin live graphing    
    def create_window(self):
                
        t = Toplevel(self)
        canvas2 = FigureCanvasTkAgg(f, t)
        canvas2.show()
        canvas2.get_tk_widget().pack(side=BOTTOM, fill=BOTH,expand=True)
        canvas2._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        ani = animation.FuncAnimation(f, self.animated_barplot, interval=20, blit=True, repeat=False)

#Static graphing page
class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.label = Label(self, text="Page One!!!", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button.pack()

#Function to create static graph based upon single date input by user (can select for multiple hosts)        
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
            
            z = (', '.join(self.datehost))
            fig.suptitle(('Traffic for %s for %s') % (z, date.strftime('%A, %B %d')), fontsize=14, fontweight='bold')
            plt.legend(patchlist, (self.datehost))
            plt.show()
                     
        def getmonth():
             
            plt.close()
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_xlabel('Day')
            ax.set_ylabel('Megabytes received')
            c = 0
            colarray = ['red','blue','green']
            patchlist2 = []

            for host in self.datehost2 :
                query = """SELECT CAST(date AS DATE), SUM(MBYTES) as 'mbytes per day', HOSTNAME FROM RXGRAPH WHERE HOSTNAME LIKE%s AND MONTH(date) LIKE %s GROUP BY CAST(date AS DATE)"""
                var = (host, self.monthsel)
                cursor.execute(query, var)
                data = cursor.fetchall()
                datearr = []
                daybytes = [] 
                harr = []
                d = 0
                print(data)

                for row in data :
                    date = row[0]
                    bytesrec = row[1]
                    datearr.append(date)
                    daybytes.append(bytesrec)
                    print(date)
                    print(bytesrec)

                for i in datearr:
                    datday = datearr[d].strftime('%d')
                    harr.append(int(datday))
                    d+=1
                
                ax.plot(harr, daybytes)
                patch2 = mpatches.Patch(color=colarray[c])
                patchlist2.append(patch2)
                c+=1
            
            x = (', '.join(self.datehost2)) 
            y = calendar.month_name[self.monthsel]
            fig.suptitle('Traffic for %s for %s' % (x, y), fontsize=14, fontweight='bold')
            plt.legend(patchlist2, (self.datehost2))
            plt.show()
           
        
        def daterange():
             
            plt.close()
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_xlabel('Day')
            ax.set_ylabel('Megabytes received')
            c = 0
            colarray = ['red','blue','green']
            patchlist2 = []
            d2 = ''.join(dentry2.get())
            dashstring2 = '-'.join([d2[:4], d2[4:6], d2[6:]])
            d3 = ''.join(dentry3.get())
            dashstring3 = '-'.join([d3[:4], d3[4:6], d3[6:]])

            for host in self.datehost3 :
                query = """SELECT CAST(date as DATE), SUM(MBYTES), HOSTNAME FROM RXGRAPH WHERE CAST(date AS DATE) BETWEEN %s AND %s AND HOSTNAME LIKE %s GROUP BY CAST(date AS DATE)"""
                var = (dashstring2, dashstring3, host)
                cursor.execute(query, var)
                data = cursor.fetchall()
                datearr = []
                daybytes = [] 
                harr = []
                d = 0
                print(data)

                for row in data :
                    date = row[0]
                    dembytes = row[1]
                    datearr.append(date)
                    daybytes.append(dembytes)

                for i in datearr:
                    datday = datearr[d].strftime('%d')
                    harr.append(int(datday))
                    d+=1
               
                patch2 = mpatches.Patch(color=colarray[c])
                patchlist2.append(patch2)
                c+=1
                ax.set_xticklabels(harr)
                ax.set_xticks(harr) 
                ax.plot(harr, daybytes)

            x = (', '.join(self.datehost3)) 
            #fig.suptitle('Traffic for %s between %s and %s' % (x, dashstring2.strftime('%A, %B %d'), dashstring3.strftime('%A,%B%d')), fontsize=14, fontweight='bold')
            plt.legend(patchlist2, (self.datehost3))
            plt.show()
#Populate drop down menu based on hosts being logged 
             	
        hostquery = """SELECT DISTINCT HOSTNAME FROM RXGRAPH"""
        cursor.execute(hostquery)
        hostdata = cursor.fetchall()
        self.hostarr = []
        self.hostarr2 = []
        self.hostarr3 = []
        self.datehost = []
        self.datehost2 = []
        self.datehost3 = []
        self.monthsel = 0
         
        for hrow in hostdata :
            h = hrow[0]
            self.hostarr.append(h)
            self.hostarr2.append(h)
            self.hostarr3.append(h)

        mb = Menubutton(self, text="hosts")
        mb.menu = Menu(mb, tearoff = 5)
        mb["menu"] = mb.menu
        t = 0
        for hst in self.hostarr :
            self.hostarr[t] = IntVar()
            mb.menu.add_checkbutton(label=hst,variable=self.hostarr[t],command=lambda hst=hst: self.hostexec1(hst))
            t +=1
         
        mb.pack()
        label3 = Label(self, text="Day, in format MM-DD-YYYY")
        label3.pack()
        dentry = DateEntry(self, font=('Helvetica', 20, tk.NORMAL), border=0)
        dentry.pack()
        button2 = ttk.Button(self, text = "Get date!", command=lambda: getdate())
        button2.pack()

        monthquery = """SELECT DISTINCT MONTH(date) FROM RXGRAPH"""
        cursor.execute(monthquery)
        monthdata = cursor.fetchall()
        self.montharr = []
        self.monthname = []
        print(monthdata)
        
        for month in monthdata :
            m = calendar.month_name[month[0]]
            mo = month[0]
            self.montharr.append(m)
            self.monthname.append(mo)
       
        mb2 = Menubutton(self, text="hosts")
        mb2.menu = Menu(mb2, tearoff = 5)
        mb2["menu"] = mb2.menu
        
        tr = 0  
        for hst in self.hostarr2 :
            self.hostarr2[tr] = IntVar()
            mb2.menu.add_checkbutton(label=hst,variable=self.hostarr2[tr],command=lambda hst=hst: self.hostexec2(hst))
            tr +=1

        mb2.pack()
        th = 0
        for mth in self.montharr :
            mr = self.monthname[th]
            self.montharr[th] = IntVar()
            rdo = Radiobutton(self,text=mth, value=1, variable=self.montharr[th],command=lambda mr=mr: self.monthexec(mr))
            rdo.pack() 
            th += 1

        button3 = ttk.Button(self, text = "Get month!", command=lambda: getmonth())
        button3.pack()
        
        mb3 = Menubutton(self, text="hosts")
        mb3.menu = Menu(mb3, tearoff = 5)
        mb3["menu"] = mb3.menu
        
        tz = 0  
        for hst in self.hostarr3 :
            self.hostarr3[tz] = IntVar()
            mb3.menu.add_checkbutton(label=hst,variable=self.hostarr3[tz],command=lambda hst=hst: self.hostexec3(hst))
            tr +=1
         
        mb3.pack()
        label4 = Label(self, text="Day, in format MM-DD-YYYY")
        label4.pack()
        dentry2 = DateEntry(self, font=('Helvetica', 20, tk.NORMAL), border=0)
        dentry2.pack()
        label5 = Label(self, text="Day, in format MM-DD-YYYY")
        label5.pack()
        dentry3 = DateEntry(self, font=('Helvetica', 20, tk.NORMAL), border=0)
        dentry3.pack()
        button4 = ttk.Button(self, text = "Get date range!", command=lambda: daterange())
        button4.pack()

#Create array of selected hosts in drop down menu
    def hostexec1(self, name):
        print(name)
        self.datehost.append(name)

    def hostexec2(self, name2):
        print(name2)
        self.datehost2.append(name2)

    def hostexec3(self, name3):
        print(name3)
        self.datehost3.append(name3)
     
    def monthexec(self, mot):
        print(mot)
        self.monthsel=mot
      
app = Testing()
app.mainloop()
