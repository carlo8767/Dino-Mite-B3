from dino_mite_controller.model.base_level_controller import BaseLevelController
from dino_mite_model.level_model.leveltwo import LevelTwo


class ControllerLevelTwo(BaseLevelController):
    """
    Controller for Level 2.

    Once Level 2 hazards are added to LevelTwo, list them in
    register_slowable_hazards() below. That single list drives:
      - collision detection
      - frame-by-frame movement
      - the slowdown powerup effect
      - level reset positions
    """

    def __init__(self):
        self.level_model = LevelTwo()
        super().__init__()

    def register_slowable_hazards(self):
        self.slowed_hazards = [
            # TODO: add Level 2 hazard instances once defined in LevelTwo
            # self.level_model.hazard_???,
        ]
