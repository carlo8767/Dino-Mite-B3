from dino_mite_controller.controller_level_one import ControllerLevelOne
from dino_mite_controller.controller_level_two import ControllerLevelTwo
from dino_mite_controller.controller_level_three import ControllerLevelThree


class EventsController:
    """Factory that creates a fresh controller for each level.
    Always returns a new instance so Play Again starts from a clean state."""

    def event_level_one_notification(self):
        return ControllerLevelOne()

    def event_level_two_notification(self):
        return ControllerLevelTwo()

    def event_level_three_notification(self):
        return ControllerLevelThree()
