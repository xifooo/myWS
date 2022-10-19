class FuncDescr:
    def __get__(self, *args):
        def f(self, data):
            print(self.name)
            print(data)
        return f
    
class A:
    f = FuncDescr()
    
    
o = A()
o.name = "Bob"
# 哪个是对的?
o.f(o, "hello")
o.f("hello")
