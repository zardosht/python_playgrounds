import time
import random
import pickle
import socket
import select
from datetime import datetime

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
print(f"Server: Socket bound to {IP}:{PORT}")

print("Waiting for connections ... ")
server_socket.listen()

sockets_list = [server_socket]
clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return None

        message_length = int(message_header.decode("utf-8").strip())
        msg = client_socket.recv(message_length)
        return {"header": message_header, "data": msg}

    except Exception as exp:
        print(exp)
        return None


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket: 
            # someone just connected
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is None:
                # someone disconnected
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            username = user["data"].decode("utf-8")
            print(f"Accepted new connection from {client_address}, username: {username}")

        else: 
            message = receive_message(notified_socket)
            if message is None:
                username = (clients[notified_socket]["data"]).decode("utf-8")
                print(f"Closed connection from {username}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            msg = message["data"].decode("utf-8")
            username = (user["data"]).decode("utf-8")
            print(f"Received message from {username}: {msg}")

            for client_socket in clients: 
                if client_socket != notified_socket: 
                    client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
