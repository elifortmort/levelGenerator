import pygame
from tiles import Tile
from player import Player

# 1. Initialize all Pygame modules
pygame.init()

# 2. Set up the game window (Width, Height)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ultimater: Green Star North")

# 3. Create a clock tracking object to control frame rate
clock = pygame.time.Clock()

walls = pygame.sprite.Group()

wall_layouts = [
    ((0, 0), 100, 200),
    ((16, 0), 116, 200),
    ((32, 0), 132, 200)
]

for tile, x, y in wall_layouts:
    wall_element = Tile(tile, x, y)
    walls.add(wall_element)

all_sprites = pygame.sprite.Group()
player = Player((100, 100), walls=walls)
all_sprites.add(walls)
all_sprites.add(player)

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
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.can_jump == True:
                    player.jump()
            


    # continous action
    #keys = pygame.key.get_pressed()
    


    # --- GAME LOGIC ---
    # (Update positions, check collisions, etc. go here)
    all_sprites.update(dt)



    # --- DRAWING / RENDERING ---
    # Clear the screen with a background color (RGB format)
    screen.fill((40, 44, 52))

    # drawing(surface, color, center_coordinates, radius)
    
    all_sprites.draw(screen)

    # Refresh the visible display buffer to show changes
    pygame.display.flip()
    

# Clean up and close the window safely when exiting the loop
pygame.quit()
