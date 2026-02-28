import os.path

import pygame
import random


class Meteor():


    def __init__(self):
        self.position_x = 400
        self.position_y = 2
        self.speed = 3
        self.image_meteor = os.path.join("./image", "meteor.jpeg")
        self.image_loaded = pygame.image.load(self.image_meteor).convert()
        self.rectangle = self.image_loaded.get_rect()
        self.rectangle.center = (self.position_x, self.position_y)


    def update_positions(self, x, y):
        self.position = (x, y)

    """
        # CHANGE WITH REALISTIC VALUES
        def _init_(self, screen_width):
        super()._init_()
        self.image = pygame.Surface((10, 10))  # replace with avatar later
        self.image.fill((0, 0, 0))

        x = random.randint(50, screen_width - 50)
        self.rect = self.image.get_rect(topleft=(x, 0))

        self.speed = 3 #can be also randomised. Will be adjusted later on
        def move(self):
            self.rect.y += self.speed
    """
