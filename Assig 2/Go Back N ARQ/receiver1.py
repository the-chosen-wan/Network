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

print('initiating receiver ')
host = '127.0.0.2'
port = 9090

mySocket=socket.socket()
mySocket.connect((host,port))
rn=0

def receive(mySocket):
    lis=[]
    while True:
        r = mySocket.recv(1024).decode()
        data=r.split('/')[0]
        seqno=int(r.split('/')[-1])
        error=CheckError(data)
        print(f"Received frame {seqno}")
        
        if error==1:
            # time.sleep(0.5)
            ret="timeout"+'/'+str(rn)+":"
            print(f"Error in frame {seqno}")
            mySocket.send(ret.encode())
        
        else:
            #time.sleep(0.5)
            ret="ack"+"/"+str(rn)+":"
            mySocket.send(ret.encode())


if __name__=='__main__':
    receive(mySocket)

