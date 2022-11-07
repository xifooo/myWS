#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   02_total_ordering.py
@Time    :   2022/10/26 22:37:26
'''
from functools import total_ordering


@total_ordering
class ManualComment:
    def __init__(self,id:int, text:str) -> None:
        self.__id : int = id
        self.__text : str = text
        
    @property
    def id(self):
        return self.__id
    
    @property
    def text(self):
        return self.__text
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} id = {self.id}, text = {self.text}"
    
    def __hash__(self) -> int:
        ''' ManualComment 现在可以放入字典中了 '''
        return hash((self.__class__, self.id, self.text))
    
    def __eq__(self, __o: object) -> bool:
        '''重载运算符: =='''
        if __o.__class__ is self.__class__:
            return (self.id, self.text) == (__o.id, __o.text)
        else:
            return NotImplemented
    # def __ne__(self, __o: object):
    #     '''重载运算符: !='''
    #     result = self.__eq__(__o)
    #     if result is NotImplemented:
    #         return NotImplemented
    #     else:
    #         return not result
    # def __lt__(self, __o:object):
    #     '''重载运算符: <'''
    #     if __o.__class__ is self.__class__:
    #         return (self.id, self.text) < (__o.id, __o.text)
    #     else:
    #         return NotImplemented
    # def __le__(self, __o:object):
    #     '''重载运算符: <='''
    #     if __o.__class__ is self.__class__:
    #         return (self.id, self.text) <= (__o.id, __o.text)
    #     else:
    #         return NotImplemented
    # def __gt__(self, __o:object):
    #     '''重载运算符: >'''
    #     if __o.__class__ is self.__class__:
    #         return (self.id, self.text) > (__o.id, __o.text)
    #     else:
    #         return NotImplemented
    # def __ge__(self, __o:object):
    #     '''重载运算符: >='''
    #     if __o.__class__ is self.__class__:
    #         return (self.id, self.text) >= (__o.id, __o.text)
    #     else:
    #         return NotImplemented
    

def main():
    ...


if __name__ == "__main__":
    main()