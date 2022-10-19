import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')
    
coro = main()
asyncio.run(coro)