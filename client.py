import socket
import keyboard
import pygame

SIZE = 1024
FORMAT = "utf-8"
HOST = "127.0.0.1"
PORT = 6240


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 5
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)

    def move(self, WIN_SIZE):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.x <= 0:
                self.x = 0
            else:
                self.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            if self.x >= WIN_SIZE - self.width:
                self.x = WIN_SIZE - self.width
            else:
                self.x += self.velocity

        self.update()
        
    def update(self):
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_pos(self):
        return self.x, self.y


def send(client, mes):
    message = mes.encode(FORMAT)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


def main_game():
    WIN_SIZE = 500
    pygame.init()
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))

    player = Player(50, 50, 200, 50, (0, 0, 0))
    player2 = Player(300, 300, 200, 50, (255, 0, 0))

    client.send("initializing".encode(FORMAT))
    cord = client.recv(1024).decode(FORMAT)
    player.x, player.y = eval(cord)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        #pobieramy kordy gracza i wysylamy na server
        pos = player.get_pos()
        client.send(str(pos).encode(FORMAT))

        #pobieramy kordy drugiego gracza 
        p2pos = client.recv(1024).decode(FORMAT)

        #aktualizujemy pozycje drugiego gracza 
        player2.x, player2.y = eval(p2pos)
        player2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        player.move(WIN_SIZE)
        redraw_window(screen, player, player2)


def redraw_window(screen, player, player2):
    screen.fill((255, 255, 255))
    player.draw(screen)
    player2.draw(screen)
    pygame.display.update()







with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    run = True
    while run:
        #potem tutaj main_game()
        #game start
        main_game()
        

        message = client.recv(1024).decode(FORMAT)
        print(message)
        if message == 'stop':
            break

