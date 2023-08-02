from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python server.py server_ip"\n[server_ip]: It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
server_socket = socket(AF_INET, SOCK_STREAM)
# Fill in start.

# Fill in end.

while True:
    # Start receiving data from the client
    print("Ready to serve...")
    client_socket, addr = server_socket.accept()
    print(f"Received a connection from: {addr}")
    message =  # Fill in start. # Fill in end.
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    file_exist = False
    try:
        # Check weather the file exist in the cache
        with open(filename, 'r') as f:
            output_data = f.readlines()
            file_exist = True
            # Proxy server finds a cache hit and generates a response message
            client_socket.send("HTTP/1.0 200 OK\r\n")
            client_socket.send("Content-Type:text/html\r\n")
            # Fill in start.

            # Fill in end.
            print("Read from cache")
    except IOError:
        # Error handling for file not found in cache
        if not file_exist:
            # Create a socket on the proxy server
            c =  # Fill in start. # Fill in end.
            host_name = filename.replace("www.", "", 1)
            print(host_name)
            try:
                # Connect to the socket to port 80
                # Fill in start.

                # Fill in end.

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                file_obj = c.makefile('r', 0)
                file_obj.write(f"GET http://{filename} HTTP/1.0\n\n")

                # Read the response into buffer
                # Fill in start.

                # Fill in end.

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmp_file = open(f"./{filename}", 'wb')
                # Fill in start.

                # Fill in end.
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.

            # Fill in end.

    # Close the client socket
    client_socket.close()

# Close the server socket
# Fill in start.

# Fill in end.
