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
        self.image_loop_end_level = os.path.join('./image/level_one', 'wormhole.png')
        self.image_loaded = pygame.image.load(self.image_loop_end_level).convert_alpha()
        self.image_loaded = pygame.transform.scale(self.image_loaded, (450, 450))
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (400, 300)
        self.image = os.path.join('./image/level_one/', 'backgroundLevelOne.jpeg')
        self.sound = os.path.join('./music',  'SoundLevelOne.mp3')
        self.sound_end_game =  os.path.join('./music', 'EndGameLevelOne.mp3')
        self.sound = os.path.join('./music', 'SoundLevelOne.mp3')
        self.sound_complete_level = os.path.join('./music', 'End_First_Level.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelOne.mp3')
        self.store_text_end = self.upload_file()



    def upload_file(self):
        try:
            content = ""
            os_path = os.path.join("./text_files", "end_story.txt")
            with open(os_path, 'r', encoding='utf-8') as f:
                content += f.read()
        except FileNotFoundError:
            content = "file is missing"
        return content


