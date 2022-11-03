import socket
import keyboard

SIZE = 1024
FORMAT = "utf-8"
HOST = "127.0.0.1"
PORT = 6240


def send(client, mes):
    message = mes.encode(FORMAT)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    run = True
    while run:

        mes = "OK"
        client.send(mes.encode(FORMAT))

        if keyboard.read_key() == 'a':
            client.send(mes.encode(FORMAT))

        message = client.recv(1024).decode(FORMAT)
        print(message)
        if message == 'stop':
            break
