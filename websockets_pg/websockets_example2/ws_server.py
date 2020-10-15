import asyncio
import websockets

# callback for websockets.serve()
async def my_accept(websocket, path):
    i = 0
    while True:
        try:
            data_rcv = await websocket.recv()
            print(f"{i}. Received data: {data_rcv}")
        except websockets.exceptions.ConnectionClosed: 
            print("Connection closed on recv()")
            break
                
        try: 
            await websocket.send("Sending ACK len(data_rcv): {}".format(len(data_rcv)))
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed on send()")
            break
        
        i += 1


def main():
    websockets_server = websockets.serve(my_accept, "localhost", 3000)
    print("WebSockets server: waiting for client access.")
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(websockets_server)
    event_loop.run_forever()
    # event_loop.close()


if __name__ == "__main__":
    main()

