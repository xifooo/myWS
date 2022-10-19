def dec(f):
    return 10000

@dec
def double(x):
    return x*2
# 完全等价于
# double = dec(double)
print(double,type(double))


import time

def timeit(f):
    
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = f(*args, **kwargs)
        print(time.time() - start)
        return ret
    
    return wrapper

@timeit
def my_func(x):
    time.sleep(x)
