import aiohttp, asyncio, async_timeout


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            print (await f"{response.text()} {response.status}")

async def post(session, url):
    async with session.post(url["hb.post"], data=b'data') as resp:
        print(await f"{resp.text()} {resp.status}")

async def main():
    url = {
        "hb.get": "http://httpbin.org/get",
        "hb.put": "http://httpbin.org/put",
        "hb.post": "http://httpbin.org/post",
        "hb.del": "http://httpbin.org/delelte",
        "hb.head": "http://httpbin.org/head",
        "hb.patch": "http://httpbin.org/patch",
        "hb.options": "http://httpbin.org/options",
        "pyorg": "http://python.org"
    }
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url["pyorg"])
        
        # session.post(url["hb.post"], data=b'data')
        # session.put('http://httpbin.org/put', data=b'data')
        # session.delete('http://httpbin.org/delete')
        # session.head('http://httpbin.org/get')
        # session.options('http://httpbin.org/get')
        # session.patch('http://httpbin.org/patch', data=b'data')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())