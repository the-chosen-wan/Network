import socket
import sys
import time
import copy
from collections import deque
import threading


sentframes = dict()
returnlist = dict()
total_data = deque()
window_size = 4
count = 0
nak_count=1000
sending=False


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
    data = input()
    while data != "q":
        frame = createFrame(data)
        frame = frame+'/'+str(count)
        count = (count+1) % window_size
        total_data.append(frame)
        data = input()
    return


def keep_sending(mySocket):
    while True:
        global sentframes
        global total_data
        global window_size
        global nak_count
        global sending

        if len(sentframes.keys()) == 0:
            temp = copy.deepcopy(total_data)
            nak_count = min(window_size, len(total_data))
            sending=True
            for i in range(min(window_size, len(total_data))):
                f = temp[0]
                seqno = return_seqno(f)
                print(f"Sent frame {seqno}")
                sentframes[seqno]=[f,"not_received"]
                temp.popleft()
                time.sleep(0.2)
                mySocket.send(f.encode())
            sending=False
            total_data = temp


def do_receive(mySocket):
    while True:
        if not sending:
            global returnlist
            ret = mySocket.recv(1024).decode()
            ret = ret.split(":")
            ret = ret[0:-1]
            # print(ret)
            for r in ret:
                returnlist[return_seqno(r)]=r


def try_resending(mySocket):
    while True:
        global returnlist
        global sentframes
        global nak_count
        global sending
        if len(returnlist.keys()) == nak_count:
            nak_count=0
            temp = copy.deepcopy(returnlist)
            nak_received = False
            for seqno,frame in temp.items():
                if return_data(frame)=='nak':
                    nak_received=True
                else:
                    try:
                        sentframes[seqno][1]='received'
                    except Exception:
                        pass


            if nak_received:
                print("Resending required")

            returnlist = dict()
            nak_received = False

            sending=True
            senttemp = copy.deepcopy(sentframes)
            for seqno,lis in senttemp.items():
                if lis[1]=='not_received':
                    nak_count+=1
                    nak_received=True
                    print(f"Resent frame {seqno}")
                    time.sleep(2)
                    mySocket.send(sentframes[seqno][0].encode())
                elif nak_received==False:
                    del sentframes[seqno]
                    print(f"Successfully sent frame {seqno}")
            sending=False

        time.sleep(1)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    mySocket = socket.socket()
    mySocket.connect((host, port))
    count = 0
    sn = 0
    t1 = threading.Thread(target=do_receive, args=[mySocket])
    t2 = threading.Thread(target=try_resending, args=[mySocket])
    t3 = threading.Thread(target=keep_sending, args=[mySocket])

    take_input()
    t3.start()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    t3.join()
