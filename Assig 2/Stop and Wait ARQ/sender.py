
import socket
import sys
import time
from threading import Thread
from collections import deque

def CreateFrame(data):
    ones = 0
    for i in data:
        if i == '1':
            ones += 1
    data += str(ones % 2)
    return data


class Sender():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.socket = socket.socket()
        self.socket.connect((self.host,self.port))
        self.socket.settimeout(2)
    
    def send(self):
        while True:
            data = input("Enter the data: ")

            if data=='exit':
                break
            data = CreateFrame(data)
            timeout = True
            
            while timeout:
                prev = time.time()
                timeout = False
                self.socket.send(data.encode())

                try:
                    ret = self.socket.recv(1024).decode()
                except Exception:
                    pass

                curr=time.time()

                if curr-prev>2:
                    timeout=True
                
                if timeout:
                    print("Timeout occured")
            
            print("Sent the data")
        self.socket.close()
        return



if __name__=='__main__':
    s = Sender()
    s.send()





