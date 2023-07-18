from socket import *

# Prepare a sever socket
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print("The web server starts")

while True:
    # Establish the connection
    connection_socket, addr = server_socket.accept()
    print('Ready to serve...')

    try:
        message = connection_socket.recv(1024).decode()
        filename = message.split()[1][1:]
        with open(filename) as f:
            output_data = f.read()
        # Send one HTTP header line into socket
        connection_socket.sendall("HTTP/1.1 200 ok\r\n".encode())
        connection_socket.send("\r\n".encode())
        # Send the content of the requested file to the client
        for i in range(0, len(output_data)):
            connection_socket.send(output_data[i].encode())
        connection_socket.send("\r\n".encode())
    except IOError:
        # Send response message for file not found
        print("File not found")
        connection_socket.sendall("HTTP/1.1 404 not found\r\n".encode())
        connection_socket.send("\r\n".encode())

    # Close client socket
    connection_socket.close()
