import logging, aiomysql
# import asyncio

def log(sql, args=()):
    logging.info('SQL:%s' %sql)
    
# 创建连接池
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3308),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset','utf8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
    )
    
# 封装 Select 语句
async def select(sql, args, size = None):
    '''这个 select 函数给我们从 SQL 返回了一个列表'''
    log(sql, args)
    global __pool
    # 用这个连接执行数据库操作
    with (await __pool) as conn:
        # aiomysql.DictCursor 仅仅是要求返回字典格式
        cur = await conn.cursor(aiomysql.DictCursor) 
        # SQL语句的占位符是 ?, 而MySQL的占位符是 %s, select()函数在内部自动替换 - replace('old str','new str')。
        # 注意要始终坚持使用带参数的 SQL, 而不是自己拼接 SQL 字符串, 这样可以防止 SQL 注入攻击。
        await cur.execute(sql.replace('?','%s'), args or ())
        if size:
            # fetchmany 可以获取行数为 size 的多行查询结果集, 返回一个列表
            rs = await cur.fetchmany(size)
        else:
            # fetchall 可以获取一个查询结果的所有()剩余行, 返回一个列表
            rs = await cur.fetchall()   # 获取全部, 例如 select * from user
        # 关闭 cursor , 从这一时刻起该 cursor 将不再可用
        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs
    
# Insert, Update, Delete
# execute() 函数和 select() 函数所不同的是, 
# cursor 对象不返回结果集, 而是通过 rowcount 返回结果数。
'''
要执行INSERT、UPDATE、DELETE(remove)语句, 可以定义一个通用的 execute() 函数,
因为这3种 SQL 的执行都需要相同的参数, 以及返回一个整数表示影响的行数。
'''
async def execute(sql, args):
    '''这个 execute 函数返回一个整数表示影响的行数'''
    log(sql)
    global __pool
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            # rowcount 获取行数, 应该表示的是该函数影响的行数
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        # 返回行数
        return affected
    

def create_args_string(num:int):
    '''
    作用是增加数量为 num 的 '?'  ---封装的 select 语句会用 '%s' 替换掉 '?'
    下面的 Model 元类中被调用,
    '''
    L = []
    for _ in range(num):
        L.append('?')
    return ', '.join(L)
# 注意到Model只是一个基类, 
# 要将具体的子类如 User 的映射信息读取出来需要通过 metaclass: ModelMetaclass。 
# 这样, 任何继承自Model的类（比如User）, 
# 会自动通过 ModelMetaclass 扫描映射关系, 
# 并存储到自身的类属性如__table__、__mappings__中
# 解读 : https://www.cnblogs.com/minseo/p/15538636.html

# Model 只是一个基类, 所以先定义 ModelMetaclass , 再在定义 Model 时使用 metaclass 参数
class ModelMetaclass(type):
    '''
    在ModelMetaclass中, 一共做了几件事情: 
        1.排除掉对 Model 类的修改; 
        2.在当前类(比如 User)中查找定义的类的所有属性, 
        如果找到一个 Field 属性, 就把它保存到一个 __mappings__ 的 dict 中, 
        同时从类属性中删除该 Field 属性, 
        否则, 容易造成运行时错误（实例的属性会遮盖类的同名属性）; 
        3.把表名保存到 __table__ 中, 这里简化为表名默认为类名。
    from metaclass part
    '''
    # __new__ 接收的4个参数分别为: 
    # 当前准备创建的类的对象;   --cls
    # 类的名字;     --name
    # 类继承的父类集合;  --bases
    # 类的方法集合。  --attrs
    def __new__(cls, name, bases, attrs):
        # 排除Model类本身, 返回它自己:
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table 名称:
        tableName = attrs.get('__table__', None) or name    # 若 get 不到就用 name
        # 日志: 找到名为 name 的 model
        logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有的 Field 和 主键名:
        mappings = dict()
        fields = []
        primaryKey = None
        # attrs.items 取决于 __new__ 传入的 attrs 参数
        for k, v in attrs.items():
            # 如果找到一个 Field 类型(字段)
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:   # 若当前字段有 PrimaryKey 为 True, 则它就是主键
                    # 找到主键, 如果主键 primaryKey 有值时, 返回一个错误:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    # 然后直接给主键赋值
                    primaryKey = k
                # 该 field 字段不是主键, 就加入 fidels 列表
                else:
                    fields.append(k)
        # 如果主键为 None 就报错
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)    # 如果 key 存在于字典中则将其移除并返回其值, 否则返回 default 
            
        # lambda: 将变量(无论何种类型)都加上 ``, 最后转换为 str 类型.
        # map: 将 lambda 作用于 fields 这个列表中的每个元素
        # list: 最最后列表化所有成功加工过的元素
        # escaped_fields 列表中每个元素都是str类型的非主键的字段field, 也是数据库表中非主键的列
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName  # table 名
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        # 构造默认的 SELECT, INSERT, UPDATE 和 DELETE 语句:
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        '''
        所有继承自本元类的 Model 都能使用 attrs 中包含的所有方法。
        另外, django中模型类里使用的字段类型如 StringField 等也都是其所在模型类继承来的元类中的方法
        '''
        return type.__new__(cls, name, bases, attrs)


