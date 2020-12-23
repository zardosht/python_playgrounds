import socket

# If the message is larger than the buffer size we should 
# manage the buffer. 
#
# As seen in server1.py and client1.py example, in order to get the full
# message from the message chunks, we have to receive a 0 byte message
# on the client side. The recv() method blocks until there is something 
# to read. In order to send the 0 byte message and unblock the recv() 
# call we have to close the socket on the server-side. 
# This, however, is inconvenient for the cases where I have a large 
# message and want to keep the connection open and send my message as
# chunks of data. 
# 
# There are several ways to do it: 
# * fixed sized messages
# * message delimiters
# * headers indicating how long the message will be
# * shutting down the connection
#
# -----------------------------------------
# From: https://docs.python.org/3/howto/sockets.html
#
# Now we come to the major stumbling block of sockets - send and recv 
# operate on the network buffers. They do not necessarily handle all the 
# bytes you hand them (or expect from them), because their major focus is 
# handling the network buffers. In general, they return when the 
# associated network buffers have been filled (send) or emptied (recv). 
# They then tell you how many bytes they handled. It is your 
# responsibility to call them again until your message has been 
# completely dealt with.
#
# When a recv returns 0 bytes, it means the other side has closed (or is 
# in the process of closing) the connection. You will not receive any 
# more data on this connection. Ever. You may be able to send data 
# successfully; I’ll talk more about this later.
#
# A protocol like HTTP uses a socket for only one transfer. The client 
# sends a request, then reads a reply. That’s it. The socket is 
# discarded. This means that a client can detect the end of the reply by 
# receiving 0 bytes.
#
# But if you plan to reuse your socket for further transfers, you need to 
# realize that there is no EOT on a socket. I repeat: if a socket send or 
# recv returns after handling 0 bytes, the connection has been broken. If 
# the connection has not been broken, you may wait on a recv forever, 
# because the socket will not tell you that there’s nothing more to read 
# (for now). Now if you think about that a bit, you’ll come to realize a 
# fundamental truth of sockets: messages must either be fixed length 
# (yuck), or be delimited (shrug), or indicate how long they are 
# (much better), or end by shutting down the connection. 
# The choice is entirely yours, (but some ways are righter than others).
#
# Assuming you don’t want to end the connection, the simplest solution 
# is a fixed length message.
# -----------------------------------------


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
host = socket.gethostname()
s.connect((host, port))
print(f"Client: Socket connected to {host}:{port}")

while True: 
    full_msg = ""
    new_msg = True
    while True:
        chunk = s.recv(16)
        if new_msg: 
            print(f"New message length: {chunk[:HEADERSIZE]}")
            msglen = int(chunk[:HEADERSIZE])
            new_msg = False

        full_msg += chunk.decode("utf-8")
        if len(full_msg) - HEADERSIZE == msglen:
            print("Full message received.")
            print(f"Full Message: {full_msg[HEADERSIZE:]}")
            new_msg = True
            full_msg = ""
        
    print(full_msg)
