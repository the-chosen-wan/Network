from utils import *
import json

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0: pick]

    while pick < len(divident):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            tmp = xor('0'*pick, tmp) + divident[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    checkword = tmp
    return checkword

class CRC:
    def __init__(self,blocksize):
        self.blocksize = blocksize
        with open("configs.json","r") as f:
            index_list = json.load(f)["CRC_poly"]
        self.degree = index_list[0]
        self.str = ""
        for i in range(self.degree+1):
            if i in index_list:
                self.str+=str(1)
            else:
                self.str+=str(0)
        self.str = self.str[::-1]
        
    def encode(self,s,noise=None,bit_pos=None):
        l = len(s)

        for i in range(l):
            appended = s[i]+'0'*(self.degree)
            codeword = mod2div(appended, self.str)
            s[i] += codeword

            if noise is not None:
                s[i] = get_noise(s[i],1,bit_pos)

        return s
    
    def decode(self,s):
        l = len(s)
        check = True
        for i in range(l):
            appended = s[i][0:self.blocksize]+'0'*(self.degree)
            codeword = mod2div(appended,self.str)
            if codeword!=s[i][self.blocksize:]:
                check=False
        return check,s


