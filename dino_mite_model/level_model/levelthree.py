import os

import pygame

from dino_mite_model.level_model.base_level_model import BaseLevelModel


class LevelThree(BaseLevelModel):
    """
    Level 3 entity container.

    Add Level 3 hazard instances here. Each hazard must have:
      - update_position()           called every frame to move it
      - update_position_collision() called to reset it after a collision
      - name  (str)                 used by the collision system
      - speed or move_x (int/float) used by the slowdown powerup

    Example:
        self.hazard_??? = ???()
    """

    def __init__(self):
        super().__init__(os.path.join("./text_files", "end_story_level_three.txt"))

        # ── Hazards ───────────────────────────────────────────────────────────
        # TODO: add Level 3 hazard instances here
        # self.hazard_??? = ???()

        # ── Win-sequence animation ────────────────────────────────────────────
        # TODO: load the Level 3 win animation image
        # self.image_loaded = pygame.transform.scale(
        #     pygame.image.load(os.path.join('./image/level_three', '???.png')).convert_alpha(),
        #     (450, 450)
        # )
        # self.rect = self.image_loaded.get_rect()
        # self.rect.center = (400, 300)

        # ── Assets ────────────────────────────────────────────────────────────
        # TODO: replace with Level 3 specific asset paths
        self.image          = os.path.join('./image/level_three/', 'backgroundLevelThree.jpeg')
        self.sound          = os.path.join('./music', 'SoundLevelThree.mp3')
        self.sound_end_game = os.path.join('./music', 'EndGameLevelThree.mp3')
