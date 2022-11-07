import socket
import threading

SIZE = 1024
PORT = 6240

HOST = "127.0.0.1"
FORMAT = 'utf-8'


def handle_client(conn, addr, client_number):
    print(f"[NEW CONNECTION {addr} connected.")
    connected = True
    while connected:
        # if client_number > 2:
        #     conn.send("stop".encode(FORMAT))
        #     connected = False
        #     continue

        message = conn.recv(SIZE).decode(FORMAT)
        if message == "stop":
            connected = False


        print(f"[{addr}] {message}")
        message_to_send = "XXX"
        conn.send(message_to_send.encode(FORMAT))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(2)
    while True:
        conn, addr = server.accept()
        client_number = threading.activeCount()
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_number))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
