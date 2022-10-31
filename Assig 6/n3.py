import socket as socket
import random
import pickle
import time

host = "127.0.0.5"
port = 8080
physical = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))
                                        
print(f"Physical address of host {host} is {physical}")

if __name__ == '__main__':
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

