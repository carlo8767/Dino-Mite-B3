import os

import pygame.sprite

from dino_mite_model.character_game.Character import CharacterDino
from dino_mite_model.character_game.Hazard import Meteor, RollingRock
from dino_mite_model.character_game.power_ups import ShieldBubble, TimeReduction, SlowerHazards

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
        self.pw_up_shield_bubble = ShieldBubble()
        self.pw_up_time_reduction = TimeReduction()
        self.pw_up_slower_hazard = SlowerHazards()
        self.character = CharacterDino()
        self.image = os.path.join('./image/level_one/', 'backgroundLevelOne.jpeg')
        self.sound = os.path.join('./music',  'SoundLevelOne.mp3')
        self.sound_end_game =  os.path.join('./music', 'EndGameLevelOne.mp3')




