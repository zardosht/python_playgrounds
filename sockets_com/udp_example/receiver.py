import socket
import time
from datetime import datetime

ip = ""
# ip = "localhost"
# ip = "127.0.0.1"
# ip = "susy"
port = 5555
receiver_address = (ip, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(receiver_address)

while True:
    print("Waiting for message ...")
    message, address = s.recvfrom(1024)
    print(f"Received message {message} from address {address}")




# ===============================================
# ================================================

# #  Computer B "receiver":
# import socket
# UDP_IP = "localhost"
# UDP_PORT = 5005

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT)) 

# while True:
#     data = sock.recv(1024)
#     print("received: ", data)


