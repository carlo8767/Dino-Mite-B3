from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.levelthree import LevelThree


class ControllerLevelThree(BaseLevelController):
    """
    Controller for Level 3.

    Hazards: 2 helicopters + 3 bombs + 1 drone.

    Both helicopters independently signal should_drop().  Each time one fires
    this controller activates the next idle bomb at that helicopter's position,
    so bombs visually fall from whichever helicopter dropped them.

    All hazards are in slowed_hazards so the slow powerup reduces helicopter
    speeds (shifting bomb landing zones) and the drone speed, while also
    slowing active bomb fall speeds.
    """

    def __init__(self):
        self.level_model = LevelThree()
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

    def update_movement(self):
        """Move all hazards, then check each helicopter's drop timer."""
        super().update_movement()

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
