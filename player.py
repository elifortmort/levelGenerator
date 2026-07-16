import pygame
from sprite import AnimatedPlayer

class Player(pygame.sprite.Sprite):
    def __init__(self, position, walls):
        super().__init__()

        # 1. Setup appearance (32x32 pixel red square)
        self.animPlayer = AnimatedPlayer("guySheet.png")
        self.image = self.animPlayer.image#pygame.Surface((32, 32))
        #self.image.fill((255, 0, 0))
        
        # 2. Setup physics boundaries and start position
        self.rect = self.image.get_rect(topleft=position)
        
        # 3. Store the reference to the walls group for collision checks
        self.walls = walls
        
        # 4. Movement variables
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 3

    def get_input(self):
        """Reads keyboard input to set player direction and speed."""
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
            
        # Vertical movement (assuming a top-down game layout)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed
        else:
            self.velocity.y = 0

    def update(self, dt):
        """Updates position and resolves collisions frame-by-frame."""
        # Get latest movement intentions
        self.get_input()

        # STEP A: Handle Horizontal Movement & Collisions
        self.rect.x += self.velocity.x
        for wall in pygame.sprite.spritecollide(self, self.walls, False):
            if self.velocity.x > 0:    # Moving right, hit left side of wall
                self.rect.right = wall.rect.left
            elif self.velocity.x < 0:  # Moving left, hit right side of wall
                self.rect.left = wall.rect.right

        # STEP B: Handle Vertical Movement & Collisions
        self.rect.y += self.velocity.y
        for wall in pygame.sprite.spritecollide(self, self.walls, False):
            if self.velocity.y > 0:    # Moving down, hit top of wall
                self.rect.bottom = wall.rect.top
            elif self.velocity.y < 0:  # Moving up, hit bottom of wall
                self.rect.top = wall.rect.bottom
        
        self.animPlayer.update(self.velocity, dt)
        self.image = self.animPlayer.image