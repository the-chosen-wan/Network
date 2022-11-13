import socket as socket
import random
import pickle
import time
from multiprocessing import Process

def query(ip_list):
    host = "127.0.0.255"
    port = 8080
    physical = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))

    UDPsock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPsock.bind((host, port))
    cnt=0
    while True:
        ip = random.choice(ip_list)

        print(f"Wanting physical address of {ip}\n")
        arp_frame = [host, physical, ip, -1]

        if cnt == 4:
            arp_frame[0] = -1

        for i in ip_list:
            tup = (i, port)

            UDPsock.sendto(pickle.dumps(arp_frame), tup)

        msg, addr = UDPsock.recvfrom(1024)
        msg = pickle.loads(msg)
        time.sleep(4)
        print(f"Received physical address is {msg[3]}\n")
        time.sleep(2)
        cnt+=1

        if cnt==5:
            break

def answer(i):
    host = f"127.0.0.{i}"
    port = 8080
    physical = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))

    print(f"Physical address of host {host} is {physical}\n")
    while True:
        UDPsock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPsock.bind((host, port))

        msg, addr = UDPsock.recvfrom(1024)
        msg = pickle.loads(msg)


        if msg[2] == host:
            msg[3] = physical
            time.sleep(4)
            UDPsock.sendto(pickle.dumps(msg), addr)

        else:
            print(f"Ip {host} dropped message")
            time.sleep(4)
        
        if msg[0] == -1:
            break

if __name__ == '__main__':
    n = int(input("Enter number of processes "))
    print()
    ip_list = [f"127.0.0.{i}" for i in range(1,n+1)]

    cq = Process(target=query,args=(ip_list,))
    ans = [Process(target=answer,args=(i,)) for i in range(1,n+1)]

    for a in ans:
        a.start()
    cq.start()

    for a in ans:
        a.join()
    cq.join()




