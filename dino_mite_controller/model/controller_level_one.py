

from dino_mite_model.level_model.levelone import LevelOne




class ControllerLevelOne:

    def __init__(self):
        # ADD MODEL  VERIFY IF HERE
        self.level_one = LevelOne()

    def start_level_one (self):
        return self.level_one
