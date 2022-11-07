#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   03_dataclasses.py
@Time    :   2022/10/26 22:35:37
'''

from dataclasses import dataclass, astuple, asdict, field
from objprint import op
import inspect, pprint


@dataclass(frozen=True, order=True)
class Comment:
    id : int
    text : str = ""
    replis: list[int] = field(default_factory=list)
    

def main():
    comment = Comment(1, "First comment is created!")
    
    print(comment)  # __repr__返回str类型
    
    print(astuple(comment))  # __repr__返回tuple类型
    
    print(asdict(comment))  # __repr__返回dict类型
    
    op.config(arg_name=True)
    op(inspect.getmembers(Comment, inspect.isfunction))
    op(dir(comment))


if __name__ == "__main__":
    main()
    