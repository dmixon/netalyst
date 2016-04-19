import paramiko
import time
import re

def stripout(dstr):
    dstr = "".join(filter(lambda char: char!= "/n", dstr))
    stripout.dstr = "".join(filter(lambda x: not re.match(r'^\s*$', x), dstr))

def mega(num):
    num = int(num)
    mega.num = int(num / 1048576)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.254.38',username='dmixon',password='Lebron236')
cat = "ls /sys/class/net | grep e"
stdin, stdout, stderr = ssh.exec_command(cat)
stripout(stdout.readlines())
netfile = " cat /sys/class/net/%s/statistics/rx_bytes" % stripout.dstr
stdin, stdout, stderr = ssh.exec_command(netfile)
stripout(stdout.readlines())
mega(stripout.dstr)
print(mega.num)
