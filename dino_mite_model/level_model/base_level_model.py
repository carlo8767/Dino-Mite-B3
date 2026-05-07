import os

import pygame.sprite

from dino_mite_model.character_game.Character import CharacterDino
from dino_mite_model.character_game.CharacterTwo import CharacterDinoTwo
from dino_mite_model.character_game.power_ups import ShieldBubble, TimeReduction, SlowerHazards
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class BaseLevelModel(pygame.sprite.Sprite):
    """
    Shared state for all level models.

    Every level has the same character, the same three powerup types, and the
    same level-complete music. Subclasses add their own hazards, background,
    and level-specific sounds.

    Subclass usage:
        class LevelTwo(BaseLevelModel):
            def __init__(self):
                super().__init__(os.path.join("./text_files", "end_story_level_two.txt"))
                self.hazard_meteor = Meteor()
                ...
    """

    def __init__(self, text_file_path: str):
        super().__init__()
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.character = CharacterDino()
        self.characterTwo = CharacterDinoTwo()

        # One instance per powerup type — reused across the level, never re-created mid-game
        self.pw_up_shield_bubble = ShieldBubble()
        self.pw_up_time_reduction = TimeReduction()
        self.pw_up_slower_hazard = SlowerHazards()

        self.sound_volume = 0.35
        self.sound_complete_level = os.path.join('./music', 'End_First_Level.mp3')
        self.store_text_end = self._load_text(text_file_path)

    def _load_text(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "file is missing"
