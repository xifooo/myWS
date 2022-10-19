class A:
    def say(self):
        print('A')
        
class B:
    def say(self):
        print('B')
        
class C(A):
    pass

class D(C,B):
    pass

class M(D):
    pass

m = M()
print(M.mro())
m.say()