from socket import *

import argparse as argparse


def http_get_request(server_host: str, server_port: int, filename: str) -> None:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        # Send the HTTP request message
        url_template = f"GET /{filename} HTTP/1.1\r\n" \
                       f"Host: {gethostbyname(gethostname())}:{str(client_socket.getsockname()[1])}\r\n\r\n"
        client_socket.send(url_template.encode())

        # Handle HTTP response
        # Receive one HTTP response header line
        response = client_socket.recv(1024).decode()
        print(response)

        # Receive the file
        response = client_socket.recv(10000).decode()
        print(response)
    except SO_ERROR:
        print(f"Error while requesting {gethostbyname(gethostname())}:{server_port}/{filename}")

    client_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("server_host", help="server host name", type=str)
    parser.add_argument("server_port", help="server port number", type=int)
    parser.add_argument("filename", help="file name", type=str)
    args = parser.parse_args()

    http_get_request(args.server_host, args.server_port, args.filename)
