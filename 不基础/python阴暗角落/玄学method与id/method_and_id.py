class C:
    def f(self):
        ...

o = C()

# 实验1
a = id(o.f)
b = id(o.f)
print(a,b)

# 实验2
a = id(o.f)
print(a)
b = id(o.f)
print(a,b)


"""
py3.8, 实验2里第二个print的效果是a=b, py3.9里却不是
"""
# function object, function method, method function
