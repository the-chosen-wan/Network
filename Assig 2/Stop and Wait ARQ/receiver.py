import socket
import sys
import time
import random
from threading import Thread

def Wait():
    x = random.randint(0, 5)
    if x <= 1:
        time.sleep(0.2)
    return


def CheckError(data):
    parity = 0
    for i in data:
        if i == '1':
            parity += 1
    return parity % 2

def Extract(data):
    startind = -1
    endind = -1

    for i in range(len(data)):
        if data[i]=='/':
            endind=i
            if startind==-1:
                startind=i+1
    return data[0:startind-1],data[startind:endind]

class Receiver():
    def __init__(self):
        self.host = '127.0.0.2'
        self.port = 9090
        self.socket = socket.socket()
        self.socket.connect((self.host,self.port))
    
    def receive(self):
        while True:
            data = self.socket.recv(1024).decode()

            if data[0:len(data)-1]=='exit':
                break

            error=CheckError(data)
            Wait()
            if error==1:
                print("Error occured")
                time.sleep(2.2)
            else:
                print("Frame received")
                ret="ACK"
                self.socket.send(ret.encode())
        self.socket.close()
        return
            

if __name__=='__main__':
    r = Receiver()
    r.receive()
