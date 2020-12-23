import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
host = socket.gethostname()
s.connect((host, port))
print(f"Client: Socket connected to {host}:{port}")

# msg = s.recv(1024)
# print(msg.decode("utf-8"))

## What if the message was longer than 1024 bytes? 
## We obviously need to work with buffers. 

full_msg = ''
while True: 
    msg = s.recv(8)
    print(f"Message chunk received (8 bytes): {msg}")

    # The recv() method blocks if there is no data but the connection
    # is still open. 
    # When a recv returns 0 bytes, it means the other side has closed 
    # (or is in the process of closing) the connection.
    # https://docs.python.org/3/howto/sockets.html
    if len(msg) <= 0:
        print("Socket closed by server.")
        break

    full_msg += msg.decode("utf-8")

print(f"Full Message: {full_msg}")



## -----------------------------
## This wouldn't work: 
#
# while True:
#     msg = s.recv(8)
#     print(msg.decode("utf-8"))
#
## Output:
## Client: Socket connected to SUSY:12345
## Welcome 
## to the s
## erver! N
## ow: 2020
## -12-23 1
## 4:33:00.
## 105941

# -----------------------------

