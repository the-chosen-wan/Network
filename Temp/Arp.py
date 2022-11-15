from multiprocessing import Process
import random
import socket
import pickle
import time

def randomMac():
    return "20::00::00::%02x::%02x::%02x"%(random.randint(0,256),
                                            random.randint(0,256),
                                            random.randint(0,256))


def queryProcess(hostList):
    host = ("127.0.0.50",8080)
    mac = randomMac()

    print(f"Query node has ip 127.0.0.1 and mac {mac}")

    UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDPsock.bind(host)
    cnt = 0

    while cnt<4:
        ip = random.choice(hostList)[0]

        print(f"Querying for ip {ip}")

        frame = [host[0],mac,ip,-1]

        if cnt==4:
            frame[1]=-1
        
        frame = pickle.dumps(frame)

        for h in hostList:
            UDPsock.sendto(frame,h)


        if cnt == 4:
            break
        
        time.sleep(1)
        frame,addr = UDPsock.recvfrom(1024)
        frame = pickle.loads(frame)

        print(f"Received mac address {frame[3]}")

        time.sleep(4)
        cnt+=1

    UDPsock.close()

def nodeProcess(i):
    host = (f"127.0.0.{i}",8080)
    mac = randomMac()

    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.bind(host)

    print(f"Ip {host[0]} had mac {mac}")

    while True:
        frame,addr = UDPsock.recvfrom(1024)
        frame = pickle.loads(frame)

        if frame[1]==-1:
            break

        ip = frame[2]
        if host[0]!=ip:
            print(f"Node {i} dropping frame")
            time.sleep(4)
            continue
        
        frame[3]=mac

        time.sleep(4)
        frame = pickle.dumps(frame)
        UDPsock.sendto(frame,addr)

    UDPsock.close()

if __name__=='__main__':
    n = int(input("Enter number of nodes "))
    hostList = [(f"127.0.0.{i}",8080) for i in range(1,n+1)]

    queryProcesses = Process(target=queryProcess,args=[hostList])
    nodeProcesses = [Process(target=nodeProcess,args=[i]) for i in range(1,n)]

    for pro in nodeProcesses:
        pro.start()
    queryProcesses.start()

    for pro in nodeProcesses:
        pro.join()
    queryProcesses.join()

