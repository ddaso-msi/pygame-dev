import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan (I)
    (255, 255, 0),  # Yellow (O)
    (255, 165, 0),  # Orange (L)
    (0, 0, 255),    # Blue (J)
    (0, 255, 0),    # Green (S)
    (255, 0, 0),    # Red (Z)
    (128, 0, 128)   # Purple (T)
]

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock to control game speed
clock = pygame.time.Clock()

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 0], [1, 1, 1]]   # T
]

# Function to create a new tetromino
def create_tetromino():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {
        "shape": shape,
        "color": color,
        "x": SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2,
        "y": 0
    }

# Function to draw a tetromino
def draw_tetromino(tetromino):
    shape = tetromino["shape"]
    color = tetromino["color"]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    color,
                    ((tetromino["x"] + x) * BLOCK_SIZE, (tetromino["y"] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    screen,
                    GRAY,
                    ((tetromino["x"] + x) * BLOCK_SIZE, (tetromino["y"] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

# Function to check for collisions
def check_collision(board, tetromino):
    shape = tetromino["shape"]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board_x = tetromino["x"] + x
                board_y = tetromino["y"] + y
                if (
                    board_x < 0 or board_x >= SCREEN_WIDTH // BLOCK_SIZE or
                    board_y >= SCREEN_HEIGHT // BLOCK_SIZE or
                    (board_y >= 0 and board[board_y][board_x])
                ):
                    return True
    return False

# Function to merge tetromino into the board
def merge_tetromino(board, tetromino):
    shape = tetromino["shape"]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[tetromino["y"] + y][tetromino["x"] + x] = tetromino["color"]

# Function to clear completed lines
def clear_lines(board):
    lines_cleared = 0
    for y in range(len(board)):
        if all(board[y]):
            del board[y]
            board.insert(0, [None] * (SCREEN_WIDTH // BLOCK_SIZE))
            lines_cleared += 1
    return lines_cleared

# Function to draw the board
def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    cell,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    screen,
                    GRAY,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

# Main game loop
def main():
    board = [[None for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    tetromino = create_tetromino()
    score = 0
    level = 1
    fall_time = 0
    fall_speed = 500  # Milliseconds

    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino["x"] -= 1
                    if check_collision(board, tetromino):
                        tetromino["x"] += 1
                if event.key == pygame.K_RIGHT:
                    tetromino["x"] += 1
                    if check_collision(board, tetromino):
                        tetromino["x"] -= 1
                if event.key == pygame.K_DOWN:
                    tetromino["y"] += 1
                    if check_collision(board, tetromino):
                        tetromino["y"] -= 1
                if event.key == pygame.K_UP:
                    # Rotate tetromino
                    rotated = list(zip(*reversed(tetromino["shape"])))
                    original_shape = tetromino["shape"]
                    tetromino["shape"] = rotated
                    if check_collision(board, tetromino):
                        tetromino["shape"] = original_shape

        # Automatically move tetromino down
        if fall_time >= fall_speed:
            tetromino["y"] += 1
            if check_collision(board, tetromino):
                tetromino["y"] -= 1
                merge_tetromino(board, tetromino)
                lines_cleared = clear_lines(board)
                score += lines_cleared * 100
                level = 1 + score // 500
                fall_speed = max(100, 500 - (level - 1) * 50)
                tetromino = create_tetromino()
                if check_collision(board, tetromino):
                    running = False
            fall_time = 0

        # Draw everything
        draw_board(board)
        draw_tetromino(tetromino)

        # Display score and level
        font = pygame.font.SysFont("comicsansms", 20)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 50))
        screen.blit(level_text, (10, SCREEN_HEIGHT - 30))

        pygame.display.update()

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()