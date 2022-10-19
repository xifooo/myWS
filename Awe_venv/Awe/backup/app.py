import logging; logging.basicConfig(level=logging.INFO)
from aiohttp import web


# 定义服务器响应请求的的返回为 "Awesome Website"
async def index(request):
    return web.Response(body=b'<h1>Awe Website</h1>', content_type='text/html')

# 建立服务器应用，持续监听本地9000端口的http请求，对首页"/"进行响应
def init():
    app = web.Application() # 实例化 application
    app.router.add_get('/',index)   # 添加路由, 响应
    web.run_app(app, host='127.0.0.1', port=9000)   # 在 host:port 上运行 app
    
if __name__ == '__main__':
    init()