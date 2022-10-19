#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Configuration
把config_default.py作为开发环境的标准配置, 
把config_override.py作为生产环境的标准配置, 
我们就可以既方便地在本地开发, 又可以随时把应用部署到服务器上。

应用程序读取配置文件需要优先从config_override.py读取。
为了简化读取配置文件, 可以把所有配置读取到统一的config.py中:
'''

__author__ = 'Michael Liao'

import config_default

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    重写属性设置，获取方法
    支持通过属性名访问键值对的值，属性名将被当做键名
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        # zip函数将参数数据分组返回[(arg1[0],arg2[0],arg3[0]...),(arg1[1],arg2[1],arg3[1]...),,,]
        # 以参数中元素数量最少的集合长度为返回列表长度
        for k, v in zip(names, values):
            self[k] = v
    def __getattr__(self, key): # 访问不存在的属性时再来这里找
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

@classmethod
def from_dict(cls, src_dict):
    """
    将一个dict转为Dict
    """
    d = Dict()
    for k, v in src_dict.items():
        # 使用三目运算符，如果值是一个dict递归将其转换为Dict再赋值，否则直接赋值
        d[k] = cls.from_dict(v) if isinstance(v, dict) else v
    return d

'''def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D'''

configs = config_default.configs

try:
    from . import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = from_dict(configs)