import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from collections import deque
from threading import Thread,Lock
import tempfile
import os

if __name__ == '__main__':
    TCPsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPsock.bind(('127.0.0.1',8081))
    TCPsock.listen(1)

    conn,addr = TCPsock.accept()
    tempList = []

    while True:
        char = conn.recv(1024)

        char = pickle.loads(char)

        if char[0]=='0':
            if char[1]=='$':
                data = "".join(tempList)
                tempList = []
                print(data)
                if data=="exit":
                    break
            
            else:
                tempList.append(char[1])
    
    conn.close()
    TCPsock.close()
