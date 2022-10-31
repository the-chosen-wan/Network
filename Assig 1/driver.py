from sender import *
from receiver import *

if __name__ == '__main__':
    print("00101011 is sent")
    print("00101001 is received")
    print("CRC polynomial is x^2")
    print("\n")

    print("Using CRC")
    send = sender(8)
    send.get_string("text.txt")
    send.send("CRC",noise=True,bit_pos=[1])
    receive = receiver(8)
    receive.get_string()
    receive.decode("CRC")
    print("\n")

    # print("Using Checksum")
    # send = sender(8)
    # send.get_string("text.txt")
    # send.send("Checksum", noise=True,bit_pos=[1])
    # receive = receiver(8)
    # receive.get_string()
    # receive.decode("Checksum")
    # print("\n")

    print("Using VRC")
    send = sender(8)
    send.get_string("text.txt")
    send.send("VRC", noise=True,bit_pos=[1])
    receive = receiver(8)
    receive.get_string()
    receive.decode("VRC")
    print("\n")

    # print("Using LRC")
    # send = sender(8)
    # send.get_string("text.txt")
    # send.send("LRC", noise=True,bit_pos=[1])
    # receive = receiver(8)
    # receive.get_string()
    # receive.decode("LRC")
