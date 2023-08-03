# Link for testing: http://localhost:8888/http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html
from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python server.py server_ip"\n[server_ip]: It is the IP Address Of Proxy Server')
    sys.exit(2)


# Wrapper function for socket.send()
def send(skt: socket, msg: str) -> None:
    skt.send(msg.encode())


# Wrapper function for socket.sendall()
def sendall(skt: socket, msg: str) -> None:
    skt.sendall(msg.encode())


# Wrapper function for socket.recv()
def recv(skt: socket, buffer: int = 2048) -> str:
    return skt.recv(buffer).decode()


# Create a server socket, bind it to a port and start listening
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((sys.argv[1], 8888))
server_socket.listen(1)

while True:
    # Start receiving data from the client
    print("Ready to serve...")
    client_socket, addr = server_socket.accept()
    print(f"Received a connection from: {addr}")
    message = recv(client_socket)
    print(message)

    # Extract the filename from the given message
    filepath = message.split()[1].partition('//')[2]
    print(f"File path: {filepath}")
    filename = filepath.replace('/', '-')
    print(f"File name: {filename}")
    file_exist = False
    try:
        # Check weather the file exist in the cache
        with open(filename, 'r') as f:
            output_data = f.readlines()
            file_exist = True
            # Proxy server finds a cache hit and generates a response message
            header = (f"HTTP/1.1 200 OK\r\n"
                      f"Connection:close\r\n"
                      f"Content-type:text/html\r\n"
                      f"Content-length:{len(output_data)}\r\n"
                      f"\r\n")
            send(client_socket, header)
            for line in output_data:
                send(client_socket, f"{line}\r\n")
            print("Read from cache")
    except IOError:
        # Error handling for file not found in cache
        if not file_exist:
            # Create a socket on the proxy server
            c = socket(AF_INET, SOCK_STREAM)
            host_name = filepath.partition("/")[0]
            file_to_get = filepath.partition("/")[2]
            port = 80
            print(f"Host name: {host_name}")
            print(f"File to GET: {file_to_get}")
            try:
                # Connect to the socket to port 80
                c.connect((host_name, port))

                # Ask port 80 for the file requested by the client
                sendall(c, f"GET /{file_to_get} HTTP/1.1\r\n"
                           f"Host: {host_name}\r\n"
                           f"\r\n")

                # Read the response into buffer
                data = recv(c)

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                with open(f"./{filename}", 'w') as tmp_file:
                    tmp_file.write(data.split("\r\n\r\n")[1])
                send(client_socket, data)
            except:
                print("Illegal request")
            finally:
                c.close()
        else:
            # HTTP response message for file not found
            send(client_socket, "HTTP/1.1 404 Not Found\r\n")
    finally:
        # Close the client socket
        client_socket.close()
