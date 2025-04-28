import pygame
import random
import sys
import math  # <-- add this

# Initialize Pygame
pygame.init()

# Settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARROT_COLOR = (255, 165, 0)

# Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horse Race!")

# Clock
clock = pygame.time.Clock()

# Maze
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Carrot
carrot_pos = (COLS // 2, ROWS // 2)

# Load Horse Sprites
horse_sprites = [
    pygame.transform.scale(pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse1.png'), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse2.png'), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse3.png'), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse4.png'), (CELL_SIZE, CELL_SIZE)),
    pygame.transform.scale(pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse5.png'), (CELL_SIZE, CELL_SIZE))
]

# Horses
horses = []

start_positions = [[0, 0], [1, 0], [0, 1], [1, 1], [2, 0]]

for i in range(len(horse_sprites)):
    horses.append({
        'pos': start_positions[i],
        'sprite': horse_sprites[i]
    })

# Functions

def create_maze():
    global maze
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    path = []
    x, y = 0, 0
    path.append((x, y))

    while (x, y) != carrot_pos:
        options = []
        if x < carrot_pos[0]:
            options.append((x + 1, y))
        if y < carrot_pos[1]:
            options.append((x, y + 1))
        if options:
            x, y = random.choice(options)
            path.append((x, y))

    for row in range(ROWS):
        for col in range(COLS):
            if (col, row) not in path and random.random() < 0.35:
                maze[row][col] = 1

def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

def draw_carrot():
    rect = pygame.Rect(carrot_pos[0] * CELL_SIZE, carrot_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, CARROT_COLOR, rect)

def draw_horses():
    for horse in horses:
        rect = horse['sprite'].get_rect()
        rect.topleft = (horse['pos'][0] * CELL_SIZE, horse['pos'][1] * CELL_SIZE)
        screen.blit(horse['sprite'], rect)

def move_horses():
    for horse in horses:
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            new_x = horse['pos'][0] + dx
            new_y = horse['pos'][1] + dy

            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                if maze[new_y][new_x] == 0:
                    collision = False
                    for other in horses:
                        if other != horse and other['pos'] == [new_x, new_y]:
                            collision = True
                            break
                    if not collision:
                        horse['pos'] = [new_x, new_y]
                        break

def check_winner():
    for horse in horses:
        if horse['pos'] == list(carrot_pos):
            return horse['sprite']
    return None

# THIS IS THE NEW UPDATED FUNCTION ↓↓↓
def show_winner(sprite):
    font = pygame.font.SysFont(None, 100)
    t = 0
    running = True
    while running:
        t += 0.03
        r = int(127 * (1 + math.sin(t)))
        g = int(127 * (1 + math.sin(t + 2)))
        b = int(127 * (1 + math.sin(t + 4)))

        screen.fill(BLACK)
        text = font.render('YOU WIN!', True, (r, g, b))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.blit(sprite, (WIDTH // 2 - CELL_SIZE // 2, HEIGHT // 2 - CELL_SIZE // 2 - 100))
        screen.blit(text, rect)
        pygame.display.update()
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if t > 20:
            running = False

    pygame.quit()
    sys.exit()

# MAIN

create_maze()

running = True
while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_horses()

    screen.fill(WHITE)
    draw_maze()
    draw_carrot()
    draw_horses()

    winner_sprite = check_winner()
    if winner_sprite:
        show_winner(winner_sprite)

    pygame.display.update()

pygame.quit()
