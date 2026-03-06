import os

import pygame.sprite


from dino_mite_model.character_game.Character import CharacterDino
from dino_mite_model.character_game.Hazard import Meteor

from dino_mite_utility.utilities_names import WIDTH, HEIGHT

class LevelOne(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.hazard_level_one = Meteor()
        self.character = CharacterDino()
        self.image = os.path.join('./image', 'backgroundLevelOne.jpeg')




    def verification_limit_screen_colision(self, x, y):
        if x > WIDTH or  y > HEIGHT:
            return True
        return False