# 定义所有 ORM 映射的基类 Model:
class Model(dict, metaclass = ModelMetaclass):
# class Model(dict, metaclass = Meta):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r" 'Model' object has no attribute '%s' " % key)
        
    def __setattr__(self, key, value ):
        self[key] = value
    # 通过属性返回想要的值
    def getValue(self, key):
        return getattr(self, key, None)
    
    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            # 如果 value 为 None, 定位某个键； value 不为 None 就直接返回
            field = self.__mappings__[key]
            if field.default is not None:
                # 如果 field.default 非空 :  就把它赋值给 value
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s:%s' % (key, str(value)))
                setattr(self, key, value)
        return value
    
    # ------ Model 类添加 class 方法, 就可以让所有子类调用class方法 ------
    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        # findAll() - 根据WHERE条件查找; 
        sql = [cls.__select__]  # 见 ModelMetaClass 中的 attrs['__select__'], 其它的相似
            # where 默认值为 None, 为空值时啥也不干
            # 如果 where 有值就在 sql 加上字符串 'where' 和 变量 where
        if where:
            sql.append('where')
            sql.append(where)
            # 如果没传入 args 参数(默认为空), 就把 args 变成 列表 类型
        if args is None:
            args = []
            
        # get 可以返回 orderBy 的值, 如果失败就返回 None , 这样失败也不会出错
        orderBy = kw.get('orderBy', None)
        # orderBy 非空(或称为'有值'时)给 sql 加上它, 为空值时啥也不干
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        # 和上面的 orderBy 的做法相近
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):  # 若传入的 limit 是整数
                sql.append('?') 
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:  # 如果 limit 是元组且里面只有两个元素
                sql.append('?, ?')
                args.extend(limit)
            else:   # 既不整数, 也不元组, 报错
                raise ValueError('Invalid limit value: %s' % str(limit))
        # 返回选择的列表里的所有值 , 完成 findAll 函数
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]
    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        # findNumber() - 根据WHERE条件查找, 但返回的是整数, 适用于 select count(*) 类型的SQL。
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)   # 等待执行 select 语句
        # 如果 rs 内无元素, 返回 None ；有元素就返回某个数
        if len(rs) == 0:
            return None
        return rs[0]['_num_']
    @classmethod
    async def find(cls, pk):
        # find object by primary key - 根据主键索引查询对象
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])
    
    # ------ 往 Model 类添加实例方法, 就可以让所有子类调用实例方法 ------
    async def save(self):   # 调用方法时, 要注意最后要使用.save()
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)
    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warning('failed to update by primary key: affected rows: %s' % rows)
    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warning('failed to remove by primary key: affected rows: %s' % rows)
    
# Field 和各种 Field 子类:
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)
# 定义 Field 子类及其子类的默认值
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)
        
class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)
