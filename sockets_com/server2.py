import time
import random
import socket
from datetime import datetime

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
s.bind((socket.gethostname(), port))
print(f"Server: Socket bound to {socket.gethostname()}:{port}")

s.listen(5)

while True: 
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = f"Welcome to the server! Now: {datetime.now()}"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    
    clientsocket.send(bytes(msg, "utf-8"))
    print("First message sent.")
    
    # We don't need it anymore
    # clientsocket.close()

    while True: 
        time.sleep(3)
        randlength = random.randrange(15)
        randstr = "a" * randlength
        msg = f"Time: {time.time()}, random: {randstr}"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))
