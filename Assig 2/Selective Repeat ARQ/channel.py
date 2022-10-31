import socket
import time
import subprocess
import random
import os
from threading import Thread


def injectRandomError(frame):
    p = random.random()
    if p < 0.4:
        return frame
    pos = random.randint(0, len(frame)-1)
    frame = frame[:pos]+'1'+frame[pos+1:]
    return frame


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
            data = conn[0].recv(1024).decode()
            seqno = int(data.split('/')[-1])
            data = data.split('/')[0]
            if data == 'q0':
                break
            data = injectRandomError(data)
            data = data+'/'+str(seqno)

            rconn = random.choice(self.recvconn)
            rconn[0].send(data.encode())
            ret = rconn[0].recv(1024).decode()
            conn[0].send(ret.encode())
        return


if __name__ == '__main__':
    c = Channel(1, 1)
    c.InitializeSenders()
    c.InitializeReceivers()
    c.run()
    c.CloseSenders()
    c.CloseReceivers()
