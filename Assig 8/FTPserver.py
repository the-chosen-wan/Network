import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from threading import Thread
from FTPUtils import dataRecvOp, dataSendOp, listRecvOp, listSendOp
import tempfile
import os

controlClientAddr = ('127.0.0.1', 8023)
controlServerAddr = ('127.0.0.2', 8023)

dataClientAddr = ('127.0.0.1', 8022)
dataServerAddr = ('127.0.0.2', 8022)


def controlServerRoutine(serverDict):
    controlClientAddr = ('127.0.0.1', 8023)
    controlServerAddr = ('127.0.0.2',8023)
    fileList = ["server/"+i for i in os.listdir("server")]

    TCPsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPsock.bind(controlServerAddr)
    TCPsock.listen(1)

    with open("server/hosts.txt","r") as f:
        lines = f.readlines()
    
    users = dict()
    for line in lines:
        username = line.split()[0]
        password = line.split()[1]
        users[username]=password

    conn,addr = TCPsock.accept()
    conn.setblocking(True)
    data = conn.recv(1024)
    data = pickle.loads(data)

    if data[0]=="VERIFY":
        username = data[1]
        password = data[2]

        if username not in users.keys() or users[username]!=password:
            reply=["REJECT"]
        else:
            reply=["ACCEPT"]

        time.sleep(0.2)
        conn.send(pickle.dumps(reply))

    while True:
        conn.setblocking(True)
        data = conn.recv(1024)
        data = pickle.loads(data)
        flag = 0

        if data[0]=="EXIT":
            serverDict["EXIT"]=True
            conn.close()
            TCPsock.close()
            break

        if data[0]=="SEND":
            if data[1] in fileList:
                serverDict["SEND"] = True
                serverDict["RECEIVER"] = data[1]
                flag=1

        if data[0]=="RECV":
            if data[1] in fileList:
                serverDict["RECV"] = True
                serverDict["SENDER"] = data[1]
                flag = 1

        if data[0]=="DEL":
            if data[1] in fileList:
                serverDict["DEL"]=True
                serverDict["SENDER"]=data[1]
                flag=1

        if data[0]=="LIST":
            flag = 1
            serverDict["LIST"]=True

        if flag==1:
            ack="FOUND"
        else:
            ack = "NOT FOUND"

        ack = pickle.dumps([ack])
        conn.send(ack)
        time.sleep(0.5)


if __name__=='__main__':
    dataClientAddr = ('127.0.0.4', 8022)
    dataServerAddr = ('127.0.0.5', 8022)
    serverDict = dict()


    t1 = Thread(target=controlServerRoutine, args=[serverDict])
    keys = ["EXIT", "SEND", "RECV", "SENDER", "RECEIVER","LIST","DEL"]

    for k in keys:
        serverDict[k] = False
    t1.start()

    while True:
        if serverDict["EXIT"]:
            break

        if serverDict["SEND"]:
            fil = serverDict["RECEIVER"]
            t2 = Thread(target=dataRecvOp, args=[
                        fil, dataClientAddr, dataServerAddr])
            t2.start()
            t2.join()
            serverDict["SEND"]=False

        if serverDict["RECV"]:
            fil = serverDict["SENDER"]
            t2 = Thread(target=dataSendOp, args=[
                        fil, dataServerAddr, dataClientAddr])
            t2.start()
            t2.join()
            serverDict["RECV"]=False

        if serverDict["LIST"]:
            lis = os.listdir("server")
            t2 = Thread(target=listSendOp, args=[
                        dataServerAddr, dataClientAddr,lis])
            t2.start()
            t2.join()
            serverDict["LIST"]=False
            
        if serverDict["DEL"]:
            os.remove(serverDict["SENDER"])
            serverDict["DEL"]=False

        time.sleep(1)

    t1.join()
