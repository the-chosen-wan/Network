import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from threading import Thread
import os

def dataSendOp(fil,clientAddr,serverAddr):
    time.sleep(0.5)
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.connect(serverAddr)

    with open(fil, "r") as f:
        lines = f.readlines()

    TCPsock.send(str(len(lines)).encode())
    time.sleep(2)

    for line in lines:
        TCPsock.send(line.encode())
        time.sleep(2)

    TCPsock.close()

def dataRecvOp(fil,clientAddr,serverAddr):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.bind(serverAddr)
    TCPsock.listen(1)


    conn, addr = TCPsock.accept()

    num = int(conn.recv(1024).decode())
    time.sleep(2)
    op = open(fil, "w")

    for i in range(num):
        msg = conn.recv(1024).decode()
        op.write(msg)
        time.sleep(1)
        op.flush()
        time.sleep(1)

    conn.close()
    TCPsock.close()
    op.close()

def listSendOp(clientAddr,serverAddr,lis):
    time.sleep(0.5)
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.connect(serverAddr)

    lis = pickle.dumps(lis)
    TCPsock.send(lis)
    TCPsock.close()

def listRecvOp(clientAddr,serverAddr):
    time.sleep(0.5)
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.bind(serverAddr)
    TCPsock.listen(1)

    conn,addr = TCPsock.accept()
    lis = conn.recv(1024)
    lis = pickle.loads(lis)

    print(f"Received list {lis}")
    conn.close()
    TCPsock.close()



    


        
