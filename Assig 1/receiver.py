from utils import *
from VRC import *
from LRC import *
from CRC import *
from Checksum import *
import json


class receiver:
    def __init__(self,blocksize):
        self.blocksize = blocksize
    
    def get_string(self):
        self.json_path = "channel.json"
        with open(self.json_path,"r") as f:
            self.encoded_string = json.load(f)
    
    def decode(self,method):
        if method=="VRC":
            check,s = VRC(self.blocksize).decode(self.encoded_string)
            if check==False:
                print("Error detected")
            else:
                print("No error detected")
        
        if method == "LRC":
            check, s = LRC(self.blocksize).decode(self.encoded_string)
            if check == False:
                print("Error detected")
            else:
                print("No error detected")

        if method == "CRC":
            check, s = CRC(self.blocksize).decode(self.encoded_string)
            if check == False:
                print("Error detected")
            else:
                print("No error detected")
        if method == "Checksum":
            check, s = Checksum(self.blocksize).decode(self.encoded_string)
            if check == False:
                print("Error detected")
            else:
                print("No error detected")
