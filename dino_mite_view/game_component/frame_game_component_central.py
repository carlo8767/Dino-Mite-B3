import pygame

from dino_mite_view.event_game_notifications.event_controller import EventsController
from dino_mite_view.game_component.viewLevelOne import ViewLevelOne
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class FrameGameComponent:
    """
    Top-level game frame that owns the pygame window and manages
    which screen is currently active.
    """

    RUN_GAME = True
    GAME_STATE = ""

    def __init__(self):
        self.init_game()

    def init_game(self):
        """
        Initialise pygame, create the window, and enter the main
        application loop that renders the correct level view.
        """
        pygame.init()
        window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption(utilities_names.INIT_GAME)
        fps = pygame.time.Clock()

        # Set up helpers
        init_event = EventsController()
        view_level_one = ViewLevelOne()

        # Start on Level One
        self.GAME_STATE = utilities_names.LEVEL_ONE
        controller_level_one = None

        while self.RUN_GAME:
            # ---- Handle top-level quit events ----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUN_GAME = False

            # ---- Game State (runs once per frame, NOT per event) ----

            if self.GAME_STATE == utilities_names.LEVEL_ONE:
                controller_level_one = init_event.event_level_one_notification()
                self.GAME_STATE = "DrawLevelOne"

            if self.GAME_STATE == "DrawLevelOne":
                # Hand control to the Level One view (its own game loop runs
                # inside draw_screen_level_one and returns when the level ends)
                view_level_one.draw_screen_level_one(window, controller_level_one)

                # Once the level view returns, stop the outer loop.
                # (Replace with a state transition when more levels exist,
                #  e.g. self.GAME_STATE = utilities_names.LEVEL_TWO)
                self.RUN_GAME = False

            pygame.display.update()
            fps.tick(60)

        pygame.quit()