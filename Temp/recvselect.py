import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager
from collections import deque
from threading import Thread, Lock
import tempfile
import os

Rf = 0
Rn = 0
windowSize = 4

if __name__=='__main__':
    UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDPsock.bind(('127.0.0.2',8081))
    sendAddr = ('127.0.0.1',8082)
    marked = [False for i in range(1000)]

    while True:
        data,addr = UDPsock.recvfrom(1024)
        data = pickle.loads(data)
        seqno = data[1]
        data = data[0]

        p = random.random()

        if p<0.7:
            ret = ["ACK",seqno]
            ret = pickle.dumps(ret)
            UDPsock.sendto(ret,sendAddr)

            marked[seqno] = True

            if seqno==Rn:
                Rn+=1

        else:
            ret = ["NAK",seqno]
            ret = pickle.dumps(ret)
            UDPsock.sendto(ret,sendAddr)

        while marked[Rf]:
            print(f"Delivered data from frame {Rf}")
            Rf+=1
        

            

