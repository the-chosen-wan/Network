from utils import *

class LRC:
    def __init__(self,blocksize):
        self.blocksize = blocksize
    
    def encode(self,s,noise=None,bit_pos=None):
        l = len(s)
        vec = ""
        for i in range(self.blocksize):
            temp = ""
            for j in range(l):
                temp+=s[j][i]
            vec+=get_parity(temp)
        if noise is not None:
            for i in range(l):
                s[i] = get_noise(s[i],1,bit_pos)
        s.append(vec)
        return s
    
    def decode(self,s):
        l = len(s)
        vec = s[-1]
        s = s[0:l-1]
        l = l-1
        check = True
        for i in range(self.blocksize):
            temp = ""
            for j in range(l):
                temp+=s[j][i]
            if vec[i]!=get_parity(temp):
                check = False
        return check,s