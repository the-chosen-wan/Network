import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager

def randomMac():
    return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))

#frame format [physical,TTL]

def relayStationRoutine(i,serverInd,visited):
    host = f"127.0.0.{i}"
    port = 8080

    host1 = f"127.0.0.{i}"
    port1 = 8081

    serverHost = f"127.0.0.{serverInd}"
    serverPort = 8080

    start = time.time()

    UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDPsock.settimeout(15)
    UDPsock.bind((host,port))

    UDPsock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock1.settimeout(15)
    UDPsock1.bind((host1, port1))

    while time.time()-start<=15:
        
        try:
            msg,addr = UDPsock.recvfrom(1024)
        except Exception:
            break

        msg = pickle.loads(msg)

        if msg[1]==0:
            continue
        
        msg[1]-=1

        print(f"Message reached relay station {i}")
        print()
        time.sleep(1)

        UDPsock.sendto(pickle.dumps(msg),(serverHost,serverPort))
        # time.sleep(0.5)
        try:
            msg,addr = UDPsock1.recvfrom(1024)
        except Exception:
            break

        while addr[0]!=serverHost:
            try:
                time.sleep(0.5)
                msg,addr = UDPsock.recvfrom(1024)
            except Exception:
                break

        msg = pickle.loads(msg)
        try:
            UDPsock1.sendto(pickle.dumps(msg),(msg[0],port))
        except Exception:
            pass

    UDPsock.close()
    UDPsock1.close()

def bootpServerRoutine(i,table):
    host = f"127.0.0.{i}"
    port = 8080

    start = time.time()

    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.settimeout(15)
    UDPsock.bind((host, port))
    cnt = 0
    msg=[0,0]
    addr = [0,0]

    while time.time()-start<=15:
        if cnt==0:
            try:
                msg,addr = UDPsock.recvfrom(1024)
            except Exception:
                break

            msg = pickle.loads(msg)
        
        if cnt==0:
            print(f"Message reached bootp server")
            print()
        time.sleep(1)

        cnt+=1
        
        if cnt==1:
            physicalAddr = msg[0]
            ipAddr = table[physicalAddr]
            msg = [ipAddr]

            UDPsock.sendto(pickle.dumps(msg),(addr[0],port+1))

    UDPsock.close()

def nodeRoutine(i,adj,visited):
    host = f"127.0.0.{i}"
    port = 8080

    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.settimeout(15)
    UDPsock.bind((host, port))

    start = time.time()
    msg=[0,0]
    addr = [0,0]

    while time.time()-start<=15:
        try:
            msg,addr = UDPsock.recvfrom(1024)
            msg = pickle.loads(msg)
        except Exception:
            break
        
        print(f"Message received at {i}")
        time.sleep(1)

        if msg[1]==0:
            continue

        msg[1]-=1

        for ip in adj[host]:
            if visited[ip]:
                continue

            UDPsock.sendto(pickle.dumps(msg),(ip,port))
            visited[ip]=True

    UDPsock.close()

def queryRoutine(i,physical,adj,visited):

    host = f"127.0.0.{i}"
    port = 8080
    visited[host]=True

    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.settimeout(15)
    UDPsock.bind((host, port))

    start = time.time()
    msg = [0, 0]
    addr = [0, 0]

    print(f"Initializing query node {i}")
    print()
    time.sleep(1)

    msg = [physical,12]

    for ip in adj[host]:
        if not visited[ip]:
            UDPsock.sendto(pickle.dumps(msg),(ip,port))
            visited[ip]=True

    try:
        msg,addr = UDPsock.recvfrom(1024)
        msg = pickle.loads(msg)
        print(f"Ip address of node is {msg[0]}")

    except Exception:
        print(f"Ip not found")

    finally:
        print()
        UDPsock.close()

if __name__=='__main__':
    n = int(input("Enter number of nodes "))
    m = int(input("Enter number of edges "))
    manager = Manager()

    ind2mac = {i: randomMac() for i in range(1, n+1)}
    ind2ip = {i:f"127.0.0.{i}" for i in range(1,n+1)}
    adj = {ind2ip[i]:[] for i in range(1,n+1)}
    table = {ind2mac[i]:ind2ip[i] for i in range(1,n+1)}
    visited = manager.dict()

    for ip in ind2ip.values():
        visited[ip]=False

    print("Enter the edges")

    for i in range(m):
        st = input()
        e1 = int(st.split(" ")[0])
        e2 = int(st.split(" ")[1])

        adj[ind2ip[e1]].append(ind2ip[e2])
        adj[ind2ip[e2]].append(ind2ip[e1])

    x = int(input("Continue ? "))

    while x==1:
        start = int(input("Enter the query node: "))
        
        relays = list(map(lambda x:int(x),input("Enter the relay indices: ").split(" ")))

        server = n

        nodes = [i for i in range(1,n) if i!=start and i not in relays]

        print(start,server,relays,nodes)

        startProcess = Process(target=queryRoutine,args=(start,ind2mac[start],adj,visited))
        serverProcess = Process(target=bootpServerRoutine,args=(n,table))
        relayProcesses = [Process(target=relayStationRoutine,args=(i,n,visited)) for i in relays]
        nodeProcesses = [Process(target=nodeRoutine,args=(i,adj,visited)) for i in nodes]

        for r in relayProcesses:
            r.start()
        for n1 in nodeProcesses:
            n1.start()
        serverProcess.start()
        startProcess.start()

        startProcess.join()
        serverProcess.join()

        for r in relayProcesses:
            r.join()
        for n1 in nodeProcesses:
            n1.join()

        for ip in ind2ip.values():
            visited[ip] = False
        
        x = int(input("Continue ? "))






