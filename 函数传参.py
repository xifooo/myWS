def f(a=1, b=1, /,*, args=1, **kwargs):
    # for i in kwargs:
    #     print(f"kwargs:{i} - {kwargs[i]}")
    # for j in args:
    #     print(f"args:{j}")
        
    print(a+b)

# def f(a, *, b=1, **kwargs):
#     print(a+b)

# def f():
#     import math as m
#     a = 1
#     b = "accccccc"
#     c = (3,0)
#     d = [9,9,9,"D",[6]]
#     e = {"A":8}
#     return a * b

code = f.__code__

print(f"flags: {code.co_flags}")
print(f"lnotab: {code.co_lnotab}")


print(f"argcount: {code.co_argcount}")
print(f"positional only: {code.co_posonlyargcount}")
print(f"keyword only: {code.co_kwonlyargcount}")

f(b=2,a=1,)


print(f"co_nlocals: {code.co_nlocals}")

print(f"co_varnames: {code.co_varnames}")
print(f"co_names: {code.co_names}")
print(f"co_cellvars: {code.co_cellvars}")
print(f"co_freevars: {code.co_freevars}")

print(f"code.co_consts{code.co_consts}")
# print(f"code.co_{code.co_}")