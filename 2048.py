import pygame
import random
import numpy as np
from collections import defaultdict
import os
import itertools
import sys
import time

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library using defaultdict
colors = defaultdict(lambda: (0, 0, 0))
colors.update({
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'bg': (187, 173, 160)
})

board_values = np.zeros((4, 4), dtype=int)
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0

with open(os.path.join(os.getcwd(), 'high_score'), 'r') as file:
    init_high = int(file.readline())

high_score = init_high

def draw_over():
    pygame.draw.rect(screen, colors['other'], [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, colors['light text'])
    game_over_text2 = font.render('Press Enter to Restart', True, colors['light text'])
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

def take_turn(direc, board):
    global score
    merged = np.zeros((4, 4), dtype=bool)
    # ... [rest of the function logic remains the same]

def new_pieces(board):
    count = 0
    full = False
    while 0 in board and count < 1:
        row, col = random.choice(list(itertools.product(range(4), repeat=2)))
        if board[row][col] == 0:
            count += 1
            board[row][col] = 4 if random.randint(1, 10) == 10 else 2
    return board, count < 1

def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, colors['dark text'])
    high_score_text = font.render(f'High Score: {high_score}', True, colors['dark text'])
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))

def draw_pieces(board):
    for i, j in itertools.product(range(4), repeat=2):
        value = board[i][j]
        value_color = colors['light text'] if value > 8 else colors['dark text']
        pygame.draw.rect(screen, colors[value], [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
        if value > 0:
            value_len = len(str(value))
            font_size = 48 - (5 * value_len)
            value_font = pygame.font.Font('freesansbold.ttf', font_size)
            value_text = value_font.render(str(value), True, value_color)
            text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
            screen.blit(value_text, text_rect)
            pygame.draw.rect(screen, colors['other'], [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction:
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            with open('high_score', 'w') as file:
                file.write(f'{high_score}')
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
