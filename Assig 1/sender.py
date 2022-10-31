from utils import *
from VRC import *
from LRC import *
from CRC import *
from Checksum import *
import json


class sender:
    def __init__(self,blocksize):
        self.blocksize = blocksize
    
    def get_string(self,pathname):
        self.pathname = pathname
        with open(self.pathname,"r") as f:
            self.string = f.readlines()[0]
        self.encoded_string = encode_string(self.string,self.blocksize)
        self.json_path = "channel.json"
    
    def send(self,method,noise=None,bit_pos=None):
        if method == 'VRC':
            with open(self.json_path,"w") as f:
                json.dump(VRC(self.blocksize).encode(self.encoded_string,noise,bit_pos),f)
        elif method == 'LRC':
            with open(self.json_path, "w") as f:
                json.dump(LRC(self.blocksize).encode(self.encoded_string,noise,bit_pos), f)
        elif method == 'CRC':
            with open(self.json_path, "w") as f:
                json.dump(CRC(self.blocksize).encode(self.encoded_string,noise,bit_pos), f)
        elif method == 'Checksum':
            with open(self.json_path, "w") as f:
                json.dump(Checksum(self.blocksize).encode(self.encoded_string,noise,bit_pos), f)        