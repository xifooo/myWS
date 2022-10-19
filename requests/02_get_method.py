import requests as rs


def dec(func):
    
    def inner(*args, **kwargs):
        print(f"模块名字: {func.__name__}")
        print(f"功能: {func.__doc__}")
        func(*args, **kwargs)
        print('-------------------'.ljust(10, '*'))
        
    return inner

# 创建一个 HTTP 的 GET 请求并发送到 url
@dec
def create_get(url:str) -> 0:
    '''创建一个 HTTP 的 GET 请求并发送到 url'''
    resp = rs.request(method="GET", url=url)
    print(resp.text)
    return 0

# 获取 status_code 状态码
@dec
def get_status(url:str) -> 0:
    '''获取 status_code 状态码'''
    resp = rs.get(url)
    print(resp.status_code)
    
    resp1 = rs.get(f'{url}/news')
    print(resp1)
    return 0

# head() 方法检索文档标题。 标头由字段组成，包括<日期>，<服务器>，<内容类型>或<上次修改时间>
@dec
def head_request(url:str)->0:
    '''head() 方法检索文档标题。 标头由字段组成，包括<日期>，<服务器>，<内容类型>或<上次修改时间>'''
    resp = rs.head(url)
    print(resp, type(resp), sep='\n <-类型-> \n',end='\n\n')
    print(f"Server: {resp.headers['server']}")
    print(f"Last modified: {resp.headers['last-modified']}")
    print(f"Content type: {resp.headers['content-type']}")
    return 0

# GET 请求，传参
@dec
def mget(url:str,params:dict)->0:
    '''GET 请求，传参'''
    resp = rs.get(url)
    print('请求url: ', resp.url, type(resp.url), sep='\n------\n')
    print('响应内容: ', resp.text)
    return 0

# 请求重定向
@dec
def request_redirect(url:str)->0:
    '''请求重定向'''
    resp = rs.get(url)
    print('状态码: ', resp.status_code)
    print('重定向响应: ', resp.history)
    print('请求url: ', resp.url)
    return 0

# 禁用重定向
@dec
def request_unredirect(url:str)->0:
    '''禁用重定向'''
    resp = rs.get(url, allow_redirects=False)
    print('状态码: ', resp.status_code)
    print('重定向响应: ', resp.history)
    print('请求url: ', resp.url)
    return 0


if __name__ == '__main__':
    
    url = "http://www.webcode.me"
    create_get(url)
    get_status(url)
    head_request(url)
    
    # httpbin.org 免费提供 HTTP 请求&响应服务
    httpbin = 'https://httpbin.org/get'
    httpbin01 = f'{httpbin}?name=Peter'
    payload = {'name': 'Peter', 'age': 23}
    mget(httpbin, payload)
    
    rd_url = "https://httpbin.org/redirect-to?url=/"
    request_redirect(rd_url)
    request_unredirect(rd_url)
