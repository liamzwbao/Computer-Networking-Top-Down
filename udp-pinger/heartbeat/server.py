import time
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
server_socket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
server_socket.bind(('', 12000))
server_socket.settimeout(30)

while True:
    try:
        # Receive the client packet along with the address it is coming from
        message, address = server_socket.recvfrom(1024)
    except timeout:
        print("The client application has stopped")
        continue

    received = time.time()

    messages = message.decode().split(" ")
    seq = int(messages[1])
    sent = float(messages[2])
    print(f"Seq {seq}: Time difference = {(received - sent) * 1000:.3f}ms")
