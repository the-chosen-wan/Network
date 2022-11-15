import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from collections import deque
from threading import Thread, Lock
import tempfile
import os

if __name__ == '__main__':
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.connect(('127.0.0.1', 8081))

    print("Enter exit to stop")

    while True:
        x = input()

        lis = list(x)

        for data in lis:
            totalData = ['0',data]
            totalData = pickle.dumps(totalData)

            TCPsock.send(totalData)
            time.sleep(0.5)

        if x=="exit$":
            break
    
    TCPsock.close()

