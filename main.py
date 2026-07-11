import pygame
from sprite import AnimatedPlayer
from collisions import collisions

# 1. Initialize all Pygame modules
pygame.init()

# 2. Set up the game window (Width, Height)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ultimater: Green Star North")

# 3. Create a clock tracking object to control frame rate
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = AnimatedPlayer("guySheet.png")
all_sprites.add(player)

obstacles = [
    pygame.FRect(100, 200, 200, 50),
    pygame.FRect(500, 250, 50, 200)
]

# Game state variable
running = True

# Main Game Loop
while running:

    # Limit the game to 60 frames per second
    # dt holds milliseconds passed since the last frame
    dt = clock.tick(60) / 1000.0

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        # Check if the user clicked the window's close (X) button
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if player.is_falling == False:
                if event.key == pygame.K_SPACE:
                    pass
                    
    
    # Reset movement vector every frame
    player.velocity.x = 0
    if player.is_falling == True:
        player.velocity.y = 1
    elif player.is_falling == False:
        player.velocity.y = 0


    # continous action
    keys = pygame.key.get_pressed()
    # character movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity.x = -1
        player.flip_x = True # To face left
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity.x = 1
        player.flip_x = False

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.velocity.y = -1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if player.is_falling == False:
            player.is_falling = True


    # --- GAME LOGIC ---
    # (Update positions, check collisions, etc. go here)
    collisions(player, player.velocity.x, player.velocity.y, obstacles)


    all_sprites.update(dt)

    # --- DRAWING / RENDERING ---
    # Clear the screen with a background color (RGB format)
    screen.fill((40, 44, 52))

    # Draw a simple test circle: (surface, color, center_coordinates, radius)
    for wall in obstacles:
        pygame.draw.rect(screen, (200, 50, 50), wall)
    all_sprites.draw(screen)

    # Refresh the visible display buffer to show changes
    pygame.display.flip()

    

# Clean up and close the window safely when exiting the loop
pygame.quit()
