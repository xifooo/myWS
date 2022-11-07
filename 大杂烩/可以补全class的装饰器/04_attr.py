#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   04_attr.py
@Time    :   2022/10/31 11:12:55
'''

import attr, pprint, inspect


@attr.s(frozen=True, order=True)
class Comment:
    id : int = attr.ib(validator=attr.validators.instance_of(int))
    text : str = attr.ib(default="", converter=str)
    replies : list[int] = attr.ib(factory=list, order=False, hash=False, repr=False)


def main():
    comment = Comment(1,"hello")
    print(comment)
    
    pprint(inspect.getmembers(Comment,inspect.isfunction))


if __name__ == "__main__":
    main()
