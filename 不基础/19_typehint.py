class Node:
    def __init__(self, prev:'Node') -> None:    # 'Node' 作为 string literal, 这是合法的操作, 也被 mypy 认可的
        self.prev = prev
        self.next = None
        

from typing import List, Sequence, Optional


# def my_sum(lst: list) -> int:
# def my_sum(lst: list[int]) -> int:    # 这种写法是python3.9之后才支持的
# def my_sum(lst: List[int]) -> int:      # 用 typing 里的 List ，在3.9之前也好用，不过这个 typing 在 3.9 开始的5年后就会被移除
def my_sum(lst: Sequence[int]) -> int:      # 用 typing 里的 List ，在3.9之前也好用，不过这个 typing 在 3.9 开始的5年后就会被移除
    total = 0
    for i in lst:
        total += 1
    return total

my_sum([0,1,2])
my_sum([0,1,'2'])

my_sum((0,1,'2'))   # 一般不明确指定 list、tuple、range 类型，更普遍的用法是用 Sequence , 前面的都是 Sequence 类型


def my_sum2(lst: dict[str, int]) -> int:      # 用 typing 里的 List ，在3.9之前也好用，不过这个 typing 在 3.9 开始的5年后就会被移除
    total = 0
    for i in lst:
        total += 1
    return total

my_sum2({'a':1,'b':2,'c':3})   # 传递字典类型的参数


def f(x: Optional[int]) -> int: # Optional 表示 x 还可能是 None
    if x is None:
        return 0
    return x
f(None)
f(0)

'''
1. type hint 并不会导致 runtime 成分，影响 python 代码的运行效率
2. graduall typing - 渐进式的类型标注，不必在所有的代码中加入 type hint
'''