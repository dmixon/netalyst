import pymysql
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

db = pymysql.connect("localhost","root","Lebron236","NETDB" )
cursor = db.cursor()

def querytime(dateq, hostq):

    query = """SELECT * FROM RXGRAPH WHERE date LIKE %s AND HOSTNAME LIKE %s"""
    var = (dateq, hostq)
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
    
    querytime.hostq = hostname
    querytime.dateq = date
    querytime.harr = harr
    querytime.bytearr = bytearr

fig = plt.figure(1)
querytime("2016-03-08%","dmubiserver")
host1 = querytime.hostq
barr1 = querytime.bytearr
querytime("2016-03-08%","dmfedora")
host2 = querytime.hostq
barr2 = querytime.bytearr
querytime("2016-03-08%","yummypie")
host3 = querytime.hostq
barr3 = querytime.bytearr

fig.suptitle('Traffic for all servers for %s' % (querytime.dateq.strftime('%A, %B %d')), fontsize=14, fontweight='bold')
ax = fig.add_subplot(211)
ax.set_xlabel('Hour')
ax.set_ylabel('Megabytes received')
ax.plot(querytime.harr,barr1,'r--')
ax.plot(querytime.harr,barr2)
ax.plot(querytime.harr,barr3,'g^')
plt.xticks(np.arange(min(querytime.harr), max(querytime.harr)+1, 2.0))
red_patch = mpatches.Patch(color='red')
blue_patch = mpatches.Patch(color='blue')
green_patch = mpatches.Patch(color='green')
plt.legend([red_patch, blue_patch, green_patch], ['dmubiserver','dmfedora','yummypie'])
#plt.yticks(np.arange(min(bytearr), max(bytearr)+1, 5.0))
plt.show()    
cursor.close()
db.close() 
