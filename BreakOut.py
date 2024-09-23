import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

my_rect = pygame.Rect((0, 0, 100, 100))

class Player(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x,y, 150,25) #arbitrary values TODO modify
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'black', self, 0)#fill
        pygame.draw.rect(screen, 'white', self, 1) #outline

    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball(pygame.Rect):
    def __init__(self, x, y, diameter):
        super().__init__(x, y , diameter, diameter)
        self.vx = 0#random.randint(3,8) * random.choice([1,-1])
        self.vy = random.randint(7,8) #  TODO tweak

    def draw(self):
        pygame.draw.ellipse(screen, 'white', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Bounce off left or right walls
        if self.left <= 0 or self.right >= screen.get_width():
            self.vx = -self.vx
        # Bounce off top or wall
        if self.top <= 0:
            self.vy = -self.vy
        if  self.bottom >= screen.get_height():
            self.x = screen.get_width()//2
            self.y = 400

class Brick(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 25)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0)
        pygame.draw.rect(screen, 'black', self, 1)




player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2 - 10, 400, 20)
bricks = []
for i in range (0,8):
    for j in range (0,4):
        bricks.append(Brick(100+150*i, 100+ 75*j))


while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx -= 10
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += 10
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += 10
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx -= 10



    # Do logical updates here.

    player.update()
    ball.update()

    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width
        dist = ball.x + ball.width/2 - (player.x + player.width/2)
        if ball.vx + dist//10 > 9:
            ball.vx = 9
        else:
            ball.vx += dist//10

    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball.vy*= -1




    screen.fill('maroon')  # Fill the display with a solid color

    # Render the graphics here.

    player.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)


