import click


@click.group()  # 建一个 group , 可以往里塞命令行工具
def cli():
    pass

@click.command()
def initdb():
    '''
    初始化数据库
    :return:
    '''
    click.echo('Initialized the database')

@click.command()
def dropdb():
    '''
    删除数据库
    :return:
    '''
    click.echo('Dropped the database')

cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == '__main__':
    cli()