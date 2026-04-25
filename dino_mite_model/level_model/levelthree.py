import os

import pygame

from dino_mite_model.level_model.base_level_model import BaseLevelModel


class LevelThree(BaseLevelModel):
    """
    Level 3 entity container.

    Background, music, and win animation are loaded.
    Add Level 3 hazard instances when ready - each hazard must expose:
      - update_position()           called every frame to move it
      - update_position_collision() called to reset it after a collision
      - name  (str)                 used by the collision system
      - speed or move_x (int/float) used by the slowdown powerup
    """

    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story.txt"))

        # ── Hazards ───────────────────────────────────────────────────────────
        # TODO: add Level 3 hazard instances here
        # self.hazard_??? = ???()

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
        self.sound          = os.path.join('./music', 'Portal.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelOne.mp3')
