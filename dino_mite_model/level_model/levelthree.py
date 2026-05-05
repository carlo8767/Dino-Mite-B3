import os

import pygame

from dino_mite_model.level_model.base_level_model import BaseLevelModel
from dino_mite_model.character_game.vertical_hazard import Bomb
from dino_mite_model.character_game.horizontal_hazard import Helicopter, HelicopterTwo, Drone


class LevelThree(BaseLevelModel):
    """
    Level 3 entity container: 2 helicopters + 3 bombs + 1 drone.

    Helicopter  - flies left-to-right, drops bombs every 120 frames.
    HelicopterTwo - flies right-to-left, drops bombs every 150 frames.
    Bombs are inactive by default.
    Drone - flies at mid-height, randomly switching LTR/RTL; player must duck.

    !Adjust! image and sound paths once Level 3 assets are ready.
    """

    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story.txt"))

        # ── Hazards ───────────────────────────────────────────────────────────
        self.hazard_helicopter    = Helicopter()
        self.hazard_helicopterTwo = HelicopterTwo()
        self.hazard_bomb          = Bomb()
        self.hazard_bombOne       = Bomb()
        self.hazard_bombTwo       = Bomb()
        self.hazard_drone         = Drone()

        # ── Win-sequence animation (placeholder — replace when Level 3 asset is ready) ──
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(
                os.path.join('./image/level_one', 'wormhole.png')
            ).convert_alpha(),
            (450, 450)
        )
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (400, 300)

        # ── Assets ────────────────────────────────────────────────────────────
        self.image          = os.path.join('./image/level_three/', 'backgroundLevelThree.jpg')
        self.sound          = os.path.join('./music', 'Level3-BackgroundMusic.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelOne.mp3')
        self.sound_volume   = 0.20
