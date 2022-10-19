#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

from www.models import(
    User,
)
from www.coroweb import get
# from app import (
#     logger_factory,
#     response_factory,
# )
'''
有了这些基础设施, 
我们就可以专注地往handlers模块不断添加URL处理函数了, 
可以极大地提高开发效率.
这里是view层吗? 
'''

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }