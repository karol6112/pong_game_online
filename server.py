import socket
import threading

SIZE = 1024
HOST = "127.0.0.1"
PORT = 6240

FORMAT = 'utf-8'


def handle_client(conn, addr):
    print(f"[NEW CONNECTION {addr} connected.")

    connected = True
    while connected:
        message = conn.recv(SIZE).decode(FORMAT)
        if message == "stop":
            connected = False

        print(f"[{addr}] {message}")
        conn.send("Message send".encode(FORMAT))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")