'shell sort —— 希尔排序, 不稳定, 仅可适用于顺序表'

'''
先追求表中元素部分有序，再逐渐逼近全局有序
分割成形如等差数为索引值的特殊子表, 对各个子表分别进行直接插入排序
'''
from typing import Sequence
def shellsort(A:Sequence) -> Sequence:
    n = len(A)
    d = n//2
    while d > 0:
        for i in range(d,n):
            temp = A[i]
            j = i
            while j >= d and A[j-d] > temp:
                A[j] = A[j-d]
            A[j] = temp
        d = d//2
#    return A

array = [62,83,1,90,123,17,18,1,23]
shellsort(array)
print(array)
        
# 最坏o(n**2), n在某个范围内时, 可达o(n**1.3)