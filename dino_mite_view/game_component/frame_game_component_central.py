import pygame
import threading

from dino_mite_view.event_game_notifications.event_view import EventsView
from dino_mite_view.game_component.viewLevelOne import ViewLevelOne


class FrameGameComponent:
    WIDTH = 800
    HEIGHT = 800
    RUN_GAME = True
    GAME_STATE = ""


    list_model = dict()

    def __init__(self):
        self.view_notification = threading.Event()
        self.init_game()

    def add_model(self, name_model, model):
        self.list_model[name_model] = model


    def init_game (self):
        # VERIFY HOW TO HIDE  VIEW HIDE VIEW ?
        pygame.init()
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pygame.display.set_caption("INIT GAME")
        fps = pygame.time.Clock()
        init_event = EventsView()
        #ADD MODEL YOU JUST ADD THE MODEL
        view_level = ""
        view_level_one = ViewLevelOne()
        while self.RUN_GAME:

            self.GAME_STATE = "LevelOne"
            for event in pygame.event.get():
                """
                ADD LOGIC YEAR FOR LEVEL ONE AFTER THE USER PASS THE STORYLINE
                """

                # HERE WE SET THE OUTPUT BASE ON THE GAME STATE
                # VERIFY IF IT SHOULD BE BETTER DO SEPARATELY
                if self.GAME_STATE == "LevelOne":
                    # UPDATE THE WINDOW ASK
                    view_level = init_event.event_level_one_notification()
                    self.add_model("LevelOne", view_level)
                    self.GAME_STATE = "DrawLevel"
                    # WAIT UNTIL IS FINISH
                if self.GAME_STATE == "DrawLevel":
                       # self.draw_window_level_one(window,view_level)
                       view_level_one.draw_window_level_one(window, view_level)
                pygame.display.update()
                fps.tick(60)





    def receive_update_view_level_one(self):
        self.view_notification.wait()
        pygame.display.update()


    def draw_window_level_oneffff(self, window, levelOne):
         sprite_image_background = pygame.image.load(levelOne.image).convert()
         pygame.display.set_caption("LEVEL ONE")
         window.blit(sprite_image_background, (0, 0))







