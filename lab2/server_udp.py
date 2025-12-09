import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 5001))
print('Server started at 127.0.0.1:5001')

while True:
    data, addr = server.recvfrom(1024)
    print(f"Client {addr} sent {data}")

    response = data.decode().upper().encode()
    server.sendto(response, addr)
