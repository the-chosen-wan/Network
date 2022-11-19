import threading
import random
import time

frameTime = 3
interFrameTime =1

numFrames = 10
totalFrames = 0


def metrics(lock, total):
    global totalFrames
    tot = 0
    used = 0
    while totalFrames < total:
        if lock.locked():
            used += 1
        tot += 1
    print(f"Channel utilization is {used/tot}")
    print()

class CSMA(threading.Thread):
    def __init__(self,lock,k,index):
        super().__init__()
        self.lock=lock
        self.k=k
        self.index=index
    
    def run(self):
        cnt=1
        global numFrames
        global totalFrames
        while cnt <= numFrames:
            print(f"Attempting to send frame {cnt} of node {self.index}")
            print()

            while self.lock.locked():
                pass
                
            self.lock.acquire()
            time.sleep(frameTime)
            print(f"Successfully sent frame {cnt} of node {self.index}")
            print()
            self.lock.release()
            totalFrames += 1
            time.sleep(interFrameTime)
            cnt+=1
        return
                    

if __name__=='__main__':
    numberNodes = int(input("Enter number of nodes: "))
    lock = threading.Lock()
    met = threading.Thread(target=metrics, args=[lock, numberNodes*numFrames])

    Nodes = [CSMA(lock,4,i+1) for i in range(0,numberNodes)]
    met.start()
    for node in Nodes:
        node.start()
    
    for node in Nodes:
        node.join()
    met.join()