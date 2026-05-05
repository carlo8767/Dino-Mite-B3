import random
import pygame
from dino_mite_controller.base_level_controller import BaseLevelController
from dino_mite_model.level_model.levelthree import LevelThree


class ControllerLevelThree(BaseLevelController):
    """
    Controller for Level 3.

    Hazards: 2 helicopters + 3 bombs + 1 drone.

    All hazards are in slowed_hazards so the slow powerup reduces helicopter
    speeds (shifting bomb landing zones) and the drone speed, while also
    slowing active bomb fall speeds.
    """

    def __init__(self):
        self.level_model = LevelThree()
        self.level_number = 3
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_helicopter,
            self.level_model.hazard_helicopterTwo,
            self.level_model.hazard_bomb,
            self.level_model.hazard_bombOne,
            self.level_model.hazard_bombTwo,
            self.level_model.hazard_drone,
        ]

    def update_movement_hazard(self):
        """Move all hazards, then check each helicopter's drop timer."""
        super().update_movement_hazard()

        bombs = (
            self.level_model.hazard_bomb,
            self.level_model.hazard_bombOne,
            self.level_model.hazard_bombTwo,
        )

        for helicopter in (
            self.level_model.hazard_helicopter,
            self.level_model.hazard_helicopterTwo,
        ):
            if helicopter.should_drop():
                drop_x = helicopter.rect.centerx
                drop_y = helicopter.rect.bottom
                for bomb in bombs:
                    if not bomb.is_active:
                        bomb.activate_at(drop_x, drop_y)
                        break

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