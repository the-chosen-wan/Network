import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from threading import Thread

controlClientAddr = ('127.0.0.1',8023)
controlServerAddr = ('127.0.0.2',8023)

dataClientAddr = ('127.0.0.1',8022)
dataServerAddr = ('127.0.0.2',8022)

def controlClientRoutine():
    controlClientAddr = ('127.0.0.1', 8023)
    controlServerAddr = ('127.0.0.2',8023)

    TCPsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPsock.connect(controlServerAddr)

    time.sleep(1)
    msg = "SENDING"
    TCPsock.send(msg.encode())
    TCPsock.close()
    return

def controlServerRoutine(controlDict):
    controlClientAddr = ('127.0.0.1', 8023)
    controlServerAddr = ('127.0.0.2',8023)

    TCPsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPsock.bind(controlServerAddr)
    TCPsock.listen(1)

    conn,addr = TCPsock.accept()
    msg = conn.recv(1024).decode()
    controlDict["control"]=msg

    TCPsock.close()

def dataClientRoutine():
    dataClientAddr = ('127.0.0.1',8022)
    dataServerAddr = ('127.0.0.2',8022)

    TCPsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPsock.connect(dataServerAddr)

    with open("input.txt","r") as f:
        lines = f.readlines()
    
    TCPsock.send(str(len(lines)).encode())
    time.sleep(2)

    for line in lines:
        TCPsock.send(line.encode())
        time.sleep(2)

    TCPsock.close()

def dataServerRoutine(controlDict):
    dataClientAddr = ('127.0.0.1', 8022)
    dataServerAddr = ('127.0.0.2',8022)

    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.bind(dataServerAddr)
    TCPsock.listen(1)

    while "control" not in controlDict.keys():
        pass

    conn,addr = TCPsock.accept()

    num = int(conn.recv(1024).decode())
    time.sleep(2)
    op = open("output.txt", "w")

    for i in range(num):
        msg = conn.recv(1024).decode()
        op.write(msg)
        time.sleep(1)
        op.flush()
        time.sleep(1)

    TCPsock.close()
    op.close()

def clientRoutine():
    t1 = Thread(target=controlClientRoutine,args=[])
    t2 = Thread(target=dataClientRoutine,args=[])

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def serverRoutine():
    clientDict = dict()

    t1 = Thread(target=controlServerRoutine,args=[clientDict])
    t2 = Thread(target=dataServerRoutine,args=[clientDict])

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__=='__main__':
    p1 = Process(target=clientRoutine,args=[])
    p2 = Process(target=serverRoutine,args=[])

    p2.start()
    time.sleep(1)
    p1.start()

    p2.join()
    p1.join()



    


        
