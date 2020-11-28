import asyncio
import aioredis
import websockets


import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "127.0.0.1", 6379)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        'redis', 6379)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

async def redis_connect():
	redis = await aioredis.create_redis(
		'redis://localhost')
	await redis.set('my-key', 'value')
	val = await redis.get('my-key')
	print(val)
	
	# Gracefully close
	redis.close
	await redis.wait_closed()
	