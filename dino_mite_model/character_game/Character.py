import os
import random

import pygame.sprite

from dino_mite_utility.utilities_names import WIDTH, HEIGHT
from dino_mite_model.character_game.player_movement import Player_Movement


class CharacterDino(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.move_x = 2
        self.move_y = 2
        self.position_x = 100
        self.position_y = 700
        self.image_dino_path = os.path.join("./image","character.png")
        self.image_loaded = pygame.image.load(self.image_dino_path).convert()
        self.image_loaded = pygame.transform.scale(
            self.image_loaded,
            (60, 60)
        )
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.name = "Dino"
        self.player_movement = Player_Movement()

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

