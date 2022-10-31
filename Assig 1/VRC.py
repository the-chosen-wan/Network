from utils import encode_string,get_parity,get_noise

class VRC:
    def __init__(self,block):
        self.block=block

    def encode(self,s,noise = None,bit_pos=None):
        #s = encode_string(s,self.block)
        l = len(s)
        for i in range(l):
            s[i] += get_parity(s[i])
            if noise is not None:
                s[i] = get_noise(s[i],noise, bit_pos)
        return s
    
    def decode(self,s):
        l = len(s)
        check = True
        for i in range(l):
            parity = get_parity(s[i][0:self.block])
            if parity!=s[i][-1]:
                check = False
            s[i] = s[i][0:-1]
        return check,s
        

# if __name__=='__main__':
#     print(VRC(8).encode("Network lab"))