import socket
from datetime import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
s.bind((socket.gethostname(), port))
print(f"Server: Socket bound to {socket.gethostname()}:{port}")

s.listen(5)

while True: 
    print("Waiting for incoming connection...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    clientsocket.send(bytes(f"Welcome to the server! Now: {datetime.now()}", "utf-8"))
    print("Message sent.")
    
    # If we don't close the socket here, the client will continue blocking
    # on recv() method. 
    # When a recv returns 0 bytes, it means the other side has closed 
    # (or is in the process of closing) the connection.
    # https://docs.python.org/3/howto/sockets.html
    clientsocket.close()
    print("Connection closed.")
