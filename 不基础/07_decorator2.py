import time

def timeit(iteration):
    
    def inner(f):
        
        def wrapper(*args, **kwargs):
            start = time.time()
            for _ in range(iteration):
                ret = f(*args, **kwargs)
            print(time.time() - start)
            return ret
        return wrapper
    
    return inner

@timeit(1000)
def double(x):
    return x*2

inner = timeit(1000)
double = inner(double)