__name__ = 'quick sort'
'''最好:o(nlog2n)  最坏:o(n^2)  平均:o(nlogn)'''

def partition(A, low:int, high:int):
    pivot = A[low]
    while low < high:
        while (low < high) and (pivot <= A[high]):    # high 大
            high -= 1
        A[low] = A[high]
        while (low < high) and (pivot > A[low]):   # low 小
            low += 1
        A[high] = A[low]
        # high 小, low 大
    A[low] = pivot
    return low

def quicksort2(A, low:int, high:int):
    if low < high:
        piv = partition(A, low, high)
        quicksort2(A, low, piv-1)
        quicksort2(A, piv+1, high)
    return A

A = [62,83,1,90,123,17,18,1,23]
quicksort2(A, 0, len(A)-1)
print(A)