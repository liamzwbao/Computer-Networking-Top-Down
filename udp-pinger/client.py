from datetime import datetime
from socket import *

server_name = "localhost"
server_port = 12000
# Create a client UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

sent = 10
rtts = []
lost = 0

for i in range(sent):
    start_time = datetime.now()
    message = f"Ping {i + 1} {start_time}: "
    print(message, end="")

    client_socket.sendto(message.encode(), (server_name, server_port))

    try:
        client_socket.recvfrom(1024)
        rtt = (datetime.now() - start_time).total_seconds() * 1000
        rtts.append(rtt)
        print(f"RTT: {rtt:.3f}ms")
    except timeout:
        lost += 1
        print("Request timed out")

client_socket.close()

loss_rate = lost / sent
rtt_min = min(rtts)
rtt_max = max(rtts)
rtt_avg = sum(rtts) / len(rtts)
print(f"\nPing statistics for {server_name}:")
print(f"\tPackets: Sent = {sent}, Received = {len(rtts)}, Lost = {lost} ({loss_rate * 100:.2f}% loss),")
print("Approximate round trip times (RTTs) in milli-seconds:")
print(f"\tMinimum = {rtt_min:.3f}ms, Maximum = {rtt_max:.3f}ms, Average = {rtt_avg:.3f}ms")
