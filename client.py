import socket
import pygame

SIZE = 1024
FORMAT = "utf-8"
HOST = "127.0.0.1"
PORT = 6240


WIDTH, HEIGHT = 900, 500
WIN_SIZE = 500

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
VEL = 20
BALL_VEL = 10
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 10


pygame.init()
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))

class Ball():

    def __init__(self):
        self.x = WIN_SIZE/2
        self.y = WIN_SIZE/2
        self.color = BLUE
        self.radius = 10
        self.velocity_x = BALL_VEL
        self.velocity_y = BALL_VEL
        self.shape = (self.x, self.y)
        self.step = 1

    def get_pos(self):
        return self.x, self.y

    def draw_ball(self):
        pygame.draw.circle(screen, self.color, (self.shape), self.radius)

    #testowo klawiszse
    def ball_movement(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.velocity_y

        if keys[pygame.K_s]:
            self.y += self.velocity_y

        self.update()

    def update(self):
        self.shape = (self.x, self.y)



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


# def send(client, mes):
#     message = mes.encode(FORMAT)
#     client.send(message)
#     print(client.recv(1024).decode(FORMAT))


def main_game():

    player = Player(50, 50, 200, 50, (0, 0, 0))
    player2 = Player(300, 300, 200, 50, (255, 0, 0))
    ball = Ball()

    client.send("initializing".encode(FORMAT))
    cord = client.recv(1024).decode(FORMAT)
    player.x, player.y = eval(cord)
    client.send(cord.encode(FORMAT))

    ball_cord = client.recv(1024).decode(FORMAT)
    ball.x, ball.y = eval(ball_cord)

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

        #ball
        ball_pos = ball.get_pos()
        client.send(str(ball_pos).encode(FORMAT))

        ball_pos = client.recv(1024).decode(FORMAT)
        ball.x, ball.y = eval(ball_pos)
        ball.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        player.move(WIN_SIZE)
        ball.ball_movement()
        redraw_window(screen, player, player2, ball)


def redraw_window(screen, player, player2, ball):
    screen.fill((255, 255, 255))
    player.draw(screen)
    player2.draw(screen)
    ball.draw_ball()
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

