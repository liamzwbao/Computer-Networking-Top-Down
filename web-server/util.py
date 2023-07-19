from socket import socket


def handle_request(connection_socket: socket) -> None:
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
