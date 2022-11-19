import socket as socket
import random
import pickle
import time
from multiprocessing import Process, Manager

hostCount = 3

def insert(adj,wordList,currWord):
    if len(wordList)==0:
        return
    
    if wordList[0] not in adj[currWord].keys():
        adj[currWord][wordList[0]] = dict()
    
    temp = wordList[0]
    wordList.pop(0)
    insert(adj[currWord],wordList,temp)
    return

def assign(adj,label2ip,name2ip,currLis):
    global hostCount

    lis = reversed(currLis)
    name = ".".join(lis)
    name = name[0:-1]

    label2ip[name] = (f"127.0.0.{hostCount}", 8080)
    hostCount+=1
    
    for word in adj.keys():
        currLis.append(word)
        assign(adj[word],label2ip,name2ip,currLis)
        currLis.pop(-1)
    return


def dnsServerRoutine(label2ip,name2ip,hostAddr):

    # hostAddr = UDPsock.getsockname()
    # UDPsock.close()
    # time.sleep(1)
    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.settimeout(10)
    UDPsock.bind(hostAddr)

    start = time.time()
    cnt=0
    tempaddr = 0

    while time.time()-start<=10:
        try:
            msg,addr = UDPsock.recvfrom(1024)
            msg = pickle.loads(msg)
            cnt+=1
            if cnt==1:
                tempaddr = addr
        except Exception:
            break
        
        time.sleep(1)
        if msg[1]=="YES":
            UDPsock.sendto(pickle.dumps(msg),tempaddr)
            break

        currLis,eraseLis,adj,string = msg
        name = ".".join(reversed(eraseLis))
        print(f"At server {name}\n")
        if len(currLis)==0 and name in name2ip.keys():
            ip = name2ip[name]

            data = [ip,"YES"]
            UDPsock.sendto(pickle.dumps(data),tempaddr)
        
        elif len(currLis)>0 and currLis[0] in adj.keys():
            label = ".".join(reversed(eraseLis))
            addr = label2ip[label]

            temp = currLis[0]
            eraseLis.append(currLis[0])
            currLis.pop(0)
            data = (currLis,eraseLis,adj[temp],"NO")

            UDPsock.sendto(pickle.dumps(data),addr)

    UDPsock.close()
    return

def queryRoutine(string,label2ip,adj,hostAddr):
    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.settimeout(10)
    UDPsock.bind(hostAddr)

    currLis = list(reversed(string.split(".")))
    eraseLis = []
    addr = label2ip[""]

    data = (currLis,eraseLis,adj[""],"NO")
    UDPsock.sendto(pickle.dumps(data),addr)

    time.sleep(1)

    try:
        msg,addr = UDPsock.recvfrom(1024)
        msg = pickle.loads(msg)
        print(f"Found ip address {msg[0]}\n")

    except Exception:
        print("Ip not found\n")

    finally:
        UDPsock.close()

    return
        
if __name__ == '__main__':
    manager = Manager()
    name2ip = manager.dict()
    label2ip = manager.dict()
    label2ip[""] = ("127.0.0.1",8080)
    adj = dict()

    adj[""] = dict()
    port = 8080

    print("Enter the names and ip, -1 to stop")
    inp = input()

    while(inp!="-1"):
        name = inp.split()[0]
        ip = inp.split()[1]
        wordList = name.split(".")
        wordList.reverse()

        insert(adj,wordList,"")

        name2ip[name]=ip
        inp = input()

    assign(adj,label2ip,name2ip,[])

    x = int(input("Continue ? "))
    print(adj)

    while x!=0:

        ent = input("Enter the name to be searched ")

        queryProcess = Process(target=queryRoutine,args=(ent,label2ip,adj,("127.0.0.1",8080)))

        processDict = list()

        for key in label2ip:
            processDict.append(Process(target=dnsServerRoutine,args=(label2ip,name2ip,label2ip[key])))

        for pro in processDict:
            pro.start()
        
        queryProcess.start()

        queryProcess.join()

        for pro in processDict:
            pro.join()

        x = int(input("Continue ? "))


