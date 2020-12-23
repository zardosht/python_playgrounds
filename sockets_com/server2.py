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

    

    clientsocket.send(bytes(f"Welcome to the server! Now: {datetime.now()}", "utf-8"))
