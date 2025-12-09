import socket
import time
from datetime import datetime

LOG_FILE = "udp_log.txt"
HOST = '127.0.0.1'
PORT = 5001


def log_data(data: str) -> None:
    with open(LOG_FILE, "a", encoding="UTF-8") as f:
        f.write(data)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(1)

message = input("Enter message: ")

for i in range(100):
    try:
        start = time.perf_counter()
        client.sendto(message.encode(), (HOST, PORT))

        data, addr = client.recvfrom(1024)
        end = time.perf_counter()
        timestamp = datetime.utcnow().isoformat()

        log_data(f"{timestamp} | UDP | SUCCESSFUL | seq={i} | rtt={end - start:.6f} | msg={message}\n")
        print("Server:", data.decode())

    except socket.timeout:
        print(f"Iteration {i}: Timeout!")
        timestamp = datetime.utcnow().isoformat()
        end = time.perf_counter()
        log_data(f"{timestamp} | UDP | LOST | seq={i} | rtt={end - start:.6f} | msg={message}\n")
        continue
