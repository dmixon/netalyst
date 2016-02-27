import paramiko
import time
import pymysql
import re

ssh = paramiko.SSHClient()
ssh2 = paramiko.SSHClient()
ssh3 = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.254.37',username='dmixon',password='Lebron236')
ssh2.connect('192.168.254.38',username='dmixon',password='Lebron236')
ssh3.connect('192.168.254.27',username='dmixon',password='Lebron236')
stdin, stdout, stderr = ssh.exec_command("hostname")
stdin2, stdout2, stderr2 = ssh2.exec_command("hostname")
stdin3, stdout3, stderr3 = ssh3.exec_command("hostname")
p = stdout.readlines()
p2 = stdout2.readlines()
p3 = stdout3.readlines()
hostname1 = "".join(filter(lambda char: char!= "/n", p))
hostname1 = "".join(filter(lambda x: not re.match(r'^\s*$', x), hostname1)) 
hostname2 = "".join(filter(lambda char: char!= "/n", p2))
hostname2 = "".join(filter(lambda x: not re.match(r'^\s*$', x), hostname2)) 
hostname3 = "".join(filter(lambda char: char!= "/n", p3))
hostname3 = "".join(filter(lambda x: not re.match(r'^\s*$', x), hostname3)) 
db = pymysql.connect("localhost","root","Lebron236","NETDB" )
cursor = db.cursor()

while True:
    t,t2,t3,z,z2,z3=(0,0,0,0,0,0)    
    for i in range(1800):
        y = []
        y2 = []
        y3 = []
        for i in range(2): 
            stdin, stdout, stderr = ssh.exec_command("cat /sys/class/net/eth0/statistics/rx_bytes")
            stdin2, stdout2, stderr2 = ssh2.exec_command("cat /sys/class/net/eno16777736/statistics/rx_bytes")
            stdin3, stdout3, stderr3 = ssh3.exec_command("cat /sys/class/net/eth0/statistics/rx_bytes")
            p = stdout.readlines()
            p2 = stdout2.readlines()
            p3 = stdout3.readlines()
            p = "".join(filter(lambda char: char!= "/n", p))
            p2 = "".join(filter(lambda char: char!= "/n", p2)) 
            p3 = "".join(filter(lambda char: char!= "/n", p3))
            q = int(p)
            q2 = int(p2)
            q3 = int(p3)
            x = int(q / 1024)
            x2 = int(q2 / 1024)
            x3 = int(q3 / 1024)
            y.append(x)
            y2.append(x2)
            y3.append(x3)
            time.sleep(1)
        t = int(y[1] - y[0])
        t2 = int(y2[1] - y2[0])
        t3 = int(y3[1] - y3[0])
        z += t
        z2 += t2
        z3 += t3
    print(z)
    print(z2)
    print(z3)
    sql = """INSERT INTO RXGRAPH(HOSTNAME, MBYTES)
              VALUES (%s, %s)"""
    sql2 = """INSERT INTO RXGRAPH(HOSTNAME, MBYTES)
              VALUES (%s, %s)"""
    sql3 = """INSERT INTO RXGRAPH(HOSTNAME, MBYTES)
              VALUES (%s, %s)"""
    cursor.execute(sql, (hostname1, int(z / 1024)))
    cursor.execute(sql2, (hostname2,int(z2 / 1024))) 
    cursor.execute(sql3, (hostname3, int(z3 / 1024)))
    db.commit()
