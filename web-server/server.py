from socket import *

from util import handle_request

# Prepare a sever socket
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print(f"The web server starts at port: {server_port}")

while True:
    # Establish the connection
    connection_socket, addr = server_socket.accept()
    print('Ready to serve...')

    handle_request(connection_socket)

    # Close client socket
    connection_socket.close()
