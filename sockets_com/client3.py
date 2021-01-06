import socket
import pickle


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
host = socket.gethostname()
s.connect((host, port))
print(f"Client: Socket connected to {host}:{port}")

while True: 
    full_msg = b''
    new_msg = True
    while True:
        chunk = s.recv(16)
        if new_msg: 
            print(f"New message length: {chunk[:HEADERSIZE]}")
            msglen = int(chunk[:HEADERSIZE])
            new_msg = False

        full_msg += chunk
        if len(full_msg) - HEADERSIZE == msglen:
            print("Full message received.")
            print(f"Full Message: {full_msg[HEADERSIZE:]}")
            
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)
            new_msg = True
            full_msg = b''
        
    print(full_msg)
