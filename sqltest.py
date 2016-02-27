import pymysql
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

db = pymysql.connect("localhost","root","Lebron236","NETDB" )
cursor = db.cursor()
query = """SELECT * FROM RXGRAPH WHERE date LIKE '2016-02-26%' AND HOSTNAME LIKE 'yummy%'"""
cursor.execute(query)
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
    #print(hour)
    d+=1

print(harr[0])
fig = plt.figure(1)
fig.suptitle('Traffic for %s for %s' % (hostname, date.strftime('%A, %B %dth')), fontsize=14, fontweight='bold')
ax = fig.add_subplot(211)
ax.set_xlabel('Hour')
ax.set_ylabel('Megabytes received')
ax.plot(harr,bytearr)
plt.xticks(np.arange(min(harr), max(harr)+1, 2.0))
plt.yticks(np.arange(min(bytearr), max(bytearr)+1, 2.0))
plt.show()    
cursor.close()
db.close() 
