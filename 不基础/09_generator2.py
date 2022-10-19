def gen(num):
    while num > 0:
        tmp = yield num
        if tmp is not None:
            num = tmp
        num -= 1
        
g = gen(5)

first = next(g)     # first = g.send(None)
print(f'first:{first}')

# send 之前必须
print(f'send:{g.send(10)}')

for i in g:
    print(i)