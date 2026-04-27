from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.leveltwo import LevelTwo


class ControllerLevelTwo(BaseLevelController):
    """
    Controller for Level 2.

    Hazards: 3 fireballs (vertical) + 1 mammoth leg (vertical stomp).
    
    All four are registered so collision detection, movement, the slowdown
    powerup, and level reset all work automatically.
    """

    def __init__(self):
        self.level_model = LevelTwo()
        self.level_number = 2
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            self.level_model.hazard_fireball,
            self.level_model.hazard_fireballOne,
            self.level_model.hazard_fireballTwo,
            self.level_model.hazard_mammothLeg,
        ]
