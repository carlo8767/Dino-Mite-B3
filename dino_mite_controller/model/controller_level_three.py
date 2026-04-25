from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.levelthree import LevelThree


class ControllerLevelThree(BaseLevelController):
    """
    Controller for Level 3.

    Once Level 3 hazards are added to LevelThree, list them in
    register_slowable_hazards() below. That single list drives:
      - collision detection
      - frame-by-frame movement
      - the slowdown powerup effect
      - level reset positions
    """

    def __init__(self):
        self.level_model = LevelThree()
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            # TODO: add Level 3 hazard instances once defined in LevelThree
            # self.level_model.hazard_???,
        ]
