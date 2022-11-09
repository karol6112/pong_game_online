import socket
import threading

SIZE = 1024
PORT = 6240

HOST = "127.0.0.1"
FORMAT = 'utf-8'

players_pos = [(50,50), (300,300)]

def convert_message(message):
    message = message.strip("()")
    message = message.split(",")
    return (int(message[0]), int(message[1]))

def handle_client(conn, addr, client_number):
    print(f"[NEW CONNECTION {addr} connected.")
    connected = True
    conn.recv(1024).decode(FORMAT)
    conn.send(str(players_pos[client_number-1]).encode(FORMAT))
    while connected:
        #pobieramy kordy gracza
        message = conn.recv(SIZE).decode(FORMAT)

        if message == "stop":
            connected = False

        #print(players_pos[client_number-1])
        #print(convert_message(message))
        players_pos[client_number-1] = convert_message(message)
        #jezeli gracz 1 to
        if client_number == 2:
            conn.send(str(players_pos[0]).encode(FORMAT))
        else:
            conn.send(str(players_pos[1]).encode(FORMAT))
        

        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(2)
    while True:
        conn, addr = server.accept()
        client_number = threading.active_count()
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_number))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
