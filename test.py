def test(a):

    try:
        pro(a)

    except:
        print('wront')


def pro(a):
    newL=[]

    for i in range(4):
        print(a[i])
        newL.append(i)

    return NewL
        


test([1,2,3])


from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp

#array = mp.Array()
#l = mp.Lock()
que = mp.Queue()
pool = ThreadPool()
outcome = pool.map(test, [[1,4,2] for i in range(10)])
pool.close()
pool.join()


