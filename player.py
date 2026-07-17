import pygame
from sprite import AnimatedPlayer

class Player(pygame.sprite.Sprite):
    def __init__(self, position, walls):
        super().__init__()

        # 1. Setup appearance
        self.animPlayer = AnimatedPlayer("guySheet.png")
        self.image = self.animPlayer.image
        
        # 2. Setup physics boundaries and start position
        self.rect = self.image.get_rect(topleft=position)
        self.grounded = pygame.Rect(position[0], position[1]+16, 16, 2)
        
        
        
        # 3. Store the reference to the walls group for collision checks
        self.walls = walls
        
        # 4. Movement variables
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 0.2
        self.speed = 3
        self.is_grounded = False
        self.can_jump = True
        self.is_jumping = False

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
        

        """
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed
        else:
            self.velocity.y = 0
        """
    def jump(self):
        self.is_jumping = True
        self.velocity.y = -3
        self.can_jump = False

    def update(self, dt):
        """Updates position and resolves collisions frame-by-frame."""
        # Get latest movement intentions
        self.get_input()
        
        # setting is_grounded based on if the grounded rect hits any wall
        hit = False
        for wall in self.walls:
            if self.grounded.colliderect(wall):
                hit = True
                self.can_jump = True
            
        if hit:
            self.is_grounded = True
        else:
            self.is_grounded = False
        
        # jumping ends when velocity.y goes positive and character starts falling
        if self.velocity.y > 0:
            self.is_jumping = False

        # gravity and reseting velocity y on land
        if self.is_grounded == True and self.is_jumping == False:
            self.velocity.y = 0
        else:
            self.velocity.y += self.gravity
            self.can_jump = False

        # moving the grounding rect with the character
        self.grounded.x += self.velocity.x
        self.grounded.y += self.velocity.y

        # handle horizontal movement and collisions
        self.rect.x += self.velocity.x
        for wall in pygame.sprite.spritecollide(self, self.walls, False):
            if self.velocity.x > 0:    # Moving right, hit left side of wall
                self.rect.right = wall.rect.left
                self.grounded.right = wall.rect.left
            elif self.velocity.x < 0:  # Moving left, hit right side of wall
                self.rect.left = wall.rect.right
                self.grounded.left = wall.rect.right
        
        # handle vertical movement and collisions
        self.rect.y += self.velocity.y
        for wall in pygame.sprite.spritecollide(self, self.walls, False):
            if self.velocity.y > 0:    # Moving down, hit top of wall
                self.rect.bottom = wall.rect.top
                self.grounded.bottom = wall.rect.top + 2
                
            elif self.velocity.y < 0:  # Moving up, hit bottom of wall
                self.rect.top = wall.rect.bottom
                self.grounded.top = wall.rect.bottom + 16
        
        
        # updating the frame of the animation
        self.animPlayer.update(self.velocity, dt)
        self.image = self.animPlayer.image