# !/user/bin/env python3
#-*- coding: utf-8 -*-

__author__ = 'Michael liao'

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

# 首页
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')
    # return web.Response(body=b'<h1>Awesome</h1>') ,content_type='text/html'  不添加会变成下载文件非直接浏览

# coroutine类型的初始化函数
async def init(loop):
    '''
    # liao 的方法
    app = web.Application(loop=loop)    # 创建一个Application实例
    app.router.add_route('GET', '/', index)
    # srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000) 旧的协程语法, 下面是新的语法
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    return srv
    '''
    # 新的方法
    host = '127.0.0.1'
    port = 9000
    app = web.Application(loop=loop)
    app.router.add_route("GET", "/", index)
    apprunner = web.AppRunner(app) # 构造AppRunner对象
    await apprunner.setup()        # 调用setup()方法，注意因为源码中这个方法被async修饰，所以前面要加上await，否则报错
    srv = await loop.create_server(apprunner.server, host, port) # 将apprunner的server属性传递进去
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()