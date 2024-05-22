import pygame
import sys
import random

pygame.init()

SW, SH = 800, 800

BLOCK_SIZE = 45

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    def update(self):
        global apple, highest_score

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True

        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.xdir = 1
            self.ydir = 0
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.dead = False
            apple = Apple()
            highest_score = max(highest_score, len(self.body) - 1)

        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

score_font = pygame.font.Font(None, 36)

def draw_scores(current_score, highest_score):
    current_score_text = score_font.render(f"Score: {current_score}", True, "white")
    highest_score_text = score_font.render(f"High Score: {highest_score}", True, "white")
    screen.blit(current_score_text, (10, 10))
    screen.blit(highest_score_text, (10, 40))

drawGrid()

snake = Snake()
apple = Apple()
highest_score = 0
paused = False  # Track whether the game is paused

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.ydir = 0
                snake.xdir = -1
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        snake.update()

        screen.fill("black")
        drawGrid()
        apple.update()

        current_score = len(snake.body) - 1
        highest_score = max(highest_score, current_score)
        draw_scores(current_score, highest_score)

        pygame.draw.rect(screen, "green", snake.head)
        for square in snake.body:
            pygame.draw.rect(screen, "green", square)

        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()

    pygame.display.update()
    clock.tick(8)
