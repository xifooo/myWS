#! /usr/bin/env python3

import subprocess, inspect
 
 
# 在每个函数运行时, 先输出函数名，再运行函数
def dec(f):
    
    def wrapper(*args, **kwargs):
        print(f" \n ***- this is a method named after {f.__code__.co_name} -***")
        f()
        # return f.__code__.co_name
    return wrapper



''' 方法一: subprocess.Popen() '''
@dec
def popen(cmd='ipconfig',/):
    cmd = cmd.split()
    # 返回的是 Popen 实例对象
    proc = subprocess.Popen(
        cmd, # cmd特定的查询空间的命令
        stdin=None, # 标准输入 键盘
        stdout=subprocess.PIPE,    # -1 标准输出（演示器、终端) 保存到管道中以便进行操作
        stderr=subprocess.PIPE,    # 标准错误, 保存到管道
        shell=True  
    )

    # print(proc.communicate()) # 标准输出的字符串 + 标准错误的字符串
    outinfo, errinfo = proc.communicate()
    print(outinfo.decode('gbk'))  # 外部程序(windows系统)决定编码格式
    print(errinfo.decode('gbk'))


''' 
方法二: subprocess.call() 
相当于os.system(cmd), 参数shell默认为False
'''
@dec
def call(cmd='ipconfig',/):
    cmd = cmd.split()
    subprocess.call(cmd)

    # # linux获取磁盘空间
    # subprocess.call(['df', '-h'])  # 数组作为参数运行命令


''' 
方法三: subprocess.run() 
命令执行完成后返回一个包含执行结果的CompletedProcess类的实例. 默认不会返回输出, 只返回命令和执行状态.
'''
@dec
def run(cmd='ipconfig',/):
    cmd = cmd.split()
    # subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, timeout=None, check=False, universal_newlines=False)
    completed = subprocess.run(cmd)
    print(f'returncode: {completed.returncode}')


'''
方法四:subprocess.getstatusoutput()
执行cmd命令, 返回一个元组 (命令执行状态, 命令执行结果输出). 
返回状态码和结果, 0表示成功
'''
@dec
def getstatusoutput(cmd='ipconfig',/):
    cmd = cmd.split()
    ret, val = subprocess.getstatusoutput(cmd)
    print(ret)
    print(val)


if __name__ == "__main__":
    cmd = 'ping www.baidu.com'
    popen(cmd)
    call(cmd)
    run(cmd)
    getstatusoutput(cmd)