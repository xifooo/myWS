import time, random


# def insertsort(A):
#     '''插入排序'''
#     for i in range(1,len(A)):
#         current = A[i]  # 取第二个元素, 跟前一个元素比大小
#         pre_index = i - 1   
        
#         while pre_index >= 0 and A[pre_index] > current:    # 若当前元素比前一元素小, 则前一元素覆盖当前元素
#             A[pre_index + 1] = A[pre_index]
#             pre_index -= 1  # 继续往前退(默认先前的序列已经排好序了)，
            
#         A[pre_index + 1] = current
#     return A

# # A=[62,83,1,90,123,17,18,1,23]
# A={x:random.uniform(0,9999) for x in range(1999)}
# B=[x for x in A.values()]
# # print(f'started at {time.strftime("%X")}')
# # print(f'finished at {time.strftime("%X")}')
# print(insertsort(B))
# o(n**2)

def insertsort_pro(A):
    '''折半查找+插入排序=插入排序的优化'''
    for i in range(1,len(A)):
        current = A[i]
        low,high = 0,i-1
        while low <= high:   # 开始折半查找
            mid = (high-low)//2
            if A[mid] < current:
                low = mid+1
            else:
                high = mid-1
        for j in range(low,i):    # 停止折半查找, 将[low,i-1]的元素全部后移一位
            A[j] = A[j-1]
        A[low] = current
C={x:random.randint(0,9999) for x in range(99)}
print(insertsort_pro(C))
# o(n**2)