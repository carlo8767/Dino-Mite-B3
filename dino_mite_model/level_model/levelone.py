import os

import pygame

from dino_mite_model.level_model.base_level_model import BaseLevelModel
from dino_mite_model.character_game.vertical_hazard import Meteor
from dino_mite_model.character_game.horizontal_hazard import RollingRock


class LevelOne(BaseLevelModel):
    """Level 1 entity container: 3 meteors + 1 rolling rock."""

    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story.txt"))

        self.hazard_meteor    = Meteor()
        self.hazard_meteorOne = Meteor()
        self.hazard_meteorTwo = Meteor()
        self.hazard_rollingRock = RollingRock()

        # Win-sequence animation image (wormhole portal)
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(
                os.path.join('./image/level_one', 'wormhole.png')
            ).convert_alpha(),
            (450, 450)
        )
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (400, 300)

        self.image         = os.path.join('./image/level_one/', 'backgroundLevelOne.jpeg')
        self.sound         = os.path.join('./music', 'SoundLevelOne.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelOne.mp3')
