import time
import random
import pickle
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

    d = {1: "Hey", 2:"There"}
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
    
    clientsocket.send(msg)
    print("Message sent.")
    
    # We don't need it anymore
    # clientsocket.close()

