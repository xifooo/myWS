def mergeSort(array):
    if len(array) > 1:

        #  r 是将数组分为两半后的分割点
        r = len(array)//2
        L = array[:r]
        M = array[r:]

        # 通过递归方法对两半进行排序
        mergeSort(L)
        mergeSort(M)

        i = j = k = 0

        # 直到我们到达 L 或 M 的任一端，从中选择较大的元素 L 和 M 并将它们放置在 A[p 到 r] 处的正确位置
        while i < len(L) and j < len(M):
            if L[i] < M[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1

        # 将L或者M里的元素排序好后，将剩余的元素并放入 A[p to r]
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1
array = [8, 6, 14, 12, 10, 3]

mergeSort(array)
print("Sorted array: ")
print(array)





A = [2,14,66,21,1,56,8,3,0]