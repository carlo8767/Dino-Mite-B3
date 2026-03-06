import os.path

import pygame
import random

from dino_mite_utility.utilities_names import WIDTH, HEIGHT
class Meteor(pygame.sprite.Sprite):
    """The meteor spawns with the random X position at the very top of the screen and falls down\n"
    "vertically with the set speed"""

    def __init__(self):
        super().__init__()
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.position_x = random.randint(50, self.screen_width - 50)
        self.position_y = -60
        self.speed = 4
        self.is_active = True
        self.image_path = os.path.join("./image", "meteor.jpg")
        self.image_loaded = pygame.image.load(self.image_path).convert_alpha()
        self.image_loaded = pygame.transform.scale(self.image_loaded, (60, 60))
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.name = "Hazard"

    """ Moves the meteor from top os the screen to the bottom"""
    def update_positions(self, meteor):
        meteor.rect.y += meteor.speed

        if meteor.rect.top > meteor.screen_height:
            meteor.kill()

    def update_position_collision(self):
        self.rect.y = -60
        self.rect.x = random.randint(50, self.screen_width - 50)

    def get_current_position(self):
        return self.rect.x, self.rect.y

    def kill(self,):
        self.is_active = False  # pass flag to the controller for removing and object
