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
    def __init__(self,window_size):
        self.rn=0
        self.window_size=window_size
        print('initiating receiver ')
        host = '127.0.0.2'
        port = 9090

        self.mySocket = socket.socket()
        self.mySocket.connect((host, port))

    def receive(self):
        while True:
            flag=False
            self.mySocket.settimeout(5)
            # r = self.mySocket.recv(1024).decode()
            # print(r)
            recvlist=[]
            
            try:
                while True:
                    r = self.mySocket.recv(1024).decode()
                    print(r)
                    recvlist.append(r)
            except Exception:
                pass
            
            returnlist=[]
            for r in recvlist:
                seqno=int(r.split('/')[-1])
                data=r.split('/')[0]
                if data=='q0':
                    flag=True
                error=CheckError(data)
                self.rn=(self.rn+1)%self.window_size
                if error==1:
                    print(f"Error receiving frame {seqno}")
                    returnlist.append(str(self.rn)+'/'+"timeout")
                else:
                    print(f"Received frame {seqno}")
                    returnlist.append(str(self.rn)+'/'+"ack")

            if flag:
                break

            for r in returnlist:
                self.mySocket.send(r.encode())
                time.sleep(0.1)
            # data=self.mySocket.recv(1024).decode()
            # seqno=int(data.split('/')[-1])
            # data=data.split('/')[0]
            # if data=='q0':
            #     break
            # error=CheckError(data)

            # if error==1 or seqno!=self.rn:
            #     print(f"Error receiving frame {seqno}")
            #     ret=str(-1)+'/'+"timeout"
            #     time.sleep(2)
            #     self.mySocket.send(ret.encode())
            # else:
            #     self.rn=(self.rn+1)%self.window_size
            #     print(f"Received frame {seqno}")
            #     ret=str(self.rn)+'/'+"ack"
            #     self.mySocket.send(ret.encode())
            
        self.mySocket.close()
        return

if __name__=='__main__':
    r=Receiver(7)
    r.receive()