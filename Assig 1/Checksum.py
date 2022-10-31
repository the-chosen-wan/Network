from utils import *

class Checksum:
    def __init__(self,blocksize):
        self.blocksize = blocksize
        self.mod = 1<<(self.blocksize+1)
    
    def encode(self,s,noise=None,bit_pos=None):
        l = len(s)
        sum = 0
        for i in range(l):
            sum = sum + int(s[i],2)
        sum = sum%self.mod
        sum = self.mod-sum
        if noise is not None:
            for i in range(l):
                s[i] = get_noise(s[i],1,bit_pos)
        s.append(str(bin(sum)))
        return s
    
    def decode(self,s):
        l = len(s)
        temp = 0
        check = True

        for i in range(l):
            temp = temp+int(s[i],2)
        if temp!=0:
            check = False
        s = s[0:l-1]
        return check,s
