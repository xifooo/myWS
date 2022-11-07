import click


'''
@click.command()   # 将这个method装饰为命令行工具
@click.option('-name',default='world', help='姓名', type=str)   # 添加可传(选)参数
def say_hello(name):
    click.echo(f'hello {name}')
'''
    
@click.command()
@click.option('-count', default=1, help='number of greetings')   # 可选, 必须使用 --count=5 这种样式
@click.argument('name')   # 必须传值, 但不必再输入一次这个名为 name 的string, (不必传键值的键), 不必使用 name=wang 这种样式
def say_hello(count,name):
    for _ in range(count):
        click.echo(f'hello! {name}')



if __name__ == '__main__':
    say_hello()

    