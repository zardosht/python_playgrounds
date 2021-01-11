
import socket
import time
from datetime import datetime


ip = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    m = f"This is the message: {datetime.now()}"
    s.sendto(m.encode(), (ip, port))
    print(f"Sent message: {m}")
    time.sleep(3)



# ===============================================
# ================================================

# # Computer A "sender":

# import socket
# UDP_IP = "localhost"
# UDP_PORT = 5005
# MESSAGE = "HELLO!"

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# while True:
#     sock.sendto((bytes(MESSAGE, 'UTF-8')), (UDP_IP, UDP_PORT))


