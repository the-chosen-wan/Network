from threading import Thread

def func():
    i = input()
    print(i)

if __name__=='__main__':
    t = Thread(target=func,args=[])
    t.start()
    print("Hey")
    t.join()

