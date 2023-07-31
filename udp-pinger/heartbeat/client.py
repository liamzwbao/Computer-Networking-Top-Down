import time
from socket import *

server_name = "localhost"
server_port = 12000
# Create a client UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

seq = 1

while True:
    message = f"Ping {seq} {time.time()}"
    print(message)
    client_socket.sendto(message.encode(), (server_name, server_port))

    time.sleep(10)
    seq += 1
