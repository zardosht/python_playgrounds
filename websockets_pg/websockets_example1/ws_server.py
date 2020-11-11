import asyncio
import websockets

# From here: 
# https://www.youtube.com/watch?v=7i0-lYjtvIE


async def response(websocket, path):
    message = await websocket.recv()
    print(f"We got the messge from the client: {message}")
    await websocket.send("I can confirm I got your message!")


start_server = websockets.serve(response, "localhost", 1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


