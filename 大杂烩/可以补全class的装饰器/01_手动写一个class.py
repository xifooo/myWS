#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   01_手动写一个class.py
@Time    :   2022/10/26 22:36:02
'''

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
    def __ne__(self, __o: object):
        '''重载运算符: !='''
        result = self.__eq__(__o)
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result
    def __lt__(self, __o:object):
        '''重载运算符: <'''
        if __o.__class__ is self.__class__:
            return (self.id, self.text) < (__o.id, __o.text)
        else:
            return NotImplemented
    def __le__(self, __o:object):
        '''重载运算符: <='''
        if __o.__class__ is self.__class__:
            return (self.id, self.text) <= (__o.id, __o.text)
        else:
            return NotImplemented
    def __gt__(self, __o:object):
        '''重载运算符: >'''
        if __o.__class__ is self.__class__:
            return (self.id, self.text) > (__o.id, __o.text)
        else:
            return NotImplemented
    def __ge__(self, __o:object):
        '''重载运算符: >='''
        if __o.__class__ is self.__class__:
            return (self.id, self.text) >= (__o.id, __o.text)
        else:
            return NotImplemented

def main():
    comment = ManualComment(1, "First comment is created!")
    print(comment)
    comments = "增加新属性需要修改多处代码。不易维护。"
    print(comments)


if __name__ == "__main__":
    main()
    