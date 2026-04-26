import os

import pygame

from dino_mite_model.level_model.base_level_model import BaseLevelModel
from dino_mite_model.character_game.vertical_hazard import Bomb
from dino_mite_model.character_game.horizontal_hazard import Helicopter, Drone


class LevelThree(BaseLevelModel):
    """
    Level 3 entity container: 1 helicopter + 2 bombs + 1 drone.

    The helicopter flies across the top of the screen and drops bombs.
    Bombs are inactive by default — ControllerLevelThree activates them
    via Bomb.activate_at(x) whenever Helicopter.should_drop() fires.
    The drone flies at mid-height and requires the player to duck under it.

    !Adjust! image and sound paths once Level 3 assets are ready.
    !Adjust! bomb count if more simultaneous bombs are needed.
    """

    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story.txt"))

        # ── Hazards ───────────────────────────────────────────────────────────
        self.hazard_helicopter = Helicopter()
        self.hazard_bomb       = Bomb()
        self.hazard_bombOne    = Bomb()
        self.hazard_drone      = Drone()

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
        self.sound          = os.path.join('./music', 'SoundLevelOne.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelOne.mp3')
