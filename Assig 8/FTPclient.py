import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from threading import Thread
from FTPUtils import dataRecvOp,dataSendOp,listRecvOp,listSendOp
import tempfile
import os

controlClientAddr = ('127.0.0.1', 8023)
controlServerAddr = ('127.0.0.2', 8023)

dataClientAddr = ('127.0.0.1', 8022)
dataServerAddr = ('127.0.0.2', 8022)


def controlClientRoutine(clientDict):
    controlClientAddr = ('127.0.0.1', 8023)
    controlServerAddr = ('127.0.0.2', 8023)

    print("Verifying authenticity")

    username = input("Enter username :")
    password = input("Enter password :")
    data = ["VERIFY", username, password]

    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.connect(controlServerAddr)
    TCPsock.setblocking(True)

    TCPsock.send(pickle.dumps(data))
    time.sleep(0.5)

    reply = TCPsock.recv(1024)
    reply = pickle.loads(reply)

    if reply[0] == "ACCEPT":
        print("User Verified")
        
        while True:
            code = input()

            if code == "EXIT":
                data = [code]
                data = pickle.dumps(data)
                TCPsock.send(data)
                time.sleep(0.1)

                clientDict["EXIT"] = True
                TCPsock.close()
                break

            elif code == "SEND":
                sendName = input("Enter the client filename ")
                recvName = input("Enter the server filename ")
                sendName = "client/"+sendName
                recvName = "server/"+recvName
                clientDict["SENDER"] = sendName

                data = ["SEND", recvName]
                data = pickle.dumps(data)
                TCPsock.send(data)

            elif code == "RECV":
                recvName = input("Enter the client filename ")
                sendName = input("Enter the server filename ")
                recvName = "client/"+recvName
                sendName = "server/"+sendName

                clientDict["RECEIVER"] = recvName
                data = ["RECV", sendName]
                data = pickle.dumps(data)
                TCPsock.send(data)

            elif code=="LIST":
                clientDict["LIST"]=True
                data = ["LIST"]
                data = pickle.dumps(data)
                TCPsock.send(data)

            elif code =="DEL":
                name = input("Enter the name ")
                name = "server/"+name
                data = ["DEL",name]
                data = pickle.dumps(data)
                TCPsock.send(data)
            
            time.sleep(0.5)
            ack = TCPsock.recv(1024)
            ack = pickle.loads(ack)

            if ack[0]=="NOT FOUND":
                print("File not found at server")
            else:
                clientDict[code]=True


    else:
        data = ["EXIT"]
        data = pickle.dumps(data)
        clientDict["Exit"] = True

        TCPsock.send(data)
        time.sleep(0.1)
        TCPsock.close()
        return

    return


if __name__=='__main__':
    dataClientAddr = ('127.0.0.4', 8022)
    dataServerAddr = ('127.0.0.5', 8022)
    clientDict = dict()
    t1 = Thread(target=controlClientRoutine, args=[clientDict])
    keys = ["EXIT", "SEND", "RECV", "SENDER", "RECEIVER","LIST"]

    for k in keys:
        clientDict[k] = False

    t1.start()

    while True:
        if clientDict["EXIT"]:
            break

        if clientDict["SEND"]:
            fil = clientDict["SENDER"]
            t2 = Thread(target=dataSendOp, args=[
                        fil, dataClientAddr, dataServerAddr])
            t2.start()
            t2.join()
            clientDict["SEND"]=False

        if clientDict["RECV"]:
            fil = clientDict["RECEIVER"]
            t2 = Thread(target=dataRecvOp, args=[
                        fil, dataServerAddr, dataClientAddr])
            t2.start()
            t2.join()
            clientDict["RECV"]=False

        if clientDict["LIST"]:
            t2 = Thread(target=listRecvOp, args=[
                        dataServerAddr, dataClientAddr])
            t2.start()
            t2.join()
            clientDict["LIST"]=False

        time.sleep(1)

    t1.join()
