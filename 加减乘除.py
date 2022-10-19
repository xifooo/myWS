# a+b=a^b+(a&b)<<1
# 加法的含义可以拆分为a^b安位取异或，即不同的位上进行相加；(a&b)<<1表示同位的1进行进一位。中间的加号可以通过递归实现。

# 加法是其他计算的基础： 减、乘、除。
def add(a, b):  # # 加法的感念就是 a+b = a^b+(a&b)<<1
    if b == 0:    return a
    c = a ^ b & 0xFFFFFFFFFFFF          # 负数会溢出，所以用32位的最大数进行限制。
    d = ( (a & b) << 1 ) & 0xFFFFFFFFFFFF    # 0xFFFFFFFF=(2**31)-1 进行限定位数。
    if d!=0:
        res = add(c, d)
    else:
        res = c
    return res


# a－b＝a+(-b)
# -b=~b+1  这样就可以通用加法的来完成减法了。
# # 判断大小的作用是防止因为负数导致的位数溢出。
def minus(a,b):  # 减法的感念就是 a-b = a+(-b)=a+(~(b-1))= a^(~(b-1))+(a&(~(b-1)))<<1
    if a>=b:    return add(a,add(~b,1))
    else:      return add(~add(b,add(~a,1)),1)


# 乘法ab可以看成是每个b的每个位数与a的乘积之和。又，由于都是二进制，b的位数上要么是0要么是1，如果是a0则乘积为0，如果是a*1则乘积是a。
# 正负号的问题，则由逻辑判断确定：如果a^b>=0 说明最高位是0，是正数，反之为负数。
def multiply(a,b):
    flag = True if a^b>=0 else False
    if a<0: a=add(~a,1)
    if b<0: b=add(~b,1)
    res = 0
    while b>0:
        if b & 1:
            res = add(res,a)
        a <<= 1
        b >>= 1
    res = res if flag else add(~res,1)
    return res


# a/b 是除法，主要思想是用减法，a不断地减去b，最后如果a<b，得到余数，商则通过减去b的次数的总和得到。又，由于都是二进制，所以为了加快速度，可以对b取（2**n）倍，这个倍数真好是左移实现<<n。
# 同样，正负问题由a^b的逻辑判断确定。
def divide(a,b):
    flag = True if a ^ b >= 0 else False
    if a<0: a = add(~a,1)
    if b<0: b = add(~b,1)
    res = 0 
    for i in range(31,-1,-1):
        if a >= (b<<i):
            res = add(res,1<<i)
            a = minus(a, b<<i)
    res = res if flag else add(~res,1)
    return res


# a％b，即求余数。返回除法中最后的a即可。正负号由最初的a的正负决定。

def divide_remain(a,b):
    flag = True if a >= 0 else False
    if a<0: a = add(~a, 1)
    if b<0: b = add(~b, 1)
    res = 0
    for i in range(31, -1, -1):
        if a >= (b << i):
            res = add(res, 1 << i)
            a = minus(a, b<<i)
    a = a if flag else add(~a, 1)
    return a

print(add(10,19))
