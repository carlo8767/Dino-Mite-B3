import os

import pygame.sprite

from dino_mite_model.character_game.Character import CharacterDino
from dino_mite_model.character_game.Hazard import Meteor, RollingRock

from dino_mite_utility.utilities_names import WIDTH, HEIGHT

class LevelOne(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.hazard_meteor = Meteor()
        self.hazard_meteorOne = Meteor()
        self.hazard_meteorTwo = Meteor()
        self.hazard_rollingRock = RollingRock()
        self.character = CharacterDino()
        self.image = os.path.join('./image', 'backgroundLevelOne.jpeg')



    def verification_limit_screen_colision(self, x, y, verse="N"):
        if verse == "L":
            if x < 0  or y > HEIGHT:
                return True
        # THINK HOW TO FIX CARLO
        elif verse == "R":
            if x > (WIDTH-60) or y > HEIGHT:
                return True
        elif verse == "N":
            if  y > HEIGHT:
                return True
        return False





