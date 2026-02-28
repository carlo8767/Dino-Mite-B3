import os

import pygame.sprite


class CharacterDino:

    def __init__(self):
        self.move_x = 3
        self.move_y = 3
        self.position_x = 0
        self.position_y = 700
        self.image_dino_path = os.path.join("./image","character.png")
        self.image_loaded = pygame.image.load(self.image_dino_path).convert()
        self.image_loaded = pygame.transform.scale(
            self.image_loaded,
            (60, 60)
        )
        self.rectangle = self.image_loaded.get_rect()
        self.rectangle.center = (self.position_x, self.position_y)

    def movement_character(self, move_x):
        self.move_x = move_x
        self.move_y = self.move_y

    def set_position_rectangle(self, position_x, position_y):
        self.rectangle.center = (position_x, position_y)

