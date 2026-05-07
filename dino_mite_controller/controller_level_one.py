import pygame

from dino_mite_controller.base_level_controller import BaseLevelController
from dino_mite_model.level_model.levelone import LevelOne

import random

class ControllerLevelOne(BaseLevelController):
    """
    Controller for Level 1.

    Level 1 hazards: 3 meteors + 1 rolling rock.
    All game logic lives in BaseLevelController - only the hazard list is level-specific.
    """

    def __init__(self):
        self.level_model = LevelOne()
        self.level_number = 1
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_meteor,
            self.level_model.hazard_meteorOne,
            self.level_model.hazard_meteorTwo,
            self.level_model.hazard_rollingRock,
        ]

    def _build_deck(self) -> list:
        """One deck = 5 cards: 3 shields, 1 time reduction, 1 slow.
        Shuffled so the order is unpredictable but the 60/20/20 ratio is exact."""
        deck = (
                [self.level_model.pw_up_shield_bubble] * 3 +
                [self.level_model.pw_up_time_reduction] * 1 +
                [self.level_model.pw_up_slower_hazard] * 1
        )
        random.shuffle(deck)
        return deck


    def init_music(self):
        pygame.mixer.music.load(self.level_model.sound)
        pygame.mixer.music.set_volume(self.level_model.sound_volume)
        pygame.mixer.music.play(-1, 0.0)

    def init_music_end_level(self):
        pygame.mixer.music.load(self.level_model.sound_end_game)
        pygame.mixer.music.play(-1, 0.0)


