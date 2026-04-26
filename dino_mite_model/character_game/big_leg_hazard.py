import os.path

import pygame
import random

from dino_mite_utility.utilities_names import WIDTH, HEIGHT
""" BigLegHazard is operating in the following way:
 - Leg apperas on top of the screen hanging for a few seconds above the place it will stap on
 - Leg rapidly steps on the ground and go back up """
class BigLegHazard (pygame.sprite.Sprite):

    def __int__(self):
        super().__init__()
        self.constant_ground = 510
        self.name = "BigLegHazard"
        self.size = (80, 200)
        self.is_active = True

        self.image_path = os.path.join("./image/hazard", "big_leg_hazard_placeholder.png") #Edit image
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center_x = random.randint(-100, WIDTH - 100)
        self.rect.bottom = self.constant_ground - 80
        self.start_time = pygame.time.get_ticks()
        self.is_active = True

    def update_position(self):
        time_passed = pygame.time.get_ticks() - self.start_time

        if time_passed < 2500:
            self.rect.x += random.randint(-3,3) # if hold time - keep a leg on top and shake a little for movement effect

        elif 2500 < time_passed < 1580: # step time - move leg down until the ground level
            self.rect.bottom += 40
            if self.rect.bottom > self.constant_ground:
                self.rect.bottom = self.constant_ground

        elif time_passed < 2830: # retrive the leg
            self.rect.bottom -=30

        else:
            self.reset()
    def get_current_position(self):
        return self.rect.x, self.rect.y
    def update_position_collission(self):
        self.reset()

    def draw_vertical_hazard(self, screen):
        screen.blit(self.image, self.rect)


