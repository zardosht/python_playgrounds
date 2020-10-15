from cv2 import cv2
import websockets
import asyncio


async def show_image(image):
    cv2.imshow("Image", image)
    if cv2.waitKey() & 0xff == ord('q'):
        return 



async def consumer_handler(websocket, path):
    print("Waiting for images...")
    async for message in websocket:
        # await show_image(message)
        print(message)


def main():
    start_server = websockets.serve(consumer_handler, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()


# Use the WebSockets simple interactive client to test your server: 
# $ python -m websockets ws://localhost:5000