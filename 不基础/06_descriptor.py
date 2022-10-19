class Name:     
    # descriptor, as __get\set\delete__ method
    def __get__(self, obj, objtype):
        return 'Peter'

class A:
    # class.attr
    name = Name()
    
class B:
    # self.attr
    def __init__(self) -> None:
        # 没有触发descriptor
        self.name = Name()
        
print(A.name)
o = A()
print(o.name)
print(o.__dict__)
p = B()
print(p.name)
print(p.__dict__)