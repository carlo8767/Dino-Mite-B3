from dino_mite_model.character_game.Hazard import Meteor
from dino_mite_model.level_model.levelone import LevelOne




class ControllerLevelOne:

    def __init__(self):
        # ADD MODEL  VERIFY IF HERE
        self.level_one = LevelOne()
        self.hazards = []

    def update_level_one(self):
        for hazard in self.hazards:
            hazard.update_position()
        self.hazards = [hazard for hazard in self.hazards if hazard.is_active]

    def spawn_meteor(self):
        self.hazards.append(Meteor())

    def start_level_one (self):
        return self.level_one
