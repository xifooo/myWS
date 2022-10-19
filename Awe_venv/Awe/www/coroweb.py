import asyncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
# 由于 aiohttp 作为一个Web框架比较底层, 还需要基于 aiohttp 编写一个更方便处理 URL 的 Web 框架

from apis import APIError
# apis是处理分页的模块，APIError 是指API调用时发生逻辑错误

# 编写装饰函数 @get()
def get(path):
    # Define decorator @get('/path')
    # 函数通过@get()的装饰就附带了URL信息。
    '''
    Define decorator @get('/path')
    把一个函数映射为一个URL处理函数
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

# 编写装饰函数 @post()
def post(path):
    # Define decorator @post('/path')
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

# 以下是 RequestHandler 需要定义的一些函数
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
    return tuple(args)  # 所以这个函数的作用和名称一样,  得到需要的关键字参数, 下面同理
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
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True
def has_var_kw_arg(fn):
    """
    判断是否有关键字参数

    :param fn: function
    :return:
    """
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True
def has_request_arg(fn):
    """
    判断是否有请求参数

    :param fn: function
    :return:
    """
    sig = inspect.signature(fn) # 获取函数 fn 的签名
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found

'''
<先从URL函数中分析需要接收的参数, 然后从request对象中获取必要的参数, 
紧接着调用URL函数进行处理, 最后把结果转换为 web.Response 对象.>
这样, 就完全符合aiohttp框架的要求

URL处理函数不一定是一个coroutine, 因此我们用 RequestHandler() 来封装一个URL处理函数。
RequestHandler是一个类, 由于定义了__call__()方法，因此可以将其实例视为函数。
'''
# 定义 RequestHandler 从 URL 函数(视图方法)中分析其需要接受的参数
class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        
    '''
    此方法会在实例作为一个函数被 '调用' 时被调用；
    如果定义了此方法，则 x(arg1, arg2, ...) 就大致可以被改写为 type(x).__call__(x, arg1, ...)。
    也就是说class可以变为func
    '''
    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest(text='Missing Content-Type.')
                ct = request.content_type.lower()
                # 处理 json 格式
                if ct.startswith('application/json'):
                    params = await request.json()   # 其实就是 json.load, 可理解成将request中的body作为json读取
                    if not isinstance(params, dict):    # 必须是字典类型嗷, 不是的话就给前端捎句话
                        return web.HTTPBadRequest(text='JSON body must be object.')
                    kw = params
                # form 表单数据被编码为 key/value 格式发送到服务器（表单默认的提交数据的格式）
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params) # **表示传入多个参数的集合, 避免位置参数报错
                else:   # POST 过来的啥也不是
                    return web.HTTPBadRequest(text='Unsupported Content-Type: %s' % request.content_type)
            
            if request.method == 'GET':
                # 获取地址栏参数(以GET方式提交的数据)
                qs = request.query_string
                if qs:
                    kw = dict()
                    # parse.parse_qs: 解析以字符串参数形式（类型为 application/x-www-form-urlencoded 的数据）给出的查询字符串。 
                    # 返回字典形式的数据。结果字典的键为唯一的查询变量名而值为每个变量名对应的值列表。'key':[value1,value2...]
                    # True: 可选参数 keep_blank_values 是一个旗标，指明是否要将以百分号转码的空值作为空字符串处理。 
                    # 真值表示空值应当被保留作为空字符串。 默认的假值表示空值会被忽略并将其视作未包括的值。
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        # kw 还是空, request 既不是post, 也不是get(或无参数的), 就把 request.match_info 内容全部以字典类型塞进kw里
        if kw is None:  
            kw = dict(**request.match_info)
        else:   # kw 非空, 继续用 kw 传递参数并开始处理
            if not self._has_var_kw_arg and self._named_kw_args: # 若有 可变关键字参数**kwarg 或 命名关键字参数*args中有参数
                # remove all unamed kw: 清除没有命名的关键字参数
                copy = dict()
                for name in self._named_kw_args:  ## get_named_kw_args 获取命名关键字参数(元组类型)
                    if name in kw:
                        copy[name] = kw[name]   ## 仅仅保留 kw 中与命名关键字参数元组相交的数据
                kw = copy
            # check named arg: 检查命名关键字参数
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v

        if self._has_request_arg:  # 若有请求参数, 就把请求参数塞进 kw 里继续传递
            kw['request'] = request
        # check required kw: 检查所需参数
        if self._required_kw_args: ## get_required_kw_args 获取所需(函数命名关键字)参数，且非默认参数
            for name in self._required_kw_args:
                if not name in kw:  # 若没有所需参数就给前端捎句话
                    return web.HTTPBadRequest(text='Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        
        try:
            # 把经过挑选(GET、POST、必需的、额外的、洗去未命名关键字参数的)参数传给
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)


# 定义 add_static 函数，来注册 static 文件夹下的文件
def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))


# 定义 add_route 函数，来注册一个 URL 处理函数，等同于路由
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
    method = getattr(fn, '__method__', default=None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))


# 定义 add_routes 函数，自动把 handler 模块的所有符合条件的 URL 函数注册了
def add_routes(app, module_name):
    '''
    最后一步, 把很多次add_route()注册的调用变成自动扫描

    自动把 handler 模块的所有符合条件的 URL 函数注册了:
    add_routes(app, 'handlers')

    add_routes()定义如下: 
    '''
    n = module_name.rfind('.')
    if n == (-1):   # rfind不存在则返回-1
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