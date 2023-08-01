import base64
import ssl
import sys
from datetime import datetime
from socket import *

# Choose a mail server (e.g. Google Mail server) and call it mailserver
mailserver = "smtp.gmail.com"
mailserver_port = 587


# Util function
def send_command(command: str) -> str:
    print(f"C: {command}")
    client_socket.send(f"{command}\r\n".encode())
    recv = client_socket.recv(1024).decode()
    print(f"S: {recv}")
    return recv


# Create socket called client_socket and establish a TCP connection with mailserver
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((mailserver, mailserver_port))
recv = client_socket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print("220 reply not received from server.")

# Send HELO command and print server response.
send_command("HELO Alice")

# Parse mail info from user input
username = input("Enter your gmail.com username: ")
password = input("Enter your gmail.com password: ")
rcpt = input("Enter the recipient's email address: ")
name = input("Enter your name: ")
subject = input("Enter the subject for your mail: ")

# Allow the user to type multi-line messages
print("Enter the message you want to send. Press Ctrl-D to stop.")
message = []
while True:
    try:
        line = input("")
    except EOFError:
        break
    message.append(f"{line}\r\n")
end_msg = "\r\n."

# Start TLS
recv = send_command("STARTTLS")
if recv[:3] != '220':
    print("220 reply not received from server.")
    sys.exit(0)
context = ssl.create_default_context()
client_socket = context.wrap_socket(client_socket, server_hostname=mailserver)
print("TLS AUTH success")

# Authentication
base64_str = f"\0{username}\0{password}".encode()
base64_str = base64.b64encode(base64_str)
auth_msg = f"AUTH PLAIN {base64_str.decode()}"
recv = send_command(auth_msg)
if recv[:3] == '503':
    print("Already authenticated.")
if recv[:3] != '235':
    print("235 reply not received from server.")
    sys.exit(0)
print("ACCOUNT AUTH success")

# Send MAIL FROM command and print server response.
recv = send_command(f"MAIL FROM: <{username}>")
if recv[:3] != '250':
    print("250 reply not received from server.")
    sys.exit(0)

# Send RCPT TO command and print server response.
recv = send_command(f"RCPT TO: <{rcpt}>")
if recv[:3] != '250':
    print("250 reply not received from server.")
    sys.exit(0)

# Send DATA command and print server response.
recv = send_command("DATA")
if recv[:3] != '354':
    print("354 reply not received from server.")
    sys.exit(0)

# Send message header
message_header = (f"From: {name} <{username}>\r\n"
                  f"To: {rcpt}\r\n"
                  f"Date: {datetime.now()}\r\n"
                  f"Subject: {subject}\r\n")

# Send message data.
message_data = message_header
for msg in message:
    message_data += f"{msg}\r\n"

# Message ends with a single period.
send_command(message_data + end_msg)

# Send QUIT command and get server response.
send_command("QUIT")

client_socket.close()
