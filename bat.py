import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Accelerating Bat Movement with Animation")

# Define colors
BLACK = (0, 0, 0)

# Load the bat sprite sheet
bat_sprite_sheet = pygame.image.load('bat_sprite.png')

# Define bat attributes
frame_width = 32
frame_height = 32
scale_factor = 2  # Scale factor for bat size (increase this value to make the bat bigger)
bat_width = frame_width * scale_factor
bat_height = frame_height * scale_factor
bat_x = screen_width // 2 - bat_width // 2
bat_y = screen_height // 2 - bat_height // 2
bat_speed = 4
max_speed = 10  # Max speed when accelerating
acceleration = 0.2  # Rate of acceleration
deceleration = 0.1  # Rate of deceleration
current_speed = bat_speed

# Define bat movement directions
dx, dy = 0, 0  # Change in position

# Animation control
frame_index = 0  # Starting frame index
frame_count = 4  # Assuming 4 frames in each row for animation
frame_time = 100  # Time in ms for each frame
last_frame_time = pygame.time.get_ticks()

# Load frames for the bat's movement (assuming sprite sheet is organized)
def get_frame(row, col):
    return bat_sprite_sheet.subsurface(col * frame_width, row * frame_height, frame_width, frame_height)

# Set up the clock for frame rate
clock = pygame.time.Clock()

# Function to move the bat
def move_bat():
    global bat_x, bat_y, dx, dy, current_speed

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        dx = -current_speed
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        dx = current_speed
    elif pygame.key.get_pressed()[pygame.K_UP]:
        dy = -current_speed
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        dy = current_speed
    else:
        # If no arrow key is pressed, stop moving in that direction
        dx = 0
        dy = 0
    
    # If space is pressed, apply acceleration
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        if current_speed < max_speed:
            current_speed += acceleration
    else:
        # Decelerate when space is released
        if current_speed > bat_speed:
            current_speed -= deceleration

    bat_x += dx
    bat_y += dy

# Function to update the frame for animation
def update_frame():
    global frame_index, last_frame_time
    current_time = pygame.time.get_ticks()
    
    if current_time - last_frame_time > frame_time:  # Change frame after the specified time
        frame_index = (frame_index + 1) % frame_count  # Loop back to the first frame
        last_frame_time = current_time

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the bat
    move_bat()

    # Update the frame for animation
    update_frame()

    # Clear the screen
    screen.fill(BLACK)

    # Scale and update the bat's image (for simplicity, just show a frame from the sprite sheet)
    if dx > 0:  # Moving to the right
        screen.blit(pygame.transform.scale(get_frame(1, frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 1 is flying right
    elif dx < 0:  # Moving to the left
        screen.blit(pygame.transform.scale(get_frame(3, frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 3 is flying left
    elif dy < 0:  # Moving upwards
        screen.blit(pygame.transform.scale(get_frame(2, frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 2 is flying up
    elif dy > 0:  # Moving downwards
        screen.blit(pygame.transform.scale(get_frame(2, frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 2 is flying down
    else:
        screen.blit(pygame.transform.scale(get_frame(0, frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Flying animation when no keys are pressed

    # Update the screen
    pygame.display.update()

    # Frame rate control
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()