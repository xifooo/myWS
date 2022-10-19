import random


# 前提：有序的顺序表
# 折半(二分)查找
def binary_search(key, lst):
    low, high = 0, len(lst)
    
    if lst[0] > lst[len(lst)-1]:
        low, high = high, low

    while(low<=high):
        mid = (low+high)//2
        if lst[mid] == key:
            return mid
        elif lst[mid] > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1


if __name__ == "__main__":
    a = int(input())
    # L = random.sample(range(1000123),k=100)
    L = [2,14,66,21,1,56,8,3,0]
    # 可变序列用: random.shuffle(lst)
    print(binary_search(a, sorted(L,reverse=True)))