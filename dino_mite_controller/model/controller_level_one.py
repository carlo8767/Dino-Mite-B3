from dino_mite_model.character_game.Hazard import Meteor
from dino_mite_model.level_model.levelone import LevelOne

import pygame


class ControllerLevelOne:

    def __init__(self):
        # ADD MODEL  VERIFY IF HERE
        self.level_one = LevelOne()
        self.hazards = []

    def update_level_one(self):
        for hazard in self.hazards:
            hazard.update_position()
        self.hazards = [hazard for hazard in self.hazards if hazard.is_active]

    def spawn_meteor(self):
        self.hazards.append(Meteor())

    def start_level_one (self):
        return self.level_one

    def detection_collision_character(self, sprite, group) -> bool:
        sprites_group = pygame.sprite.Group()
        sprites_group.add(group)
        if pygame.sprite.spritecollide(sprite, sprites_group, True):
            print("collude")
            return True
        return False
        """"
        https://www.pygame.org/docs/tut/SpriteIntro.html
        """


    def update_collision_position(self):
       self.level_one.hazard_level_one.update_position_collision()

    def screen_collision(self, x ,y):
        if int(y) > 800:
            print("Ok")
        return self.level_one.verification_limit_screen_colision(x,y)





