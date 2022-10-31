import random

def get_binary(s):
    return ''.join(format(ord(i), '08b') for i in s)

def get_noise(s,k,bit_pos=None):
    if bit_pos is None:
        p = random.random()
        if p<0.9:
            return s
        else:
            print("Error Produced")
            l = len(s)
            indices = list(range(l))
            indices = random.sample(indices,k)
            xor = ''.join('0' if i not in indices else '1' for i in range(l))
            xor = [int(a)^int(b) for a,b in zip(s,xor)]
            ret = ""
            for i in xor:
                ret+=str(i)
            return ret
    else:
        print("Error Produced")
        l = len(s)
        xor = ''.join('0' if i not in bit_pos else '1' for i in range(l))
        xor = [int(a)^int(b) for a,b in zip(s,xor)]
        ret = ""
        for i in xor:
            ret+=str(i)
        return ret


def encode_string(s,block_size):
    #s = get_binary(s)
    l = len(s)
    assert l>=block_size

    strings = []
    for i in range(0,l,block_size):
        strings.append(s[i:i+block_size])
    
    if len(strings[-1])<block_size:
        for i in range(0,block_size-len(strings[-1])):
            strings[-1]+=str(0)
    return strings

def get_parity(s):
    l = len(s)
    c = 0
    for i in range(l):
        if s[i]=='1':
            c+=1
    return str(c%2)

if __name__ == '__main__':
    print(get_binary("Network Lab"))
    print(encode_string("Network Lab",4))
