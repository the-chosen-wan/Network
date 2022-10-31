import socket
import sys
import time
import copy
from collections import deque


def createFrame(data):
	countOnes = 0
	for ch in data:
		if ch == '1':
			countOnes += 1
	data += str(countOnes % 2)
	return data


def extractMessage(frame):
	endidx = -1
	for i in range(len(frame)-1):
		if frame[i] == '/' and endidx == -1:
			endidx = i
			break
	return frame[:endidx]


class Sender:
    def __init__(self,window_size):
        self.window_size=window_size
        self.count = 0
        self.sentframes = deque()
        print('Initiating Sender #')
        host = '127.0.0.1'
        port = 8080

        self.mySocket = socket.socket()
        self.mySocket.connect((host, port))
        self.mySocket.settimeout(5)
    
    def send(self):
        while True:
            flag=False
            data=input("Enter the message ")
            data=data.split(" ")
            for d in data:
                frame=createFrame(d)
                if frame=='q0':
                    flag=True
                frame=frame+'/'+str(self.count)
                self.sentframes.append(frame)
                self.count=(self.count+1)%self.window_size
                self.mySocket.send(frame.encode())
                time.sleep(0.1)

            if flag==True:
                break

            recvlist=[]
            while True:
                try:
                    r = self.mySocket.recv(1024).decode()
                    recvlist.append(r)
                except Exception:
                    break
            
            timeout=False
            for r in recvlist:
                seqno=int(r.split('/')[0])
                timeout=r.split('/')[-1]=="timeout"

                if timeout==True:
                    break
                else:
                    fr=self.sentframes[0]
                    fr=fr.split('/')[-1]
                    print(f"Sent frame {fr}")
                    self.sentframes.popleft()

            
            while timeout:
                timeout=False
                for f in self.sentframes:
                    fr=f.split('/')[-1]
                    print(f"Resending frame {fr}")
                    self.mySocket.send(f.encode())
                    time.sleep(0.1)
                
                recvlist=[]
                while True:
                    try:
                        recvlist.append(self.mySocket.recv(1024).decode())
                    except Exception:
                        break
                
                for r in recvlist:
                    seqno=int(r.split('/')[0])
                    timeout=r.split('/')[-1]=="timeout"

                    if timeout==True:
                        break
                    else:
                        fr=self.sentframes[0]
                        fr=fr.split('/')[-1]
                        print(f"Sent frame {fr}")
                        self.sentframes.popleft()
            # seqno=int(recv.split('/')[0])
            # timeout = recv.split('/')[-1] == "timeout"

            # if seqno==self.count and timeout==False:
            #     print(f"Sent frame {(self.count-1)%self.window_size}")
            #     self.sentframes.popleft()
            # else:
            #     while timeout==True:
            #         nak_received=False
            #         timeout=False
            #         temp=copy.deepcopy(self.sentframes)

                    
            #         for f in self.sentframes:
            #             sendno=int(f.split('/')[-1])
            #             print(f"Resending frame {sendno}")

            #             self.mySocket.send(f.encode())
            #             recv=self.mySocket.recv(1024).decode()

            #             timeout = recv.split('/')[-1] == "timeout"
            #             if timeout==True:
            #                 nak_received=True

            #             if nak_received==False:
            #                 temp.popleft()
            #         self.sentframes=temp

        self.mySocket.close()
        return

if __name__=='__main__':
    s=Sender(7)
    s.send()
