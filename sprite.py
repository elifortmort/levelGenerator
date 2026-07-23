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



class AnimatedFlag(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path):
        super().__init__()
        self.ss = SpriteSheet(sprite_sheet_path)
        self.off = SpriteSheet("flagOff.png")
        
        self.animations = {
            "off": self.off.load_strip(0, 0, 14, 15, 1),
            "on": self.ss.load_strip(x=0, y=0, width=14, height=15, frame_count=4),
        }
        
        self.current_state = "off"
        self.frame_index = 0.0
        self.animation_speed = 4.0 # Higher numbers mean faster animation

        self.fin = False
        
        # Required Pygame Sprite attributes
        self.base_image = self.animations[self.current_state][int(self.frame_index)]
        self.image = self.base_image

    def change_state(self, new_state):
            """Safely switch to a new animation type."""
            if self.current_state != new_state:
                self.current_state = new_state
                self.frame_index = 0.0

    def update(self, dt=1.0):
        """animation updates."""

        if self.fin == True:
            self.change_state("on")
        else:
            self.change_state("off")

        # 2. Advance the animation frames
        current_frames = self.animations[self.current_state]
        
        # Increment index frame using delta time or animation speed
        self.frame_index += self.animation_speed * dt
        
        # Loop animation back to the start frame if it exceeds the maximum
        if self.frame_index >= len(current_frames):
            self.frame_index = 0.0
            
        # Get the standard, forward-facing frame
        self.base_image = current_frames[int(self.frame_index)]
        self.image = self.base_image



class AnimatedCoin(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path):
        super().__init__()
        self.ss = SpriteSheet(sprite_sheet_path)
        
        
        self.current_state = self.ss.load_strip(x=0, y=0, width=10, height=16, frame_count=4)
        self.frame_index = 0.0
        self.animation_speed = 4.0 # Higher numbers mean faster animation
        
        # Required Pygame Sprite attributes
        self.image = self.current_state[int(self.frame_index)]

    def update(self, dt=1.0):
        """animation updates."""

        # 2. Advance the animation frames
        current_frames = self.current_state
        
        # Increment index frame using delta time or animation speed
        self.frame_index += self.animation_speed * dt
        
        # Loop animation back to the start frame if it exceeds the maximum
        if self.frame_index >= len(current_frames):
            self.frame_index = 0.0
            
        # Get the standard, forward-facing frame
        self.image = current_frames[int(self.frame_index)]



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

    def change_state(self, new_state):
        """Safely switch to a new animation type."""
        if self.current_state != new_state:
            self.current_state = new_state
            self.frame_index = 0.0

    def update(self, velocity, dt=1.0):
        """animation updates."""
        # 1. Update position based on velocity and delta time
        if velocity.length() > 0:
            if velocity.x > 0:
                self.flip_x = False
            elif velocity.x < 0:
                self.flip_x = True
            if velocity.y > 0:
                self.change_state("falling")
            elif velocity.y < 0:
                self.change_state("falling")
            elif velocity.x > 0:
                self.change_state("walk")
            elif velocity.x < 0:
                self.change_state("walk")
        else:
            self.change_state("idle")

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
