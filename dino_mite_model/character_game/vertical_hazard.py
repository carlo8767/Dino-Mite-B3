import os.path

import pygame
import random

from dino_mite_utility.utilities_names import WIDTH, HEIGHT


# Base class of vertical hazards
class VerticalHazard(pygame.sprite.Sprite):
    def __init__(self, image_path, speed = 6, size = (120,120)):
        super().__init__()

        if image_path is not None:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
        else:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill((255, 255, 255))

        self.position_x = random.randint(550, WIDTH - 50)
        self.position_y = -60
        self.rect = self.image.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.speed = speed
        self.is_active = True
        self.name = "VerticalHazard"

    def update_position(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset()
    def get_current_position(self):
        return self.rect.x, self.rect.y

    def update_position_collision(self):
        self.reset()

    def reset(self):
        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60
        self.rect.center = (self.position_x, self.position_y)
        self.is_active = True

    def draw_vertical_hazard(self, screen):
        screen.blit(self.image, self.rect)


class Meteor(VerticalHazard):
    """Level1 hazard. The meteor spawns with the random X position at the very top of the screen and falls down\n"
       "vertically with the set speed"""

    def __init__(self):
        super().__init__(image_path = os.path.join("./image/hazard", "meteor.png"), speed= 6, size = (120, 120))
        self.name = "Meteor"
        self.sound_meteor = os.path.join("./music", "MeteorSound.mp3")

    def update_position(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-2, 2)
        if self.rect.top > HEIGHT:
            self.reset()

class Fireball(VerticalHazard):

    # Adjust: image, sound
    def __init__(self):
        super().__init__(image_path=os.path.join("./image/hazards", "meteor.png"), speed=8, size=(120, 120))
        self.name = "Fireball"
        # !Adjust! self.sound_meteor = os.path.join("./music", "Fireball.mp3")

    def update_position(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-3, 3) #more shaking
        if self.rect.top > HEIGHT:
            self.reset()
