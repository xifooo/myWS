'比 1 更简洁'

import click


@click.group()  # 建一个 group , 可以往里塞命令行工具
def cli():
    pass

@cli.command()
def initdb():
    '''
    初始化数据库
    :return:
    '''
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    '''
    删除数据库
    :return:
    '''
    click.echo('Dropped the database')

if __name__ == '__main__':
    cli()