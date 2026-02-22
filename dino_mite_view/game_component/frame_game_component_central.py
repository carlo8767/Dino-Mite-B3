import pygame


from dino_mite_model.level_model.levelone import LevelOne
from dino_mite_view.event_game_notifications.event_view import EventsView


class FrameGameComponent:
    WIDTH = 3000
    HEIGHT = 3000
    RUN_GAME = True
    GAME_STATE = ""

    list_model = dict()

    def __init__(self):
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
        self.add_model("LevelOne", LevelOne)


        while self.RUN_GAME:

            self.GAME_STATE = "LevelOne"
            for event in pygame.event.get():
                """
                ADD LOGIC YEAR FOR LEVEL ONE AFTER THE USER PASS THE STORYLINE
                """

                # HERE WE SET THE OUTPUT BASE ON THE GAME STATE
                # VERIFY IF IT SHOULD BE BETTER DO SEPARATELY
                if self.GAME_STATE == "LevelOne":
                    # UPDATE THE WINDOW
                    init_event.event_level_one_notification()

            pygame.display.update()
            fps.tick(60)





