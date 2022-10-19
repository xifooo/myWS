import inspect
from objprint import op

def f():
    frame = inspect.currentframe()
    op(
        frame,
        honor_existing=False,
        depth=1
    )
    print(f"是函数 \'{frame.f_back.f_code.co_name}\' 在调用函数 f")  # 是谁在调用我
    print(f"函数 \'{frame.f_back.f_code.co_name}\' 的局部变量有 \'{frame.f_back.f_locals}\'")    # 调用我的函数，它的局部变量都有什么
    print(f"函数 \'{frame.f_back.f_code.co_name}\' 所在的文件是 \'{frame.f_back.f_code.co_filename}\'")    # 调用我的函数，它所在的文件名
    print(f"函数 \'{frame.f_back.f_code.co_name}\' 在第 \'{frame.f_back.f_lineno}\' 行调用的函数 f")    # 调用我的函数，它在第几行调用的我
    
def g():
    a = 1
    b = 2
    c = []
    f()

g()