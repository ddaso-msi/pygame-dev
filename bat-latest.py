import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bat Animation with Enemies")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

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

# Animation control for bat
bat_frame_index = 0  # Starting frame index for bat animation
bat_frame_count = 4  # Number of frames per row for bat animation
bat_frame_time = 100  # Time in ms for each frame
bat_last_frame_time = pygame.time.get_ticks()

# Define projectile attributes
projectiles = []  # List to store active projectiles
projectile_speed = 10  # Speed of the projectiles
projectile_size = 5  # Size of the projectile
projectile_speed_multiplier = 2 


def create_mask(image):
    """Create a mask for the given image."""
    return pygame.mask.from_surface(image)

# Load frames for the bat's movement (assuming sprite sheet is organized)
def get_frame(row, col):
    return bat_sprite_sheet.subsurface(col * frame_width, row * frame_height, frame_width, frame_height)

# Set up the clock for frame rate
clock = pygame.time.Clock()

# Define the play button outside of the functions
play_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 60, 150, 40)
# Variables for Start Screen
username = ''
font = pygame.font.SysFont(None, 36)

# Function to draw start page
def draw_start_page():
    screen.fill(BLACK)

    # Draw instructions
    title_text = font.render("Enter Your Username", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 50))

    # Draw username input
    input_box = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 40)
    pygame.draw.rect(screen, WHITE, input_box, 2)
    username_text = font.render(username, True, WHITE)
    screen.blit(username_text, (input_box.x + 10, input_box.y + 10))

    # Draw the Play button
    pygame.draw.rect(screen, BLUE, play_button)
    play_text = font.render("Play", True, WHITE)
    screen.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2,
                            play_button.y + play_button.height // 2 - play_text.get_height() // 2))

    pygame.display.update()

# Function to handle username input
def handle_username_input(event):
    global username
    if event.key == pygame.K_BACKSPACE:
        username = username[:-1]
    else:
        username += event.unicode

    # Prevent username from being too long
    if len(username) > 20:
        username = username[:20]

def fire_projectile():
    """Create a new projectile at the bat's current position with bat's direction."""
    if dx == 0 and dy == 0:
        print("Cannot fire: bat is stationary!")  # Debug
        return
    
    projectile_x = bat_x + 10  # Adjust offset to center the projectile on the bat
    projectile_y = bat_y
    projectile_dx = dx * projectile_speed_multiplier
    projectile_dy = dy * projectile_speed_multiplier

    print(f"Firing projectile from ({projectile_x}, {projectile_y}) with velocity ({projectile_dx}, {projectile_dy})")  # Debug
    projectiles.append({'x': projectile_x, 'y': projectile_y, 'dx': projectile_dx, 'dy': projectile_dy})

def update_projectiles():
    """Move projectiles and remove off-screen ones."""
    for projectile in projectiles[:]:
        projectile['x'] += projectile['dx']  # Update x-coordinate
        projectile['y'] += projectile['dy']  # Update y-coordinate
        
        # Remove projectiles that move off-screen
        if projectile['x'] < 0 or projectile['x'] > screen_width or projectile['y'] < 0 or projectile['y'] > screen_height:
            projectiles.remove(projectile)
            print("Projectile removed (off-screen)")  # Debug

def draw_projectiles():
    """Draw all projectiles on the screen."""
    for projectile in projectiles:
        pygame.draw.circle(screen, (255, 0, 0), (int(projectile['x']), int(projectile['y'])), projectile_size)

# def draw_projectiles(screen):
#     """Draw all projectiles on the screen."""
#     for projectile in projectiles:
#         print("fired")
#         pygame.draw.circle(screen, (255, 0, 0), (screen_width // 2 - bat_width // 2, screen_height // 2 - bat_height // 2), projectile_size)

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
# Function to update the bat's animation frame
def update_bat_frame():
    global bat_frame_index, bat_last_frame_time
    current_time = pygame.time.get_ticks()
    
    if current_time - bat_last_frame_time > bat_frame_time:  # Change frame after the specified time
        bat_frame_index = (bat_frame_index + 1) % bat_frame_count  # Loop back to the first frame
        bat_last_frame_time = current_time

