import os

from dino_mite_model.character_game.Character import CharacterDino
from dino_mite_model.character_game.Hazard import Meteor


class LevelOne:


    def __init__(self):
        self.width = 0
        self.height = 0
        self.hazard_level_one = Meteor()
        self.character = CharacterDino()
        self.image = os.path.join('./image', 'backgroundLevelOne.jpeg')

