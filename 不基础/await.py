class A:
    ...
    
class B(A):
    ...

o = A()
b = B()
print(issubclass(o,b))
