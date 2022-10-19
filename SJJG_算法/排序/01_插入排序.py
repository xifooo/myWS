def insert_sort(seq):
    # 遍历除去首位的序列，默认为前面的序列是有序（已排序）的
    for i in range(1, len(seq)):
        key = seq[i]        # 未排序序列的首个元素
        j = i-1             # 已排序序列的末尾元素

        while key < seq[j] and j >= 0:
            seq[j+1] = seq[j] # 往后移位
            j = j-1          # 往前走
        seq[j+1] = key
        

# def insert_sort_pro(A):
#     '''插入排序+折半查找 = 插入排序的优化'''
#     for i in range(1, len(A)):
#         key = A[i]
#         low, high = 0, i-1
#         if (low == high) and A[low] >= key:
#             A[i] = A[low]
#             A[low] = key
#         # 在 "已排序序列" 中进行折半查找
#         while(low < high):
#             mid = (low+high)//2 + 1
#             if A[mid] > key:    # 左子表
#                 high = mid - 1
#             else:               # 右子表
#                 low = mid
                
#         # low+1 便是 key 的存放位置， low+1 <= i
#         j = i - 1
#         while j >= low + 1:
#             A[j+1] = A[j]
#             j -= 1

# [0,1, 2, 3, 4, 5,6,7]
# [2,14,21,66,1,56,8,3,0]
# A = [2,14,66,21,1,56,8,3,0]
# insert_sort_pro(A)
# print(A)

