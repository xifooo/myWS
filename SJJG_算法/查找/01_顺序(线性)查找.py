a = input()
lst = [1,2,3,4,5,"rot"]
for i,j in enumerate(lst):
    if a == str(j):
        print(f"目标 {a} 在序列{lst}中的位置是{i}")
