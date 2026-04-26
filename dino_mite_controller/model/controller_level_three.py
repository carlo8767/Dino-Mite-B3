from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.levelthree import LevelThree


class ControllerLevelThree(BaseLevelController):
    """
    Controller for Level 3.

    Hazards: 1 helicopter (horizontal, sky level) + 2 bombs (vertical, dropped
    by the helicopter) + 1 drone (horizontal, mid-height).

    The helicopter flies across the top of the screen. Every _drop_interval
    frames it signals should_drop(), and this controller activates the next
    idle bomb at the helicopter's current x position. This creates the visual
    of bombs falling directly from beneath the helicopter.

    All four hazards are in slowed_hazards so the slowdown powerup affects
    the helicopter speed (changing where bombs land) and the drone speed.
    Bomb fall speed is also slowed while active.
    """

    def __init__(self):
        self.level_model = LevelThree()
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_helicopter,
            self.level_model.hazard_bomb,
            self.level_model.hazard_bombOne,
            self.level_model.hazard_drone,
        ]

    def update_movement(self):
        """Move all hazards, then drop a bomb from the helicopter if the timer fires."""
        super().update_movement()

        if self.level_model.hazard_helicopter.should_drop():
            drop_x = self.level_model.hazard_helicopter.rect.centerx
            drop_y = self.level_model.hazard_helicopter.rect.bottom
            for bomb in (self.level_model.hazard_bomb, self.level_model.hazard_bombOne):
                if not bomb.is_active:
                    bomb.activate_at(drop_x, drop_y)
                    break
