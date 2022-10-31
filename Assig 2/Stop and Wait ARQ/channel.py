import socket
import time
import subprocess
import random
import os
from threading import Thread


def Noise(frame):
    p = random.random()
    if p < 0.5:
        pos = random.randint(0, len(frame)-1)
        frame = frame[:pos]+'1'+frame[pos+1:]
    return frame


def Extract(data):
    startind = -1
    endind = -1

    for i in range(len(data)):
        if data[i] == '/':
            endind = i
            if startind == -1:
                startind = i+1
    return data[0:startind-1], data[startind:endind]


class Channel():
    def __init__(self, sendno, recvno):
        self.sendno = sendno
        self.recvno = recvno

        self.sendhost = '127.0.0.1'
        self.sendport = 8080
        self.sendconn = []

        self.recvhost = '127.0.0.2'
        self.recvport = 9090
        self.recvconn = []

    def InitializeSenders(self):
        sock = socket.socket()
        sock.bind((self.sendhost, self.sendport))
        sock.listen(self.sendno)

        for i in range(self.sendno):
            conn = sock.accept()
            self.sendconn.append(conn)

    def InitializeReceivers(self):
        sock = socket.socket()
        sock.bind((self.recvhost, self.recvport))
        sock.listen(self.recvno)

        for i in range(self.recvno):
            conn = sock.accept()
            conn[0].settimeout(2)
            self.recvconn.append(conn)

    def CloseSenders(self):
        for conn in self.sendconn:
            conn[0].close()

    def CloseReceivers(self):
        for conn in self.recvconn:
            conn[0].close()
    
    def run(self):
        while True:
            conn = self.sendconn[0]
            data=conn[0].recv(1024).decode()
            if data[0:len(data)-1] == 'exit':
                break
            data=Noise(data)

            rconn = random.choice(self.recvconn)
            rconn[0].send(data.encode())

            time.sleep(0.001)
            try:
                ret = rconn[0].recv(1024).decode()
                conn[0].send(ret.encode())
            except Exception:
                pass
        return



if __name__=='__main__':
    c = Channel(1,1)
    c.InitializeSenders()
    c.InitializeReceivers()
    c.run()
    c.CloseSenders()
    c.CloseReceivers()

