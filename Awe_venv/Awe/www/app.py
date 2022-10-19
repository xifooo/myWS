import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time

from datetime import datetime
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from config import configs

import orm
from coroweb import add_routes, add_static

# handlers 是 url 处理模块
from handlers import cookie2user, COOKIE_NAME

# 初始化jinja2的函数
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        # /www/templates
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        
    logging.info('set jinja2 template path: %s' % path)
    # Load templates from a directory in the file system
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        # Filters are Python functions
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env


# 以下是 middleware,可以把通用的功能从每个URL处理函数中拿出来集中放到一个地方
# 中间件一
async def logger_factory(app, handler):
    '''URL 处理日志工厂'''
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (await handler(request)) # 等待handler处理request
    return logger
# 
async def auth_factory(app, handler):
    '''认证处理工厂--把当前用户绑定到 request 上，并对 URL/manage/ 进行拦截，检查当前用户是否是管理员身份'''
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        return (await handler(request))
    return auth

# 
async def data_factory(app, handler):
    '''
    数据处理工厂
    '''
    async def parse_data(request):
        # JSON 数据格式
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                # Read request body decoded as json 读取请求正文解码为json
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            # form 表单数据被编码为 key/value 格式发送到服务器（表单默认的提交数据的格式）
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                # Read POST parameters from request body
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data

# 中间件二
async def response_factory(app, handler):
    '''
    响应返回处理工厂:
    而 response 这个 middleware 把返回值转换为 web.Response 对象再返回,
    以保证满足 aiohttp 的要求
    '''
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        # The base class for the HTTP response handling - HTTP响应处理的基类
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
            resp = web.Response(body=r.encode('utf-8'))
            # HTML 格式
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        # Response classes are dict like objects 响应类是类似dict的对象
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                # ensure_ascii: if false then return value can contain non-ASCII characters
                    # __dict__: store an object’s (writable) attributes
                    # 序列化 r 为 json 字符串, default 把任意一个对象变成一个可序列为 JSON 的对象
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                # JSON 数据格式
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                r['__user__'] = request.__user__
                # app[__templating__] 是一个 Environment 对象, 加载模板, 渲染模板
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        # Status Code - 状态码
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        # Status Code and Reason Phrase - 状态码和原因短语
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                # 1xx: Informational - Request received, continuing process
                # 2xx: Success - The action was successfully received, understood, and accepted
                # 3xx: Redirection - Further action must be taken in order to complete the request
                # 4xx: Client Error - The request contains bad syntax or cannot be fulfilled
                # 5xx: Server Error - The server failed to fulfill an apparently valid request
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
         # 纯文本格式
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

# 时间转换
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:  # 1 min
        return u'1分钟前'
    if delta < 3600:    # 1 h
        # // 表示商取整, 如 3 / 2 = 1.5, 3 // 2 = 1
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:   # 24 h
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:  # 7 days
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

async def init(loop):
    await orm.create_pool(loop=loop, **configs.db)
    # 在handlers.py完全完成后,在下面 middlewares 的list中加入 auth_factory
    app = web.Application(
                    middlewares=[
                        logger_factory, response_factory
                ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    runner = web.AppRunner(app)
    await runner.setup()
    srv = web.TCPSite(runner, 'localhost', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    await srv.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
    
'''
asyncio的使用可分三步走:

1-创建事件循环
2-指定循环模式并运行
3-关闭循环
'''