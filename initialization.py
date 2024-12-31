# Step 1: Import the required module
import pygame

# Step 2: Initialize Pygame's core modules
pygame.init()  # Returns a tuple of (successful_initializations, failed_initializations)

"""
Think of pygame.init() like turning on all systems in a spaceship.
It prepares all components (display, sound, input devices) for use.
"""

# Step 3: Define our constants (like mathematical constants π or e)
WIDTH = 800    # Window width in pixels
HEIGHT = 600   # Window height in pixels

# Step 4: Create our display surface (like defining our coordinate plane)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
"""
The display surface is our 'canvas' where we'll draw.
The coordinate system starts at (0,0) in the top-left corner:
- x increases rightward
- y increases downward
"""

# Step 5: Set window title (optional but good practice)
pygame.display.set_caption("Pygame Tutorial")

# Step 6: Define colors using RGB tuples (like defining points in 3D space)
BLACK = (0, 0, 0)       # Absence of all colors
WHITE = (255, 255, 255) # Maximum of all colors
RED = (255, 0, 0)      # Only red component
GREEN = (0, 255, 0)    # Only green component
BLUE = (0, 0, 255)     # Only blue component

# Step 7: Initialize the clock (for controlling our time variable)
clock = pygame.time.Clock()
"""
The clock is like our time-keeper, ensuring our game runs at a consistent speed,
similar to how we might control the speed of a moving object in physics.
"""

# Step 8: Basic game loop to test our initialization
running = True
while running:
    # Event handling (like checking for input in a function)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen (like erasing our chalkboard)
    screen.fill(BLACK)
    
    # Draw a simple shape to test our display
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 50)
    
    # Update the display (like showing our work)
    pygame.display.flip()
    
    # Control frame rate (like controlling Δt in calculus)
    clock.tick(60)  # 60 frames per second

# Step 9: Cleanup when done (like cleaning up after an experiment)
pygame.quit()