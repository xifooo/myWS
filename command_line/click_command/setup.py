from setuptools import setup

setup(
    name = 'click-example-db',  # 包的名字（起名字）,脚本安装后就叫这个名字
    version = '0.1',   # 指定版本
    py_modules = ['clicktool'],   # 指定模块名称（起名字）,脚本名字
    include_package_data = True, 
    install_requires = [
        'click',
    ],
    # entry_points 设置成 [console_scripts]， 表明要安装成可以在终端调用的命令模块
    # cooldb=demo:cli，cooldb 是命令，执行该命令时，等同于执行 demo.py 的 cli
    entry_points = '''
        [console_scripts]  
        clicktool = click_group2:cli
    ''',
)