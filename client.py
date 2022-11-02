import socket
import pygame

SIZE = 1024
FORMAT = "utf-8"
HOST = "127.0.0.1"
PORT = 6240

WINDOW = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("PONG")

def send(client, mes):
    message = mes.encode(FORMAT)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    run = True
    while run:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            send(client, "WW")
        if key_pressed[pygame.K_s]:
            send(client, "stop")