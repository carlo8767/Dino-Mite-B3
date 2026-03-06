import pygame.sprite

from dino_mite_model.level_model.levelone import LevelOne


class ControllerLevelOne:

    def __init__(self):
        # ADD MODEL  VERIFY IF HERE
        self.level_one = LevelOne()

    def start_level_one(self):
        return self.level_one

    def detection_collision_character(self, sprite, group) -> bool:
        sprites_group = pygame.sprite.Group()
        sprites_group.add(group)
        if pygame.sprite.spritecollide(sprite, sprites_group, True):
            print("collude")
            return True
        return  False

        """"
        https://www.pygame.org/docs/tut/SpriteIntro.html
        
        
        """
