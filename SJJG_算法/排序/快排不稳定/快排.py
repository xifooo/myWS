# import random


def quick_sort(lst, low, high):
    if low >= high:
        return
    cur_ele = lst[low]
    
    left, right = low, high
    
    while low < high:
        # 处理右边的
        while (low < high) and (lst[high] >= cur_ele):
            high -= 1
        lst[low] = lst[high]
        # 处理左边的
        while (low < high) and (lst[low] <= cur_ele):
            low += 1
        lst[high] = lst[low]
    # low=high时完成一次全处理/划分
    lst[high] = cur_ele
    # 对两边分别进行全处理/划分
    quick_sort(lst, left, low - 1)
    quick_sort(lst, low + 1 , right)


# def quick_sort(lists,i,j):
#     if i >= j:
#         return list
#     pivot = lists[i]
#     low = i
#     high = j
#     while i < j:
#         while i < j and lists[j] >= pivot:
#             j -= 1
#         lists[i]=lists[j]
#         while i < j and lists[i] <=pivot:
#             i += 1
#         lists[j]=lists[i]
#     lists[j] = pivot
#     quick_sort(lists,low,i-1)
#     quick_sort(lists,i+1,high)
#     return lists

A = [2,14,66,21,1,56,8,3,0]
l = len(A)-1
quick_sort(A, 0, l)
print(A)