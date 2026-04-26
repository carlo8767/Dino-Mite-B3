import os

import pygame

from dino_mite_model.level_model.base_level_model import BaseLevelModel
from dino_mite_model.character_game.vertical_hazard import Fireball, MammothLeg


class LevelTwo(BaseLevelModel):
    """
    Level 2 entity container: 3 fireballs (vertical) + 1 mammoth leg (vertical stomp).

    Fireballs replace meteors — faster with more horizontal drift.
    MammothLeg hangs from the top, shakes to warn the player, then slams.

    !Adjust! image_loaded once a Level 2 win-animation asset is ready.
    !Adjust! sound once a Level 2 music track is ready.
    """

    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story.txt"))

        # ── Hazards ───────────────────────────────────────────────────────────
        self.hazard_fireball    = Fireball()
        self.hazard_fireballOne = Fireball()
        self.hazard_fireballTwo = Fireball()
        self.hazard_mammothLeg  = MammothLeg()

        # ── Win-sequence animation (placeholder — replace when Level 2 asset is ready) ──
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(
                os.path.join('./image/level_one', 'wormhole.png')
            ).convert_alpha(),
            (450, 450)
        )
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (400, 300)

        # ── Assets ────────────────────────────────────────────────────────────
        self.image          = os.path.join('./image/level_two/', 'backgroundlevelTwo.jpeg')
        self.sound          = os.path.join('./music', 'SoundLevelOne.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelOne.mp3')
