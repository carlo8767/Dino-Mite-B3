import os.path

import pygame
import random

from dino_mite_utility.utilities_names import WIDTH, HEIGHT

class HorizontalHazard(pygame.sprite.Sprite):
    def __init__(self, image_path, speed = 2, size = (60,60)):
        super().__init__()
        self.position_x = -300
        self.position_y = 600
        self.screen_width = WIDTH
        self.is_active = True  # ADD THIS
        self.name = "HorizontalHazard"  # ADD THIS
        if image_path is not None:
            self.image_loaded = pygame.image.load(image_path).convert_alpha()
            self.image_loaded = pygame.transform.scale(self.image_loaded, size)
        else:
            self.image_loaded = pygame.Surface(size, pygame.SRCALPHA)
            self.image_loaded.fill((255, 255, 255))

        self.rect = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image_loaded)
        self.speed = speed

    def get_current_position(self):
        return self.rect.x, self.rect.y

    def reset(self):
        self.rect.x = self.position_x

    def update_position_collision(self):
        self.reset()

    def update_position(self):
        self.rect.x += self.speed
        if self.rect.left > self.screen_width:
           self.reset()
    def draw_horizontal_hazard(self, screen):
        screen.blit(self.image_loaded, self.rect)

class RollingRock(HorizontalHazard):
    def __init__(self):
        super().__init__(image_path=os.path.join("./image/hazard", "rolling_rock.png"), speed=2, size=(60, 60))
        self.name = "RollingRock"
