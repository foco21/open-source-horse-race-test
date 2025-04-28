import pygame
import random
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
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
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Carrot
carrot_pos = (COLS - 2, ROWS - 2)

# Load Horse Sprites
horse_sprites = [
    pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse1.png'),
    pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse2.png'),
    pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse3.png'),
    pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse4.png'),
    pygame.image.load(r'C:\\Users\\summe\\Desktop\\horse\\horse5.png')
]

# Horses
horses = []
start_positions = [[1, 1], [2, 1], [1, 2], [2, 2], [3, 1]]

for i in range(len(horse_sprites)):
    horses.append({
        'pos': start_positions[i][:],
        'sprite': pygame.transform.scale(horse_sprites[i], (CELL_SIZE + 4, CELL_SIZE + 4)),
        'sprite_big': pygame.transform.scale(horse_sprites[i], (CELL_SIZE * 2, CELL_SIZE * 2)),
        'dir': random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]),
        'attracted': False
    })

# Functions

def create_maze():
    global maze
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

    # Clear spawn room
    for i in range(5):
        for j in range(5):
            maze[j][i] = 0

    # Carve path to carrot
    stack = [(4, 4)]
    maze[4][4] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        if x > 2 and maze[y][x - 2] == 1:
            neighbors.append((x - 2, y))
        if x < COLS - 3 and maze[y][x + 2] == 1:
            neighbors.append((x + 2, y))
        if y > 2 and maze[y - 2][x] == 1:
            neighbors.append((x, y - 2))
        if y < ROWS - 3 and maze[y + 2][x] == 1:
            neighbors.append((x, y + 2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[(y + ny) // 2][(x + nx) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    # Create random large open areas
    for _ in range(40):
        chunk_x = random.randint(0, COLS - 4)
        chunk_y = random.randint(0, ROWS - 4)
        for dy in range(3):
            for dx in range(3):
                if 0 <= chunk_x + dx < COLS and 0 <= chunk_y + dy < ROWS:
                    maze[chunk_y + dy][chunk_x + dx] = 0

def get_valid_spawn():
    return [random.randint(1, 3), random.randint(1, 3)]

def is_collision(x, y, current_horse):
    for other in horses:
        if other != current_horse and other['pos'] == [x, y]:
            return True
    return False

def move_horses():
    global frames_since_start, move_counter
    move_counter += 1
    if move_counter % 5 != 0:
        return

    for horse in horses:
        if frames_since_start > 30:
            horse['attracted'] = True

        if horse['attracted'] and random.random() < 0.7:
            best_moves = []
            if horse['pos'][0] < carrot_pos[0] and maze[horse['pos'][1]][horse['pos'][0] + 1] == 0:
                best_moves.append((1, 0))
            if horse['pos'][0] > carrot_pos[0] and maze[horse['pos'][1]][horse['pos'][0] - 1] == 0:
                best_moves.append((-1, 0))
            if horse['pos'][1] < carrot_pos[1] and maze[horse['pos'][1] + 1][horse['pos'][0]] == 0:
                best_moves.append((0, 1))
            if horse['pos'][1] > carrot_pos[1] and maze[horse['pos'][1] - 1][horse['pos'][0]] == 0:
                best_moves.append((0, -1))

            if best_moves:
                horse['dir'] = random.choice(best_moves)

        if random.random() < 0.10:
            horse['dir'] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        dx, dy = horse['dir']
        new_x = horse['pos'][0] + dx
        new_y = horse['pos'][1] + dy

        if (not (0 <= new_x < COLS) or not (0 <= new_y < ROWS) or
            maze[new_y][new_x] == 1 or is_collision(new_x, new_y, horse)):
            horse['dir'] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            horse['pos'][0] += dx
            horse['pos'][1] += dy

        horse['pos'][0] = max(0, min(COLS - 1, horse['pos'][0]))
        horse['pos'][1] = max(0, min(ROWS - 1, horse['pos'][1]))

    frames_since_start += 1

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

def check_winner():
    for index, horse in enumerate(horses):
        if horse['pos'] == list(carrot_pos):
            return index
    return None

def show_winner(horse_index, elapsed_time):
    global current_round
    horse_wins[horse_index] += 1
    horse_times.append((horse_index, elapsed_time))

    font = pygame.font.SysFont(None, 100)
    t = 0
    running = True
    while running:
        t += 0.03
        r = int(127 * (1 + math.sin(t)))
        g = int(127 * (1 + math.sin(t + 2)))
        b = int(127 * (1 + math.sin(t + 4)))

        screen.fill(BLACK)
        text = font.render('ROUND WIN!', True, (r, g, b))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, rect)

        winner_sprite = horses[horse_index]['sprite_big']
        winner_rect = winner_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_sprite, winner_rect)

        info_text = pygame.font.SysFont(None, 30).render(f'Horse {horse_index + 1} wins round {current_round} in {elapsed_time:.2f}s!', True, WHITE)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT - 40))

        pygame.display.update()
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if t > 5:
            running = False

    current_round += 1

# MAIN
frames_since_start = 0
move_counter = 0
rounds = 5
current_round = 1
horse_wins = [0 for _ in range(len(horses))]
horse_times = []

running = True
while running and current_round <= rounds:
    create_maze()
    for horse in horses:
        horse['pos'] = get_valid_spawn()
        horse['dir'] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        horse['attracted'] = False
    frames_since_start = 0
    move_counter = 0

    round_active = True
    round_start_time = time.time()
    while round_active:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                round_active = False

        move_horses()

        screen.fill(WHITE)
        draw_maze()
        draw_carrot()
        draw_horses()

        winner_index = check_winner()
        if winner_index is not None:
            elapsed_time = time.time() - round_start_time
            show_winner(winner_index, elapsed_time)
            round_active = False

        pygame.display.update()

# Final Standings
screen.fill(BLACK)
font_big = pygame.font.SysFont(None, 50)
end_text = font_big.render("Final Rankings", True, WHITE)
screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, 50))

sorted_horses = sorted(enumerate(horse_wins), key=lambda x: x[1], reverse=True)

for rank, (horse_index, wins) in enumerate(sorted_horses):
    result_text = pygame.font.SysFont(None, 30).render(f"{rank+1}. Horse {horse_index+1}: {wins} wins", True, WHITE)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 150 + rank * 40))

pygame.display.update()
pygame.time.delay(7000)
pygame.quit()
