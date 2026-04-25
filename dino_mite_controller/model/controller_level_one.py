from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.levelone import LevelOne


class ControllerLevelOne(BaseLevelController):
    """
    Controller for Level 1.

    Level 1 hazards: 3 meteors + 1 rolling rock.
    All game logic lives in BaseLevelController — only the hazard list is level-specific.
    """

    def __init__(self):
        self.level_model = LevelOne()
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_meteor,
            self.level_model.hazard_meteorOne,
            self.level_model.hazard_meteorTwo,
            self.level_model.hazard_rollingRock,
        ]
