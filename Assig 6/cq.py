import socket as socket
import random
import pickle
import time

host = "127.0.0.2"
port = 8080
physical = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))

ip_list = ["127.0.0.3", "127.0.0.4", "127.0.0.5"]

if __name__ == '__main__':
    UDPsock = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
    UDPsock.bind((host,port))

    while True:
        ip = random.choice(ip_list)

        print(f"Wanting physical address of {ip}")
        arp_frame = [host,physical,ip,-1]

        for i in ip_list:
            tup = (i,port)

            UDPsock.sendto(pickle.dumps(arp_frame),tup)

        msg,addr = UDPsock.recvfrom(1024)
        msg = pickle.loads(msg)
        time.sleep(4)
        print(f"Received physical address is {msg[3]}")
