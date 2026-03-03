from dino_mite_controller.model.controller_level_one import ControllerLevelOne
from dino_mite_model.level_model.levelone import LevelOne


class EventsController:

    def __init__(self):
        # ADD SUBSCRIBER CONTROLLER
        self.controller_level_one =  ControllerLevelOne()


    def event_level_one_notification(self):
        level_one_state_model = self.controller_level_one.start_level_one()
        return level_one_state_model
