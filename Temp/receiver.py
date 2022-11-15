import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from collections import deque
from threading import Thread, Lock
import tempfile
import os
windowSize = 3

if __name__=='__main__':
    UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDPsock.bind(("127.0.0.2",8081))
    sendAddr = ("127.0.0.1",8082)
    recCnt = 1

    while True:
        data,addr = UDPsock.recvfrom(1024)
        data = pickle.loads(data)

        seqno = data[1]
        data = data[0]


        recno = seqno+1#%windowSize

        p = random.random()
        if p<0.3:
            continue

        if recno==recCnt:
            sendData = pickle.dumps([recno])
            UDPsock.sendto(sendData,sendAddr)
            print(f"Received data {data} and seqno {seqno}")
            recCnt+=1
