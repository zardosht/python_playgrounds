import asyncio
import websockets

# From here: 
# https://www.youtube.com/watch?v=7i0-lYjtvIE

async def message():
    async with websockets.connect("ws://localhost:1234") as socket:
        msg = input("What do you want to send: ")
        await socket.send(msg)
        print(await socket.recv())


asyncio.get_event_loop().run_until_complete(message())


