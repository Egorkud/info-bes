import socket
import time

HOST = '127.0.0.1'
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(1)

message = input("Enter message: ")

for i in range(100):
    try:
        start = time.perf_counter()
        client.sendto(message.encode(), (HOST, PORT))

        data, addr = client.recvfrom(1024)
        end = time.perf_counter()

        print(f"Iteration {i}: {end - start:.6f} sec")
        print("Server:", data.decode())

    except socket.timeout:
        print(f"Iteration {i}: Timeout!")
        continue
