from datetime import datetime
from socket import *

server_name = "localhost"
server_port = 12000
# Create a client UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

for i in range(10):
    start_time = datetime.now()
    message = f"Ping {i + 1} {start_time}: "
    print(message, end="")

    client_socket.sendto(message.encode(), (server_name, server_port))

    try:
        client_socket.recvfrom(1024)
        print(f"RTT: {(datetime.now() - start_time).total_seconds() * 1000:.3f}ms")
    except timeout:
        print("Request timed out")

client_socket.close()
