import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Create the visual surface for the wall
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Gray color
        
        # Position the wall using its rect
        self.rect = self.image.get_rect(topleft=(x, y))