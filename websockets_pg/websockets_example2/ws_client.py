import asyncio
import websockets
import datetime

async def my_connect():
    async with websockets.connect("ws://localhost:3000") as websocket:
        for i in range(100):
            await websocket.send("Client1: current time: {}".format(datetime.datetime.now().time()))
            data_rcv = await websocket.recv()
            print("{}. Data received from server: {}".format(i, data_rcv))


def main():
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(my_connect())
    # event_loop.run_forever()
    # event_loop.close()


if __name__ == "__main__":
    main()

