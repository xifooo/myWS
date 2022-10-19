' —— 快速排序 XX—— XXXXXXXXXXXX'
__name__ = '不行'

def partition(A:list, low:int, high:int):
    first = A[low]
    while low < high:
        while (A[low]<A[high]) and (A[high] >= first):
            high -= high
        while (A[low]<A[high]) and (A[high] < first):
            low += low
        A[low] = A[high]
    A[low] = first
    return low

def quicksort(A:list, low:int, high:int):
    if low < high:
        pivot = partition(A, low, high)
        quicksort(A, low, pivot-1)
        quicksort(A, pivot+1, high)
    return A


A=[62,83,1,90,123,17,18,1,23]
quicksort(A, 0, len(A)-1)
print(A)