# Enemy settings
enemy_width = 64
enemy_height = 64
enemy_frame_time = 100  # Time between frames for enemy animation
enemy_frame_index = 0
enemy_frame_count = 8  # Assuming 8 frames for the enemy animation
enemy_last_frame_time = pygame.time.get_ticks()

# Load enemy sprite frames from a folder
enemy_frames = [pygame.image.load(f'enemy-frames/frame-{i + 1}.png') for i in range(enemy_frame_count)]

# Function to update enemy animation frame
def update_enemy_frame():
    global enemy_frame_index, enemy_last_frame_time
    current_time = pygame.time.get_ticks()
    
    if current_time - enemy_last_frame_time > enemy_frame_time:  # Change frame after the specified time
        enemy_frame_index = (enemy_frame_index + 1) % enemy_frame_count  # Loop back to the first frame
        enemy_last_frame_time = current_time

# Create a list to store enemy positions
enemies = []

# Function to spawn a new enemy at the bottom of the screen
# Function to spawn a new enemy at a random position
def spawn_enemy():
    # Retry logic to avoid overlapping enemies
    max_retries = 5
    for _ in range(max_retries):
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = random.randint(screen_height // 2, screen_height - enemy_height)  # Random vertical spawn
        
        # Check for overlap with existing enemies
        new_enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        overlap = any(new_enemy_rect.colliderect(pygame.Rect(enemy['x'], enemy['y'], enemy_width, enemy_height)) for enemy in enemies)
        
        if not overlap:
            # Randomize the direction for the new enemy (either 'left' or 'right')
            direction = random.choice(['left', 'right'])  # You can add more directions if needed
            
            # Add enemy with the direction to the list
            enemies.append({'x': enemy_x, 'y': enemy_y, 'time': pygame.time.get_ticks(), 'direction': direction})
            return
    
    # If maximum retries reached, skip spawning this frame
    print("Skipped spawning to prevent overlap")

# Function to fade out enemy
def fade_out_enemy(enemy_surface, alpha):
    """Apply a fade-out effect by modifying the transparency."""
    faded_surface = enemy_surface.copy()
    faded_surface.set_alpha(alpha)
    return faded_surface

# def spawn_enemy():
#     enemy_x = random.randint(0, screen_width - enemy_width)
#     enemy_y = screen_height - enemy_height
#     enemies.append({'x': enemy_x, 'y': enemy_y, 'time': pygame.time.get_ticks()})


# Function to check for collision between bat and enemy

def check_pixel_collision(bat_surface, bat_pos, enemy_surface, enemy_pos):
    """Check for pixel-perfect collision using masks."""
    bat_mask = create_mask(bat_surface)
    enemy_mask = create_mask(enemy_surface)
    
    # Calculate the offset between the two surfaces
    offset = (enemy_pos[0] - bat_pos[0], enemy_pos[1] - bat_pos[1])
    
    # Check for overlap
    return bat_mask.overlap(enemy_mask, offset) is not None

def game_over_screen():
    """Display the game over screen with a replay button."""
    global score, enemies, projectiles, bat_x, bat_y, dx, dy, current_speed

    # Define the button dimensions
    button_width = 200
    button_height = 50
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height // 2) + 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    # Reset game variables
                    score = 0
                    enemies = []
                    projectiles = []
                    bat_x = screen_width // 2
                    bat_y = screen_height // 2
                    dx, dy = 0, 0
                    current_speed = bat_speed
                    return  # Exit game over screen and restart the game loop

        # Render game over screen
        screen.fill((0, 0, 0))  # Clear screen
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))

        # Display final score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 50))

        # Draw replay button
        pygame.draw.rect(screen, (0, 128, 255), (button_x, button_y, button_width, button_height))
        font_small = pygame.font.Font(None, 36)
        replay_text = font_small.render("Replay", True, (255, 255, 255))
        screen.blit(replay_text, (button_x + (button_width - replay_text.get_width()) // 2,
                                  button_y + (button_height - replay_text.get_height()) // 2))

        pygame.display.flip()

# def check_collision(bat_rect, enemy_rect):
#     return bat_rect.colliderect(enemy_rect)

# Score counter
score = 0

# Set up a timer for 30 seconds
game_start_time = pygame.time.get_ticks()
game_duration = 30000  # 30 seconds

# Flag to track if game is started
game_started = False
# Main game loop
running = True
while running:
    if not game_started:
        # Start page logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_username_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos) and username != '':
                    game_started = True  # Start the game

        # Draw start page
        draw_start_page()
    else:
    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Fire projectile when X is pressed
            elif pygame.key.get_pressed()[pygame.K_x]:
                fire_projectile()

        # Check if 30 seconds have passed
        if pygame.time.get_ticks() - game_start_time > game_duration:
            running = False

        # Move the bat
        move_bat()
        update_projectiles()

        # Update the bat's animation frame
        update_bat_frame()

        # Update the enemy's animation frame
        update_enemy_frame()

        # Clear the screen
        screen.fill(BLACK)

        # Draw the bat's animation
        if dx > 0:  # Moving to the right
            screen.blit(pygame.transform.scale(get_frame(1, bat_frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 1 is flying right
        elif dx < 0:  # Moving to the left
            screen.blit(pygame.transform.scale(get_frame(3, bat_frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 3 is flying left
        elif dy < 0:  # Moving upwards
            screen.blit(pygame.transform.scale(get_frame(2, bat_frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 2 is flying up
        elif dy > 0:  # Moving downwards
            screen.blit(pygame.transform.scale(get_frame(2, bat_frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Assume row 2 is flying down
        else:
            screen.blit(pygame.transform.scale(get_frame(0, bat_frame_index), (bat_width, bat_height)), (bat_x, bat_y))  # Flying animation when no keys are pressed

        # Update and draw the enemies
        # Update and draw the enemies
        for enemy in enemies[:]:
            # Choose the correct direction for the enemy's surface
            if enemy['direction'] == 'left':
                enemy_surface = pygame.transform.flip(pygame.transform.scale(enemy_frames[enemy_frame_index], (enemy_width, enemy_height)), True, False)
            else:
                enemy_surface = pygame.transform.scale(enemy_frames[enemy_frame_index], (enemy_width, enemy_height))

            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_width, enemy_height)
            bat_surface = pygame.transform.scale(get_frame(0, bat_frame_index), (bat_width, bat_height))  # Assuming row 0 for idle bat

            elapsed_time = pygame.time.get_ticks() - enemy['time']
            fade_start_time = 4000  # Start fading out after 4 seconds
            fade_duration = 1000  # Duration of the fade-out effect

            # Fade-out logic
            if elapsed_time > fade_start_time:
                fade_alpha = max(0, 255 - int((elapsed_time - fade_start_time) / fade_duration * 255))
                enemy_surface = fade_out_enemy(enemy_surface, fade_alpha)

            # Remove enemy if fully faded or off the screen
            if elapsed_time > 5000 or not screen.get_rect().colliderect(enemy_rect):
                enemies.remove(enemy)
                continue

            # Check collision with the bat
            if check_pixel_collision(bat_surface, (bat_x, bat_y), enemy_surface, (enemy['x'], enemy['y'])):
                enemies.remove(enemy)  # Remove the enemy
                score += 1  # Increase score

            # Draw the enemy
            screen.blit(enemy_surface, (enemy['x'], enemy['y']))

        # Display the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

        # Display the remaining time
        remaining_time = max(0, game_duration - (pygame.time.get_ticks() - game_start_time)) // 1000
        time_text = font.render(f"Time: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (10, 10))

        # Spawn new enemies randomly
        # Adjust spawn probability based on elapsed time or score
        elapsed_time = pygame.time.get_ticks() - game_start_time
        difficulty_factor = min(1.0, elapsed_time / game_duration)  # Scales from 0 to 1 as time progresses
        spawn_probability = 0.01 + (0.02 * difficulty_factor)  # Base rate increases over time

        # Spawn new enemies based on dynamic probability
        if random.random() < spawn_probability:
            spawn_enemy()

        draw_projectiles()

        # Update the screen
        pygame.display.update()

        # Frame rate control
        clock.tick(60)

# Game over: display final score
screen.fill(BLACK)
font = pygame.font.SysFont(None, 48)
game_over_text = font.render("Game Over", True, WHITE)
score_text = font.render(f"Final Score: {score}", True, WHITE)

screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 10))

# game_over_screen()

pygame.display.update()
pygame.time.wait(3000)  # Wait for 3 seconds before quitting the game

# Quit pygame
pygame.quit()
sys.exit()