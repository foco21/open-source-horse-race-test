import pygame
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

        info_text = font_small.render(f'Horse {horse_index + 1} wins round {current_round} in {elapsed_time:.2f}s!', True, WHITE)
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

running = True
while running and current_round <= rounds:
    create_maze()
    for horse in horses:
        horse['pos'] = get_valid_spawn()
        horse['dir'] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        horse['attracted'] = False
    frames_since_start = 0
    move_delay = 0

    round_active = True
    round_start_time = time.time()
    while round_active:
        clock.tick(7)

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

# Display final standings
screen.fill(BLACK)
font_big = pygame.font.SysFont(None, 50)
end_text = font_big.render("Final Rankings", True, WHITE)
screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, 50))

sorted_horses = sorted(enumerate(horse_wins), key=lambda x: x[1], reverse=True)

for rank, (horse_index, wins) in enumerate(sorted_horses):
    result_text = font_small.render(f"{rank+1}. Horse {horse_index+1}: {wins} wins", True, WHITE)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 150 + rank * 40))

pygame.display.update()
pygame.time.delay(7000)
pygame.quit()

