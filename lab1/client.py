import socket
import time

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = input("Введіть повідомлення: ")

    start = time.perf_counter()
    s.sendall(message.encode())

    data = s.recv(1024)
    end = time.perf_counter()

    print(end - start)
    print("Від сервера:", data.decode())
