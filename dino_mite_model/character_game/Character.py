import logging

import pygame
import random

from dino_mite_utility.utilities_names import HEIGHT, WIDTH


class CharacterDino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load all images for dino PNG
        self.images = {
            "idle":       pygame.transform.scale(pygame.image.load("./image/character/idle.png").convert_alpha(), (120, 120)),
            "walk_right": pygame.transform.scale(pygame.image.load("./image/character/running.png").convert_alpha(), (120, 120)),
            "walk_left":  pygame.transform.flip(pygame.transform.scale(pygame.image.load("./image/character/running.png").convert_alpha(), (120, 120)), True, False),
            "duck":       pygame.transform.scale(pygame.image.load("./image/character/crouch.png").convert_alpha(), (120, 60)),
            "jump":       pygame.transform.scale(pygame.image.load("./image/character/jump.png").convert_alpha(), (120, 120)),
            "dead":       pygame.transform.scale(pygame.image.load("./image/character/dead.png").convert_alpha(), (120, 120)),
            "happy": pygame.transform.scale(pygame.image.load("./image/character/levelpass.png").convert_alpha(),
                                            (150, 150)),
        }
        self.position_x = 370
        self.constant_ground = 510

        self.game_state = "idle"    # Current game state
        self.rect = self.images[self.game_state].get_rect()
        self.rect.center = (self.position_x, self.constant_ground)
        self.mask = pygame.mask.from_surface(self.images[self.game_state])
        self.speed_y = 0            # For gravity and jumping
        self.png_on_ground = True
        self.standing_height = 120
        self.duck_height = 60

        self.name = "Dino"
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.move_x = 2
        self.move_y = 2

    def handle_key_input(self, keys, events):
        # Check key press for JUMP and DUCK - one time press actions
        for event in events:
            if event.type == pygame.KEYDOWN:
                # W = Jump
                if event.key == pygame.K_w and self.png_on_ground:
                    self.speed_y = -15  # Launch upward
                    self.game_state = "jump"

                # S = Duck - uses KEYDOWN instead of every frame
                if event.key == pygame.K_s and self.png_on_ground:
                    self.game_state = "duck"
                    self.rect.height = self.duck_height
                    # shift rect.y down by the difference so character
                    # crouches at ground level instead of floating
                    self.rect.y = self.constant_ground + (self.standing_height - self.duck_height)

            # S released = stand back up - restores height and position on key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s and self.game_state == "duck":
                    self.game_state = "idle"
                    self.rect.height = self.standing_height
                    # restore y position back to ground level when standing
                    self.rect.y = self.constant_ground

        # Check which keys are pressed for movement
        if keys[pygame.K_a]:
            self.rect.x -= 5
            # stop character walking off left edge of screen
            if self.rect.left < 0:
                self.rect.x += 5
            if self.game_state not in ("jump", "duck"):
                self.game_state = "walk_left"   # A = Walk left

        elif keys[pygame.K_d]:
            self.rect.x += 5
            # stop character walking off right edge of screen
            if self.rect.right > self.screen_width:
                self.rect.x -= 5
            if self.game_state not in ("jump", "duck"):
                self.game_state = "walk_right"  # D = Walk right

        elif self.png_on_ground and self.game_state not in ("duck", "jump"):
            self.game_state = "idle"            # Nothing pressed, stay idle

    def gravity(self):
        # This function simulates real gravity
        # This function is used whenever the player presses jump

        # skip gravity entirely while ducking
        if self.game_state == "duck":
            return

        constant_gravity = 0.9

        self.speed_y += constant_gravity    # Gravity pulls down png every frame
        self.rect.y += self.speed_y         # Apply vertical velocity

        if self.rect.y >= self.constant_ground:
            self.rect.y = self.constant_ground
            self.speed_y = 0
            self.png_on_ground = True
            # reset to idle when landing from jump
            if self.game_state == "jump":
                self.game_state = "idle"
        else:
            self.png_on_ground = False

    def draw(self, screen):
        screen.blit(self.images[self.game_state], self.rect)

    def movement_character_left(self):
        self.rect.x -= self.move_x

    def movement_character_right(self):
        self.rect.x += self.move_x

    def set_position_rectangle(self, position_x, position_y):
        self.rect.center = (position_x, position_y)

    def get_current_position(self):
        return self.rect.x, self.rect.y

    def set_current_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_position_collision(self):
        self.rect.y = self.constant_ground
        self.rect.x = random.randint(50, self.screen_width - 50)

    def draw_status(self, screen, state):
        # DRAW BASE ON THE STATE
        self.game_state = state
        screen.blit(self.images[self.game_state], self.rect)