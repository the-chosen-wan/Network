import socket
import sys
import time
import copy
from collections import deque
import threading

sentframes = deque()
returnlist= deque()
total_data=deque()
window_size=3
count=0


def createFrame(data):
    countOnes = 0
    for ch in data:
        if ch == '1':
            countOnes += 1
    data += str(countOnes % 2)
    return data

def return_seqno(data):
    return int(data.split('/')[-1])

def return_data(data):
    return data.split('/')[0]

def take_input():
    global count
    global total_data
    global window_size
    print("Enter q to stop")
    data=input()
    while data!="q":
        frame=createFrame(data)
        frame=frame+'/'+str(count)
        count=(count+1)%window_size
        total_data.append(frame)
        data = input()
    return

def keep_sending(mySocket):
    while True:
        global sentframes
        global total_data
        global window_size

        if len(sentframes)==0:
            temp=copy.deepcopy(total_data)
            for i in range(min(window_size,len(total_data))):
                f=temp[0]
                seqno=return_seqno(f)
                print(f"Sent frame {seqno}")
                sentframes.append(f)
                temp.popleft()
                time.sleep(0.2)
                mySocket.send(f.encode())
            total_data=temp


def do_receive(mySocket):
    while True:
        global returnlist
        ret=mySocket.recv(1024).decode()
        ret = ret.split(":")
        ret=ret[0:-1]
        returnlist.extend([l.split('/')[0] for l in ret])

def try_resending(mySocket):
    while True:
        global returnlist
        global sentframes
        if len(returnlist)==len(sentframes):
            temp=copy.deepcopy(returnlist)

            timeout=False
            for t in temp:
                if t=="timeout":
                    timeout=True
                    break
                else:
                    returnlist.popleft()
                    fr=sentframes[0]
                    print(f"Successfully Sent frame {return_seqno(fr)}")
                    sentframes.popleft()
                
            if timeout:
                print("Resending required")
            
            returnlist = deque()
            for fr in sentframes:
                mySocket.send(fr.encode())
                time.sleep(2)
                print(f"Resending frame {return_seqno(fr)}")
                time.sleep(0.2)
        time.sleep(1)
    

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    mySocket = socket.socket()
    mySocket.connect((host, port))
    count = 0
    sn = 0
    t1=threading.Thread(target=do_receive,args=[mySocket])
    t2=threading.Thread(target=try_resending,args=[mySocket])
    t3=threading.Thread(target=keep_sending,args=[mySocket])

    take_input()
    t3.start()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    t3.join()






