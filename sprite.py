import pygame

class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet and optimize it for Blitting."""
        try:
            # use convert_alpha() if your sheet has transparency
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def get_image(self, x, y, width, height):
        """Extract a single image from a specific coordinate point."""
        rect = pygame.Rect(x, y, width, height)
        # subsurface shares pixel data with the original sheet (high performance)
        image = self.sheet.subsurface(rect)
        return image

    def load_strip(self, x, y, width, height, frame_count):
        """Extract a horizontal row of frames as a list."""
        frames = []
        for i in range(frame_count):
            frame_x = x + (i * width)
            frames.append(self.get_image(frame_x, y, width, height))
        return frames






class AnimatedPlayer(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path):
        super().__init__()
        self.ss = SpriteSheet(sprite_sheet_path)
        
        # Load your animation states
        self.animations = {
            "idle": self.ss.load_strip(x=0, y=0, width=16, height=16, frame_count=4),
            "walk": self.ss.load_strip(x=0, y=16, width=16, height=16, frame_count=4),
            "falling": self.ss.load_strip(x=0, y=32, width=16, height=16, frame_count=2)
        }
        
        self.current_state = "idle"
        self.frame_index = 0.0
        self.animation_speed = 4.0 # Higher numbers mean faster animation
        self.flip_x = False
        
        # Required Pygame Sprite attributes
        self.base_image = self.animations[self.current_state][int(self.frame_index)]
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft=(100, 100))

        self.pos = pygame.Vector2(self.rect.topleft)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 100.0 # Pixels per second

    def change_state(self, new_state):
        """Safely switch to a new animation type."""
        if self.current_state != new_state:
            self.current_state = new_state
            self.frame_index = 0.0

    def update(self, dt=1.0):
        """Handle movement, positioning, and animation updates."""
        # 1. Update position based on velocity and delta time
        if self.velocity.length() > 0:
            # Normalize vector to prevent faster diagonal movement
            self.pos += self.velocity.normalize() * self.speed * dt
            self.change_state("walk")
        else:
            self.change_state("idle")

        # Bind the sprite's collision rect to the floating position
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # 2. Advance the animation frames
        current_frames = self.animations[self.current_state]
        
        # Increment index frame using delta time or animation speed
        self.frame_index += self.animation_speed * dt
        
        # Loop animation back to the start frame if it exceeds the maximum
        if self.frame_index >= len(current_frames):
            self.frame_index = 0.0
            
        # Get the standard, forward-facing frame
        self.base_image = current_frames[int(self.frame_index)]

        # 3. Apply structural flip on the fly
        # Arguments: (surface, flip_horizontal, flip_vertical)
        self.image = pygame.transform.flip(self.base_image, self.flip_x, False)
