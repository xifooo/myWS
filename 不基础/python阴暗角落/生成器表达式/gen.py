"""
list: 立刻新开一块内存
generator: 不会立刻分配内存, 而是一个一个一个往外拿
"""
# 1
lst = [1,2,3,4]
g = (n for n in lst)
print(list(g))

# 2
lst = [1,2,3,4]
g = (n for n in lst if n in lst) 
print(list(g))

# 3
lst = [1,2,3,4]
g = (n for n in lst if n in lst) 
lst = [0,1,2]
print(list(g))
# 3 等价于
lst1 = [1,2,3,4]
g = (n for n in lst1 if n in lst2) 
lst2 = [0,1,2]
print(list(g))
# 3 完全等价于这种形式:
lst = [1,2,3,4]
def __g(it):
    for n in it:
        if n in lst:    # 运行时尝试找 lst 这个变量
            yield n
g = __g(iter(lst))
lst = [0,1,2]
print(list(g))

"""
Python2.4 PEP289
惰性逻辑
推导式里只有最外层的 for表达式, 即从左往右第一个for是立刻求值的, 
而之后的、其它的表达式都是在运行时取值
"""
# 练习题
lst = [1,2,3]
g = ((a,b) for a in lst for b in lst)
lst = [1,2]
print(list(g))
