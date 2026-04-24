from dino_mite_controller.model.controller_level_one import ControllerLevelOne

class EventsController:

    def event_level_one_notification(self):
        # Always return a fresh controller so Play Again starts from a clean state
        return ControllerLevelOne()
