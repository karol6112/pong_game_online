import socket
import threading
import time

SIZE = 1024
PORT = 5555

HOST = "127.0.0.1"
FORMAT = 'utf-8'


players_pos = [(0,0), (890,0)]
ball_position = (450, 250)



def convert_message(message):
    message = message.strip("()")
    message = message.split(",")
    return (int(message[0]), int(message[1]))


def handle_client(conn, addr, client_number):
    print(f"[NEW CONNECTION {addr} connected.")
    # connected = True
    #player_cord
    conn.recv(1024).decode(FORMAT)
    conn.send(str(players_pos[client_number-1]).encode(FORMAT))
    conn.recv(1024).decode(FORMAT)

    #ball_cord
    global ball_position
    conn.send(str(ball_position).encode(FORMAT))

    while True:
        if (threading.active_count() -1) == 2:
            connected = True
            time.sleep(1)
            break
    # connected = True

    while connected:
        #pobieramy kordy gracza
        message = conn.recv(SIZE).decode(FORMAT)

        # if message == "stop":
        #     connected = False
        #print(players_pos[client_number-1])
        #print(convert_message(message))

        players_pos[client_number-1] = convert_message(message)

        #jezeli gracz 1 to
        if client_number == 2:
            conn.send(str(players_pos[0]).encode(FORMAT))
        else:
            conn.send(str(players_pos[1]).encode(FORMAT))

        #polozenie pilki
        message = conn.recv(SIZE).decode(FORMAT)
        ball_position = convert_message(message)
        print(ball_position)
        conn.send(str(ball_position).encode(FORMAT))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(2)
    while True:
        conn, addr = server.accept()
        client_number = threading.active_count()
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_number))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
