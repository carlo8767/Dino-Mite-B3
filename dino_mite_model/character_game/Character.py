import pygame
from sklearn.datasets import load_sample_images

import os
import random

from dino_mite_utility.utilities_names import HEIGHT, WIDTH


class CharacterDino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load all images for dino PNG
        # self.images = self.load_images_movements()
        self.images = {
            "idle": pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)),
            "walk_right": pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(),
                                                 (120, 120)),
            "walk_left": pygame.transform.flip(
                pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)), True,
                False),
            "duck": pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 60)),
            "jump": pygame.transform.scale(pygame.image.load("./image/character.png").convert_alpha(), (120, 120)),
        }
        self.position_x = 200
        self.position_y = 510

        self.game_state = "idle"    # Current game state
        self.rect = self.images[self.game_state].get_rect()
        self.rect.center = (self.position_x, self.position_y)
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
            if self.rect.left < 0:
                self.rect.x  -=-5
                print("overcome limit left")

        elif keys[pygame.K_d]:
            self.rect.x += 5
            self.game_state = "walk_right"  # D = Walk right
            if self.rect.right > self.screen_width:
                self.rect.x -= 5
                print("overcome limit right")

        elif keys[pygame.K_s]:
            self.game_state = "duck"        # S = Duck
            self.rect.height = self.duck_height
            self.rect.y = self.position_y - self.duck_height  # Crouch at ground level

        elif self.png_on_ground and self.game_state != "jump":
            self.game_state = "idle"        # Nothing pressed, stay idle
            self.rect.height = self.standing_height # Restore when standing

    def gravity(self):
        # This functions purpose is used to simulate real gravity
        # This function is used whenever the player presses jump
        constant_gravity = 0.9

        self.speed_y += constant_gravity    # gravity pulls down
        self.rect.y += self.speed_y         # apply vertical velocity

        if self.rect.y >= self.position_y:
            self.rect.y = self.position_y
            self.speed_y = 0
            self.png_on_ground = True
        else:
            self.png_on_ground = False

    def draw(self, screen):
        screen.blit(self.images[self.game_state], self.rect)


    def movement_character_left(self):
        self.rect.x -=self.move_x

    def movement_character_right(self):
        self.rect.x += self.move_x

    def set_position_rectangle(self, position_x, position_y):
        self.rect.center = (position_x, position_y)

    def get_current_position(self):
        return self.rect.x, self.rect.y

    def set_current_position(self, x,y):
        self.rect.x = x
        self.rect.y = y


    def update_position_collision(self):
        self.rect.y = 700
        self.rect.x = random.randint(50, self.screen_width - 50)
        if self.rect.left > self.screen_width:
            print("OVERCOME LIMIT")

