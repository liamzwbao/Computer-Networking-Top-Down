from socket import *
from threading import Thread

from util import handle_request

# Prepare a sever socket
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.listen(5)
print(f"The web server starts at port: {server_port}")

threads = []
while True:
    # Establish the connection
    connection_socket, addr = server_socket.accept()

    # Create a thread to serve the received request
    thread = Thread(target=handle_request, args=(connection_socket,))
    threads.append(thread)
    thread.start()
