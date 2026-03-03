import pygame


from dino_mite_view.event_game_notifications.event_controller import EventsController
from dino_mite_view.game_component.viewLevelOne import ViewLevelOne

from dino_mite_utility import  utilities_names

class FrameGameComponent():
    WIDTH = 800
    HEIGHT = 800
    RUN_GAME = True
    GAME_STATE = ""

    # VERIFY HOW TO HIDE  VIEW HIDE VIEW ?
    list_model = dict()

    def __init__(self):
        self.init_game()

    def init_game (self):
        pygame.init()
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pygame.display.set_caption(utilities_names.INIT_GAME)
        fps = pygame.time.Clock()
        init_event = EventsController()
        view_level_one = ViewLevelOne()
        while self.RUN_GAME:
            self.GAME_STATE = utilities_names.LEVEL_ONE
            for event in pygame.event.get():
                """
                ADD LOGIC YEAR FOR LEVEL ONE AFTER THE USER PASS THE STORYLINE
                """
                # HERE WE SET THE OUTPUT BASE ON THE GAME STATE
                # VERIFY IF IT SHOULD BE BETTER DO SEPARATELY
                if self.GAME_STATE == utilities_names.LEVEL_ONE:

                    # UPDATE THE WINDOW ASK
                    view_level = init_event.event_level_one_notification()
                    self.GAME_STATE = "DrawLevelOne"

                    # WAIT UNTIL IS FINISH
                if self.GAME_STATE == "DrawLevelOne":
                       # self.draw_window_level_one(window,view_level)
                       view_level_one.draw_screen_level_one(window,view_level)
                       # view_level_one.draw_window_level_one(window, view_level)
                pygame.display.update()
                fps.tick(60)



