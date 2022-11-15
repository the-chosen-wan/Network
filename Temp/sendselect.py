import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from collections import deque
from threading import Thread, Lock
import tempfile
import os
TIMEOUT = 2
windowSize = 4

def dataThread(data,sendDict):
    UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDPsock.bind(("127.0.0.1",8081))
    recvAddr = ("127.0.0.2",8081)

    while True:
        if len(data)==0:
            break

        Sf = sendDict["Sf"]
        Sw = sendDict["Sw"]
        Sn = sendDict["Sn"]
        cnt = 0
        sendDict["Recv"]=[]
        storeDict = dict()

        while cnt<Sw and len(data)>0:
            temp = data[cnt]
            cnt+=1
            print(f"Sending frame {Sn} and data {temp} ")
            storeDict[Sn] = temp

            temp = pickle.dumps([temp,Sn])
            UDPsock.sendto(temp,recvAddr)
            Sn = Sn+1
            time.sleep(1)

        time.sleep(TIMEOUT)

        while len(sendDict["Recv"])>0:
            tempDict = sendDict["Recv"]
            sendDict["Recv"] = []

            for ind in tempDict:
                temp = storeDict[ind]
                print(f"Resending frame {ind} and data {temp}")
                temp = pickle.dumps([temp,ind])
                UDPsock.sendto(temp,recvAddr)

                time.sleep(1)

            time.sleep(TIMEOUT)

        while Sf<Sn:
            Sf+=1
            data.popleft()
        
        sendDict["Sn"]=Sn
        sendDict["Sf"]=Sf

    UDPsock.close()


def ackThread(message,sendDict):
    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.bind(("127.0.0.1", 8082))

    while True:
        if len(message)==0:
            break

        data,addr = UDPsock.recvfrom(1024)

        data = pickle.loads(data)

        if data[0]=="NAK":
            sendDict["Recv"].append(data[1])

    UDPsock.close()

if __name__ == '__main__':
    data = deque()
    print("Enter q to stop")

    x = input()
    while x!="q":
        data.append(x)
        x = input()

    sendDict = dict()
    sendDict["Sw"]=windowSize
    sendDict["Sn"]=0
    sendDict["Sf"]=0
    
    t1 = Thread(target=dataThread,args=[data,sendDict])
    t2 = Thread(target = ackThread,args=[data,sendDict])

    t1.start()
    t2.start()
    t1.join()
    t2.join()

