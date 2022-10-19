from objprint import op


op.config(arg_name=True)

def f():
    return None
# class f:
#     ...

# op(print(bool(f) == True),
#     print(bool(f) == False),
#     print(bool(f) is True),
#     print(bool(f) is False),
#     print(bool(f()) == True),
#     print(bool(f()) == False),
#     print(bool(f()) is True),
#     print(bool(f()) is False))

op(f == True,
    f == False,
    bool(f) is True,
    bool(f) is False,
    f() == True,
    f() == False,
    bool(f()) is True,
    bool(f()) is False)

# def fn():
#     a = "good"
#     print(a)
    
# # op(print(bool(fn) == True),
# #     print(bool(fn) == False),
# #     print(bool(fn) is True),
# #     print(bool(fn) is False),
# #     print(bool(fn()) == True),
# #     print(bool(fn()) == False),
# #     print(bool(fn()) is True),
# #     print(bool(fn()) is False))

# op(bool(fn) == True,
#     bool(fn) == False,
#     bool(fn) is True,
#     bool(fn) is False,
#     bool(fn()) == True,
#     bool(fn()) == False,
#     bool(fn()) is True,
#     bool(fn()) is False)


