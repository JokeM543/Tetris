import pygame
import random

pygame.init()

# Set up the display
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

colors = [
    (0, 0, 0),  # Black
    (255, 85, 85),  # Red
    (100, 200, 115),  # Green
    (120, 108, 245),  # Blue
    (255, 140, 50),  # Orange
    (50, 120, 52),  # Dark Green
    (146, 202, 73),  # Light Green
    (150, 75, 0)  # Brown
]

tetriminos = [
    [[1, 1, 1, 1]],  # I shape
    [[2, 2, 2],
     [0, 0, 2]],  # J shape
    [[3, 3, 3],
     [3, 0, 0]],  # L shape
    [[4, 4],
     [4, 4]],  # O shape
    [[0, 5, 5],
     [5, 5, 0]],  # S shape
    [[6, 6, 6],
     [0, 6, 0]],  # T shape
    [[7, 7, 0],
     [0, 7, 7]]  # Z shape
]

grid_height = 20
grid_width = 10
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Variables for current piece
current_piece = None
piece_x = 0
piece_y = 0

def new_piece():
    global current_piece, piece_x, piece_y
    current_piece = random.choice(tetriminos)
    piece_x = grid_width // 2 - len(current_piece[0]) // 2
    piece_y = 0
    if check_collision(piece_x, piece_y, current_piece):
        print("Game Over!")
        pygame.quit()

def rotate_piece():
    global current_piece
    rotated = [list(i) for i in zip(*current_piece[::-1])]
    if not check_collision(piece_x, piece_y, rotated):
        current_piece = rotated

def check_collision(x, y, piece):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] > 0:
                if (x + j < 0 or x + j >= grid_width or y + i >= grid_height):
                    return True
                if grid[y + i][x + j] > 0:
                    return True
    return False

def fix_piece():
    global grid, current_piece, piece_x, piece_y
    for i in range(len(current_piece)):
        for j in range(len(current_piece[0])):
            if current_piece[i][j] > 0:
                grid[piece_y + i][piece_x + j] = current_piece[i][j]
    new_piece()

def draw_grid():
    screen.fill(colors[0])
    for i in range(grid_height):
        for j in range(grid_width):
            color_index = grid[i][j]
            pygame.draw.rect(screen, colors[color_index], (j * 30, i * 30, 30, 30), 0)
    if current_piece is not None:
        for i in range(len(current_piece)):
            for j in range(len(current_piece[0])):
                if current_piece[i][j] != 0:
                    pygame.draw.rect(screen, colors[current_piece[i][j]], ((piece_x + j) * 30, (piece_y + i) * 30, 30, 30), 0)
    pygame.display.update()

def clear_lines():
    global grid
    cleared_lines = 0
    new_grid = []

    # Check each row in the grid if it's full
    for row in grid:
        if 0 not in row:
            cleared_lines += 1 
        else:
            new_grid.append(row) 

    # Add empty rows at the top of the grid for each cleared line
    for _ in range(cleared_lines):
        new_grid.insert(0, [0 for _ in range(grid_width)])

    grid = new_grid
    return cleared_lines


new_piece()

running = True
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 1000

while running:
    current_time = pygame.time.get_ticks()
    if current_time - fall_time > fall_speed:
        fall_time = current_time
        if not check_collision(piece_x, piece_y + 1, current_piece):
            piece_y += 1
        else:
            fix_piece()
            cleared_lines = clear_lines()
            print(f"Cleared {cleared_lines} lines")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(piece_x - 1, piece_y, current_piece):
                    piece_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(piece_x + 1, piece_y, current_piece):
                    piece_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(piece_x, piece_y + 1, current_piece):
                    piece_y += 1
            elif event.key == pygame.K_UP:
                rotate_piece()

    draw_grid()
    clock.tick(10)


pygame.quit()
