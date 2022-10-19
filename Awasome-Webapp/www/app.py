# app.py

# -*- coding: utf-8 -*-
# @author xian_wen
# @date 5/26/2021 2:06 PM

# import asyncio
import json, logging, os, time
from aiohttp import web
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import orm
from coroweb import add_routes, add_static, get, post
from models import User,Blog

## handlers 是url处理模块, 当handlers.py在API章节里完全编辑完再将下一行代码的双井号去掉
## from handlers import cookie2user, COOKIE_NAME

logging.basicConfig(level=logging.INFO)

# jinja模板的初始化. 初始化jinja2的函数
def init_jinja2(app, **kwargs):
    logging.info('Init jinja2...')
    options = dict(
        autoescape=kwargs.get('autoescape', True),
        block_start_string=kwargs.get('block_start_string', '{%'),
        block_end_string=kwargs.get('block_end_string', '%}'),
        variable_start_string=kwargs.get('variable_start_string', '{{'),
        variable_end_string=kwargs.get('variable_end_string', '}}'),
        auto_reload=kwargs.get('auto_reload', True)
    )
    path = kwargs.get('path', None)
    if path is None:
        # /www/templates
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('Set jinja2 template path: %s' % path)
    # Load templates from a directory in the file system
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kwargs.get('filters', None)
    if filters is not None:
        # Filters are Python functions
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

# 中间件一
# 把通用的功能从每个URL处理函数中拿出来集中放到一个地方
async def logger_factory(app, handler):
    '''
    URL 处理日志工厂
    '''
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return await handler(request)   # 等待handler处理request
    return logger


# async def auth_factory(app, handler):
#     '''
#     认证处理工厂--把当前用户绑定到request上，并对URL/manage/进行拦截，检查当前用户是否是管理员身份
#     需要handlers.py的支持, 当handlers.py在API章节里完全编辑完再将下面代码的双井号去掉# 
#     '''
#     async def auth(request):
#         logging.info('check user: %s %s' % (request.method, request.path))
#         request.__user__ = None
#         cookie_str = request.cookies.get(COOKIE_NAME)
#         if cookie_str:
#             user = await cookie2user(cookie_str)
#             if user:
#                 logging.info('set current user: %s' % user.email)
#                 request.__user__ = user
#         if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
#             return web.HTTPFound('/signin')
#         return (await handler(request))
#     return auth

async def data_factory(app, handler):
    '''数据处理工厂'''
    async def parse_data(request):
        # JSON 数据格式
        if request.content_type.startswith('application/json'):
            # Read request body decoded as json 读取请求正文解码为json
            request.__data__ = await request.json()
            logging.info('Request json: %s' % str(request.__data__))
        # form 表单数据被编码为 key/value 格式发送到服务器（表单默认的提交数据的格式）
        elif request.content_type.startswith('application/x-www-form-urlencoded'):
            # Read POST parameters from request body
            request.__data__ = await request.post()
            logging.info('Request form: %s' % str(request.__data__))
        return await handler(request)
    return parse_data


# 中间件二
'''
而 response 这个 middleware 把返回值转换为 web.Response 对象再返回,
以保证满足 aiohttp 的要求
'''
async def response_factory(app, handler):
    '''响应返回处理工厂'''
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        # The base class for the HTTP response handling HTTP响应处理的基类
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            # 二进制流数据（如常见的文件下载）
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body = r.encode('utf-8'))
            # HTML 格式
            resp.content_type = 'text/html; charset=UTF-8'
            return resp
        # Response classes are dict like objects 响应类是类似dict的对象
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(
                    # ensure_ascii: if false then return value can contain non-ASCII characters
                    # __dict__: store an object’s (writable) attributes
                    # 序列化 r 为 json 字符串, default 把任意一个对象变成一个可序列为 JSON 的对象
                    body = json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                # JSON 数据格式
                resp.content_type = 'application/json; charset=UTF-8'
                return resp
            else:
                ## 在handlers.py完全完成后,去掉下一行的双井号
                ##r['__user__'] = request.__user__
                # app[__templating__] 是一个 Environment 对象, 加载模板, 渲染模板
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html; charset=UTF-8'
                return resp
        # Status Code 状态码
        if isinstance(r, int) and 100 <= r < 600:
            return web.Response(status = r)
        # Status Code and Reason Phrase 状态码和原因短语
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and 100 <= t < 600:
                # 1xx: Informational - Request received, continuing process
                # 2xx: Success - The action was successfully received, understood, and accepted
                # 3xx: Redirection - Further action must be taken in order to complete the request
                # 4xx: Client Error - The request contains bad syntax or cannot be fulfilled
                # 5xx: Server Error - The server failed to fulfill an apparently valid request
                return web.Response(status=t, reason=str(m))
        # Default
        resp = web.Response(body=str(r).encode('utf-8'))
        # 纯文本格式
        resp.content_type = 'text/plain; charset=UTF-8'
        return resp
    return response

# 时间转换
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:  # 1 min
        return u'1分钟前'
    if delta < 3600:  # 1 h
        # // 表示商取整, 如 3 / 2 = 1.5, 3 // 2 = 1
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:  # 24 h
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:  # 7 days
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


'''async def init(loop):
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='123456', db='awasome')
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv
#  这里又用蔡老师的老代码,  懒得管了能跑就行
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()'''

from config_default import configs

# 单独定义一个协程init_db(), 然后绑定到app.on_startup, 使得 app 启动后, 数据库连接池随之创建。
async def init_db(app):
    # If on Linux, use another user instead of 'root'
    '''
    host=configs.db.host,
    port=configs.db.port,
    user=configs.db.user,
    password=configs.db.password,
    db=configs.db.database,
    '''
    await orm.create_pool(
        host=configs['db']['host'],
        port=configs['db']['port'],
        user=configs['db']['user'],
        password=configs['db']['password'],
        db=configs['db']['db'],
    )

def init():
    
    # 最后, 在app.py中加入middleware、jinja2模板和自注册的支持
    app = web.Application(middlewares=[logger_factory,response_factory])
    init_jinja2(app, filters=dict(datatime=datetime_filter))
    add_routes(app, 'handlers') # 自动把 handler 模块的所有符合条件的函数注册了:
    add_static(app)

    app.on_startup.append(init_db)
    web.run_app(app, host='localhost', port=9000)
    '''
    采用 web.run_app() 代替 loop.create_server() 和 loop.run_until_complete() , 
    随着而来的问题是数据库连接池的创建必须放到协程中运行。
    解决办法：
    单独定义一个协程 init_db(), 然后绑定到 app.on_startup, 使得 app 启动后, 数据库连接池随之创建。
    '''
    
    @get('/')
    def index(request):
        summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        blogs = [
            Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
            Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
            Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
        ]
        return {
            '__template__': 'blogs.html',
            'blogs': blogs
        }
        
if __name__ == "__main__":
    init()
    