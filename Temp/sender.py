import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from collections import deque
from threading import Thread,Lock
import tempfile
import os
TIMEOUT = 2
windowSize = 3

def dataThread(data,sendDict):
    UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDPsock.bind(("127.0.0.1",8081))
    recvAddr = ("127.0.0.2",8081)

    while True:
        if len(data)==0:
            break

        Sw = sendDict["Sw"]
        Sf = sendDict["Sf"]
        Sn = sendDict["Sn"]
        sendDict["Recv"] = Sf-1
        cnt  = 0

        while cnt<Sw and cnt<len(data):
            temp = data[cnt]
            cnt+=1
            print(f"Sending frame {Sn} and data {temp} ")
            temp = pickle.dumps([temp,Sn])
            UDPsock.sendto(temp,recvAddr)
            Sn = Sn+1#%(Sw+1)
            time.sleep(1)


        sendDict["Sn"]=Sn

        time.sleep(TIMEOUT)

        recvInd = sendDict["Recv"]

        while Sf<recvInd and len(data)>0:
            print(f"Received frame {Sf}")
            time.sleep(1)
            Sf = Sf+1#%(Sw+1)
            data.popleft()

        Sn = Sf
        sendDict["Sf"]=Sf
        sendDict["Sn"]=Sn

    UDPsock.close()

def ackThread(message,sendDict):
    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.bind(("127.0.0.1", 8082))

    while True:
        data,addr = UDPsock.recvfrom(1024)
        data = pickle.loads(data)

        recvInd = data[0]

        sendDict["Recv"] = max(sendDict["Recv"],recvInd)

        if len(message)==0:
            break

    UDPsock.close()

if __name__=='__main__':
    print("Enter q to stop")
    data = deque()

    x = input()

    while x!="q":
        data.append(x)
        x = input()

    sendDict = dict()

    sendDict["Sw"]=windowSize
    sendDict["Sn"]=0
    sendDict["Sf"]=0

    t1 = Thread(target=dataThread,args=[data,sendDict])
    t2 = Thread(target=ackThread,args=[data,sendDict])

    t1.start()
    t2.start()
    t1.join()
    t2.join()





