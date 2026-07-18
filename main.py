import pygame
from tiles import Tile, LevelGen
from player import Player


# 1. Initialize all Pygame modules
pygame.init()



# 2. Set up the game window (Width, Height)
screen = pygame.display.set_mode((800, 400))
level = LevelGen("line.txt")
ratio = level.longest / len(level.lines)
width = 1200
height = width / ratio
canvas = pygame.Surface((level.longest*16, len(level.lines)*16))
screen = pygame.display.set_mode((width, height))


pygame.display.set_caption("Ultimater: Green Star North")

# 3. Create a clock tracking object to control frame rate
clock = pygame.time.Clock()

# creating and adding collision to the sprite group
walls = pygame.sprite.Group()
for t in level.tiles:
     walls.add(t)


all_sprites = pygame.sprite.Group()
player = Player((64, 48), walls=walls)
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
    canvas.fill((40, 44, 52))

    # drawing(surface, color, center_coordinates, radius)
    #pygame.draw.rect(canvas, (255, 0, 0), player.grounded) drawing the grounding element of player
    all_sprites.draw(canvas)

    # Refresh the visible display buffer to show changes
    modded_screen = pygame.transform.scale(canvas, (width, height))
    screen.blit(modded_screen, (0, 0))

    pygame.display.flip()
    

# Clean up and close the window safely when exiting the loop
pygame.quit()
