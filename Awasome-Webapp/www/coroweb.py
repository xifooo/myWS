#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__auther__ = 'Ayayaneru'
# 有两个地方的'name' ==> '_' 改动
# 围绕 web.Response 做了一些改动
# Web框架的设计是完全从使用者出发，目的是让使用者编写尽可能少的代码。
import asyncio, os, inspect, logging, functools

# apis是处理分页的模块,代码在本章页面末尾,请将apis.py放在www下以防报错
# APIError 是指API调用时发生逻辑错误
from urllib import parse
from aiohttp import web
from apis import APIError

def get(path):
    # 函数通过@get()的装饰就附带了URL信息。
    '''
    Define decorator @get('/path')
    把一个函数映射为一个URL处理函数
    '''
    def decorator(func):
        @functools.wraps(func) # 使得 wrapper.__name__ = func.__name__
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    Define decorator @post('/path')
    把一个函数映射为一个URL处理函数
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


# 下面这部分可以自行查阅 inspect 模块来理解
# https://docs.python.org/zh-cn/3.8/index.html
# 以下是RequestHandler需要定义的一些函数
def get_required_kw_args(fn):
    """
    获取函数命名关键字参数，且非默认参数
    
    :param fn: function
    :return:
    """
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            # 在 args 里加上仅包含关键字（keyword）的参数, 且不包括默认值, 然后返回 args
            args.append(name)
    return tuple(args)
    # 所以这个函数的作用和名称一样,  得到需要的关键字参数, 下面同理

def get_named_kw_args(fn):
    """
    获取函数命名关键字参数

    :param fn: function
    :return:
    """
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

def has_named_kw_args(fn):
    """
    判断是否有命名关键字参数

    :param fn: function
    :return:
    """
    params = inspect.signature(fn).parameters
    for _, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):
    """
    判断是否有关键字参数

    :param fn: function
    :return:
    """
    params = inspect.signature(fn).parameters
    for _, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    """
    判断是否有请求参数

    :param fn: function
    :return:
    """
    # 获取函数 fn 的签名
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (
            param.kind != inspect.Parameter.VAR_POSITIONAL and 
            param.kind != inspect.Parameter.KEYWORD_ONLY and 
            param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError(
                'request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found


'''
<先从URL函数中分析需要接收的参数, 然后从request对象中获取必要的参数, 
紧接着调用URL函数进行处理, 最后把结果转换为 web.Response 对象.>
这样, 就完全符合aiohttp框架的要求

URL处理函数不一定是一个coroutine, 因此我们用 RequestHandler() 来封装一个URL处理函数。
RequestHandler是一个类, 由于定义了__call__()方法，因此可以将其实例视为函数。
'''
class RequestHandler(object):
    # 这个类慢慢看吧,  不懂也没关系
    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
    
    # Make RequestHandler callable
    '''
    此方法会在实例作为一个函数被“调用”时被调用；
    如果定义了此方法，则 x(arg1, arg2, ...) 就大致可以被改写为 type(x).__call__(x, arg1, ...)。
    也就是说class可以变为func
    '''
    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest(reason='Missing Content-Type.')
                ct = request.content_type.lower()
                # JSON 数据格式
                if ct.startswith('application/json'):
                    # Read request body decoded as json
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest(reason='JSON body must be object.')
                    kw = params
                # form 表单数据被编码为 key/value 格式发送到服务器（表单默认的提交数据的格式）
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    # Read POST parameters from request body
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest(reason='Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]

        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                # Remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # Check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v

        if self._has_request_arg:
            kw['request'] = request

        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest(reason='Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)


# /www/static
def add_static(app):
    '''
    定义add_static函数，来注册static文件夹下的文件
    '''
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    # Add a router and a handler for returning static files 添加用于返回静态文件的路由器和处理程序
    # Development only, in production, use web servers like nginx or apache 仅限开发，在生产中使用nginx或apache等web服务器
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))


def add_route(app, fn):
    '''
    编写一个 add_route 函数, 用来注册一个URL处理函数
    <是路由, urls.py>
    Read:
    检查 fn 函数的__method__与__route__是否存在, 任一不存在就报错ValueError
    若fn既不是coroutine, 也不是generator, 就把fn变成coroutine
    --(官网Router.add_route()中提到 Pay attention please: handler is converted to coroutine internally when it is a regular function, 貌似会自动进行转化。)
    '''
    # getattr(x, 'foobar') 等同于 x.foobar。
    # 如果指定的属性不存在，且提供了 default 值，则返回它，否则触发 AttributeError。
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if (path is None) or (method is None):
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if (not asyncio.iscoroutinefunction(fn)) and (not inspect.isgeneratorfunction(fn)):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))


def add_routes(app, module_name):
    '''
    最后一步, 把很多次add_route()注册的调用变成自动扫描

    自动把 handler 模块的所有符合条件的 URL 函数注册了:
    add_routes(app, 'handlers')

    add_routes()定义如下: 
    '''
    n = module_name.rfind('.')
    if n == (-1): # rfind不存在则返回-1
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)