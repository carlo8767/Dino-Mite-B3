import pygame
import logging

from dino_mite_view.event_game_notifications.event_controller import EventsController
from dino_mite_view.game_component.viewLevelOne import ViewLevelOne
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT, STORY
from dino_mite_view.game_component.view_start_menu import View_MainMenu
from dino_mite_view.game_component.view_start_story_screen import ViewStartStoryScreen
from dino_mite_view.game_component.view_game_over import ViewGameOverMenu


class GameStateInteractor:
    """
    Top-level game frame that owns the pygame window and manages
    which screen is currently active.

    Game states:
        MAIN_MENU    - Shows the start/exit menu
        LEVEL_ONE    - Initialises level one controller
        DrawLevelOne - Runs the level one game loop
    """
    RUN_GAME = True
    GAME_STATE = ""

    def init_game(self):
        logging.basicConfig(level=logging.INFO, filename="login.log")

        pygame.init()
        window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption(utilities_names.INIT_GAME)
        init_event = EventsController()

        view_main_menu = View_MainMenu(window)
        view_story_screen = ViewStartStoryScreen()

        self.GAME_STATE = STORY
        controller_level_one = None
        while self.RUN_GAME:
            # ==================== STATE: MAIN MENU ====================
            if self.GAME_STATE == "STORY":
                logging.info(f'current game state {self.GAME_STATE}')
                self.GAME_STATE = view_story_screen.draw_story_screen(window)
            elif self.GAME_STATE == "MAIN_MENU":
                 logging.info(f'current game state {self.GAME_STATE}')
                 self.GAME_STATE = view_main_menu.draw_start_menu()
            # ==================== STATE: LEVEL ONE INIT ====================
            elif self.GAME_STATE == utilities_names.LEVEL_ONE:
                controller_level_one = init_event.event_level_one_notification()
                self.GAME_STATE = "DRAW_LEVEL_ONE"
                logging.info(f'current game state {self.GAME_STATE}')
            elif self.GAME_STATE == "EXIT":
                self.RUN_GAME = False
                logging.info(f'current game state {self.GAME_STATE}')
            elif self.GAME_STATE == "DRAW_LEVEL_ONE":
                view_level_one = ViewLevelOne()
                logging.info(f'current game state {self.GAME_STATE}')
                self.GAME_STATE = view_level_one.draw_screen_level_one(window, controller_level_one)
            # ==================== GAME OVER ====================
            elif self.GAME_STATE == "GAME OVER":
                view_level_game_over = ViewGameOverMenu(window)
                logging.info(f'current game state {self.GAME_STATE}')
                result = view_level_game_over.draw_game_over()
                self.GAME_STATE = result
        pygame.quit()