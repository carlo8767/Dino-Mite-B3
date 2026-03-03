import os.path

import pygame
import random


class Meteor():
    """The meteor spawns with the random X position at the very top of the screen and falls down\n"
    "vertically with the set speed"""

    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 768

        self.position_x = random.randint(50, self.screen_width - 50)
        self.position_y = -60

        self.speed = 4

        self.is_active = True

        self.image_path = os.path.join("./image", "meteor.jpg")

        self.image_loaded = pygame.image.load(self.image_path).convert_alpha()
        self.image_loaded = pygame.transform.scale(self.image_loaded, (60, 60))

        self.rectangle = self.image_loaded.get_rect()
        self.rectangle.center = (self.position_x, self.position_y)

    """ Moves the meteor from top os the screen to the bottom"""

    def update_positions(self):
        self.rectangle.y += self.speed

        if self.rectangle.top > self.screen_height:
            self.kill()

    def kill(self):
        self.is_active = False  # pass flag to the controller for removing and object
