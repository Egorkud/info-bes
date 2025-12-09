import socket
import time

HOST = '127.0.0.1'
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input("Enter message: ")
start = time.perf_counter()
client.sendto(message.encode(), (HOST, PORT))

data, addr = client.recvfrom(1024)
end = time.perf_counter()

print(end - start)
print("Server:", data.decode())
