import pygame

class Player_Movement:
    def __init__(self):
        
        # Load all images for dino PNG
        self.images = {
            "idle":       pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)),
            "walk_right": pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)),
            "walk_left":  pygame.transform.flip(pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)), True, False),
            "duck":       pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 60)),
            "jump":       pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)),
        }
        
        self.game_state = "idle"    # Current game state
        self.rect = pygame.Rect(100, 300, 64, 64)
        self.speed_y = 0            # For gravity and jumping
        self.png_on_ground = True
        self.constant_ground = 400  
        self.standing_height = 120
        self.duck_height = 60
        

    def handle_key_input(self, keys, events):
        # Check key press for JUMP
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.png_on_ground:
                    self.speed_y = -15  # Launch upward
                    self.game_state = "jump"

        # Check which keys are pressed
        # Move the png accordingly 
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.game_state = "walk_left"   # A = Walk left

        elif keys[pygame.K_d]:
            self.rect.x += 5
            self.game_state = "walk_right"  # D = Walk right

        elif keys[pygame.K_s]:
            self.game_state = "duck"        # S = Duck
            self.rect.height = self.duck_height
            self.rect.y = self.constant_ground - self.duck_height  # Crouch at ground level

        elif self.png_on_ground and self.game_state != "jump":
            self.game_state = "idle"        # Nothing pressed, stay idle
            self.rect.height = self.standing_height # Restore when standing

    def gravity(self):
        # This functions purpose is used to simulate real gravity
        # This function is used whenever the player presses jump
        constant_gravity = 0.9

        self.speed_y += constant_gravity    # gravity pulls down 
        self.rect.y += self.speed_y         # apply vertical velocity

        if self.rect.y >= self.constant_ground:
            self.rect.y = self.constant_ground
            self.speed_y = 0
            self.png_on_ground = True
        else:
            self.png_on_ground = False

    def draw(self, screen):
        screen.blit(self.images[self.game_state], self.rect) 