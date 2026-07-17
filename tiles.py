import pygame
from sprite import SpriteSheet

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y):
        super().__init__()
        ss = SpriteSheet("grassTiles.png")
        self.image = ss.get_image(tile[0], tile[1], 16, 16)

        self.rect = self.image.get_rect(topleft=(x, y))