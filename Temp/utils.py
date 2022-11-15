import copy

def andAndAdd(s,blockSize):
    andVal = (1<<blockSize)-1
    temp = s&andVal
    shiftVal = s-temp

    shiftVal = shiftVal>>blockSize
    s=shiftVal+temp
    return s,shiftVal

def getBin(s):
    ret = []
    check = (1<<8)
    
    while s!=0:
        if s>=check:
            ret.append("1")
            s-=check
        else:
            ret.append("0")
        check/=2
    return "".join(ret)

def checkSum(blocks):
    blockSize = len(blocks[0])
    s=0

    for i in range(len(blocks)):
        s+=int(blocks[i],2)


    s,temp = andAndAdd(s,blockSize)

    while temp!=0:
        s,temp = andAndAdd(s,blockSize)
    s = (1<<blockSize)-1-s
    blocks.append(getBin(s))

    s=0

    for i in range(len(blocks)):
        s += int(blocks[i], 2)

    s, temp = andAndAdd(s, blockSize)

    while temp != 0:
        s, temp = andAndAdd(s, blockSize)
    s = (1 << blockSize)-1-s
    print(s)
    
    return blocks

def getBinary(s):
    return "".join(format(ord(c),'08b') for c in s)

def xor(a,b):
    l = len(a)
    ret = []
    for i in range(l):
        ret.append(str(int(a[i])^int(b[i])))
    ret="".join(ret)
    return ret

def mod2div(dividend,divisor):
    l = len(dividend)
    pick = len(divisor)

    temp = list(copy.deepcopy(dividend))
    quotient = ""
    cnt = 0

    while cnt<=l-pick:
        if temp[cnt]=="0":
            quotient+="0"
        else:
            quotient+="1"
            temp[cnt:cnt+pick] = xor(temp[cnt:cnt+pick],divisor)
        cnt+=1
    
    remainder = temp[l-pick+1:l]
    return quotient,"".join(remainder)

def crcEncoder(s,polyLis):
    l = max(polyLis)
    divisor = ["1" if i in polyLis else "0" for i in range(l+1)]
    s+="0"*(l+1)

    quo,rem = mod2div(s,divisor)
    s = list(s)
    s[len(s)-len(rem):len(s)]=rem
    s = "".join(s)

    quo,rem = mod2div(s,divisor)
    return s,rem


def getBlocks(s,blockSize):
    ret = []
    for i in range(0,len(s),blockSize):
        ret.append(s[i:i+blockSize])

    if len(ret[-1])!=blockSize:
        while len(ret[-1])!=blockSize:
            ret[-1]+="0"

    return ret


def getParity(s):
    cnt  = 0
    for i in range(len(s)):
        if s[i]=="1":
            cnt^=1
    return str(cnt)

def vrcEncoder(blocks):
    l = len(blocks)
    for i in range(l):
        blocks[i]+=getParity(blocks[i])
    return blocks

def lrcEncoder(blocks):
    blockSize = len(blocks[0])
    l = len(blocks)
    ret = []

    for i in range(blockSize):
        app = 0

        for j in range(l):
            if blocks[j][i]=="1":
                app^=1
        ret.append(str(app))
    ret = "".join(ret)
    blocks.append(ret)
    return blocks


if __name__=='__main__':
    bin = getBinary("Hemlo")
    blocks = getBlocks(bin,8)
    blocks = checkSum(blocks)
    print(blocks)
