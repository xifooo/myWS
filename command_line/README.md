# python调用系统命令、命令行/命令行工具
   
## 1. 标准库os、subprocess
### 1.1 **os.system("command")**   
   
该函数返回命令执行结果的返回值，system()函数在执行过程中进行了以下三步操作：  
+ fork一个子进程；  
+ 在子进程中调用exec函数去执行命令；  
+ 在父进程中调用wait（阻塞）去等待子进程结束。  
   
返回0表示命令执行成功，其他表示失败。
   
注意：使用该函数经常会莫名其妙地出现错误，但是直接执行命令并没有问题，所以一般建议不要使用。   
注意：command不能是list, 只能是str、bytes or os.PathLike object.   
   

### 1.2 **os.popen("command")**   

这种调用方式是通过管道的方式来实现，函数返回是 file read 的对象，对其进行读取 read、readlines 等操作可以看到执行的输出。

注意：如果命令执行失败，就读取不到内容。

### 1.3 **subprocess.Popen('command'/['command','args',...])**   
subprocess模块被推荐用来替换一些老的模块和函数，如：os.system、os.spawn、os.popen等   
   
subprocess模块目的是fork一个新的进程并与之通信，最常用是定义类Popen，使用Popen可以创建进程，并与进程进行复杂的交互。其函数原型为：   

subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)   
+ args：这个参数必须是字符串或者是一个由字符串成员的列表。其中如果是一个字符串列表的话，那第一个成员为要运行的程序的路径以及程序名称；从第二个成员开始到最后一个成员为运行这个程序需要输入的参数。   
+ executable：指定要运行的程序，这个一般很少用到，因为要指定运行的程序在args中已经指定了。   
+ stdin，stdout ，stderr：分别代表程序的标准输入、标准输出、标准错误处理。可以选择的值有PIPE，已经存在的打开的文件对象和NONE。若stdout是文件对象的话，要确保文件对象是处于打开状态。
+ shell：默认是False。shell参数根据要执行的命令情况来定，如果将参数shell设为True，executable将指定程序使用的shell。在windows平台下，默认的shell由COMSPEC环境变量来指定。
+ bufsize：指定缓冲。0 无缓冲,1 行缓冲,其他 缓冲区大小,负值 系统缓冲
+ cwd：用于设置子进程的当前目录
+ stdin, stdout, stderr：分别表示程序的标准输入、标准输出、标准错误输出，可以是 subprocess.PIPE 或 其他程序、文件。
+ env：用于指定子进程的环境变量。如果env = None，子进程的环境变量将从父进程中继承。
+ universal_newlines：不同系统的换行符不同，True 即使用 '\n'
+ preexec_fn：只在Unix平台下有效，用于指定一个可执行对象（callable object），它将在子进程运行之前被调用。   

### 1.4 **subprocess.call(), subprocess.check_call(), subprocess.run()等等**    
**subprocess** 是用来替代 **os.system** 等函数的，当**subprocess.call()**、**subprocess.check_call()**、**subprocess.check_output()** 和**subprocess.run()** 这些高级函数无法满足需求时，我们可以使用subprocess.Popen类来实现我们需要的复杂功能。

## 2. **三方库click**   
详见click_command