import pygame

# 1. Initialize all Pygame modules
pygame.init()

# 2. Set up the game window (Width, Height)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame CE Game")

# 3. Create a clock tracking object to control frame rate
clock = pygame.time.Clock()

# Game state variable
running = True

# Main Game Loop
while running:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        # Check if the user clicked the window's close (X) button
        if event.type == pygame.QUIT:
            running = False

    # --- GAME LOGIC ---
    # (Update positions, check collisions, etc. go here)

    # --- DRAWING / RENDERING ---
    # Clear the screen with a background color (RGB format)
    screen.fill((40, 44, 52)) 

    # Draw a simple test circle: (surface, color, center_coordinates, radius)
    pygame.draw.circle(screen, (97, 218, 251), (400, 300), 50)

    # Refresh the visible display buffer to show changes
    pygame.display.flip()

    # Limit the game to 60 frames per second
    clock.tick(60)

# Clean up and close the window safely when exiting the loop
pygame.quit()
