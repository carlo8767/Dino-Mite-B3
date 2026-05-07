import pygame
import logging

from dino_mite_view.event_game_notifications.event_controller import EventsController
from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_view.game_component.base_view.view_level_one import ViewLevelOne
from dino_mite_view.game_component.base_view.view_level_two import ViewLevelTwo
from dino_mite_view.game_component.base_view.view_level_three import ViewLevelThree
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import *
from dino_mite_view.game_component.view_start_menu import ViewMainMenu
from dino_mite_view.game_component.display_story import ViewDisplayStory
from dino_mite_view.game_component.view_game_over import ViewGameOverMenu
from dino_mite_view.game_component.view_rules import ViewRules


class GameStateInteractor:
    """
    Top-level game frame that owns the pygame window and manages
    which screen is currently active.

    Game states:
        MAIN_MENU       - Shows the start/exit menu
        LEVEL_ONE       - Initialises level one controller
        DRAW_LEVEL_ONE  - Runs the level one game loop
        LEVEL_TWO       - Initialises level two controller
        DRAW_LEVEL_TWO  - Runs the level two game loop
        LEVEL_THREE     - Initialises level three controller
        DRAW_LEVEL_THREE- Runs the level three game loop
        RULES           - Displays rules
        GAME_OVER       - Shows game over screen
    """
    RUN_GAME = True
    GAME_STATE = ""

    def __init__(self):
        self.self_execution = ""

    def init_game(self):
        logging.basicConfig(
            level=logging.WARNING,
            filename="game.log",
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True
        )
        logging.info("Enter in init_game")
        pygame.init()
        window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption(utilities_names.INIT_GAME)
        init_event = EventsController()

        view_main_menu = ViewMainMenu(window)
        view_story_screen = ViewDisplayStory()
        view_rules = ViewRules()

        self.GAME_STATE = STORY

        active_player_player_two_mode = False
        controller_level_one = None
        controller_level_two = None
        controller_level_three = None
        while self.RUN_GAME:
            # ==================== STATE: MAIN MENU ====================
            if self.GAME_STATE == STORY:
                logging.info(f'current game state {self.GAME_STATE}')
                self.GAME_STATE = view_story_screen.draw_story_screen(window)
            elif self.GAME_STATE == MAIN_MENU:
                logging.info(f'current game state {self.GAME_STATE}')
                active_player_player_two_mode = False
                self.GAME_STATE = view_main_menu.draw_start_menu()
            elif self.GAME_STATE == RULES:
                logging.info(f'current game state {self.GAME_STATE}')
                self.GAME_STATE = view_rules.draw_rules_screen(window)

            # ==================== STATE: LEVEL ONE INIT ====================
            elif self.GAME_STATE == utilities_names.LEVEL_ONE:
                controller_level_one = init_event.event_level_one_notification()
                self.GAME_STATE = DRAW_LEVEL_ONE
                logging.info(f'current game state {self.GAME_STATE}')
            elif self.GAME_STATE == EXIT:
                self.RUN_GAME = False
                logging.info(f'current game state {self.GAME_STATE}')
            elif self.GAME_STATE == DRAW_LEVEL_ONE:
                view_level_one = ViewLevelOne()
                controller_level_one.player_one_active = True
                self.set_view_strategy(view_level_one)

                self.GAME_STATE = self.execution_view_strategy(view_level_one, window, controller_level_one,
                                                               active_player_player_two_mode)
                logging.info(f'current game state {self.GAME_STATE}')
            elif self.GAME_STATE == TWO_PLAYERS:
                active_player_player_two_mode = True
                controller_level_one = init_event.event_level_one_notification()
                view_level_one = ViewLevelOne()
                self.set_view_strategy(view_level_one)
                controller_level_one.player_two_active = True
                controller_level_one.player_one_active = True
                self.GAME_STATE = self.execution_view_strategy(view_level_one, window, controller_level_one,
                                                               active_player_player_two_mode)
                logging.info(f'current game state {self.GAME_STATE}')
            # ==================== STATE: LEVEL TWO INIT ====================
            elif self.GAME_STATE == LEVEL_TWO:
                logging.info(f'current game state {self.GAME_STATE}')
                controller_level_two = init_event.event_level_two_notification()
                self.GAME_STATE = DRAW_LEVEL_TWO

            elif self.GAME_STATE == DRAW_LEVEL_TWO:
                logging.info(f'current game state {self.GAME_STATE}')
                view_level_two = ViewLevelTwo()
                self.set_view_strategy(view_level_two)
                if active_player_player_two_mode:
                    controller_level_two.player_two_active = True
                controller_level_two.player_one_active = True
                self.GAME_STATE = self.execution_view_strategy(view_level_two, window, controller_level_two,
                                                               active_player_player_two_mode)
            # ==================== STATE: LEVEL THREE INIT ====================
            elif self.GAME_STATE == LEVEL_THREE:
                logging.info(f'current game state {self.GAME_STATE}')
                controller_level_three = init_event.event_level_three_notification()
                self.GAME_STATE = DRAW_LEVEL_THREE

            elif self.GAME_STATE == DRAW_LEVEL_THREE:
                logging.info(f'current game state {self.GAME_STATE}')
                view_level_three = ViewLevelThree()
                self.set_view_strategy(view_level_three)
                if active_player_player_two_mode:
                    controller_level_three.player_two_active = True
                controller_level_three.player_one_active = True
                self.GAME_STATE = self.execution_view_strategy(view_level_three, window, controller_level_three,
                                                               active_player_player_two_mode)
            # ==================== TRANSITION STORIES ====================
            elif self.GAME_STATE == STORY_L1_TO_L2:
                logging.info(f'current game state {self.GAME_STATE}')
                transition_story = ViewDisplayStory(story_part=2, next_state=LEVEL_TWO)
                self.GAME_STATE = transition_story.draw_story_screen(window)

            elif self.GAME_STATE == STORY_L2_TO_L3:
                logging.info(f'current game state {self.GAME_STATE}')
                transition_story = ViewDisplayStory(story_part=3, next_state=LEVEL_THREE)
                self.GAME_STATE = transition_story.draw_story_screen(window)

            elif self.GAME_STATE == STORY_SUCCESS:
                logging.info(f'current game state {self.GAME_STATE}')
                success_story = ViewDisplayStory(story_part=4, next_state=MAIN_MENU)
                self.GAME_STATE = success_story.draw_story_screen(window)

            elif self.GAME_STATE == STORY_FAILURE:
                logging.info(f'current game state {self.GAME_STATE}')
                failure_story = ViewDisplayStory(story_part=5, next_state=GAME_OVER)
                self.GAME_STATE = failure_story.draw_story_screen(window)

            # ==================== GAME_OVER ====================
            elif self.GAME_STATE == GAME_OVER:
                view_level_game_over = ViewGameOverMenu(window)
                logging.info(f'current game state {self.GAME_STATE}')
                result = view_level_game_over.init_game_over(active_player_player_two_mode)
                self.GAME_STATE = result
        pygame.quit()

    def set_view_strategy(self, base_level: BaseLevelView):
        self.self_execution = base_level

    def execution_view_strategy(self, base_level: BaseLevelView, window, controller, active_player_player_two_mode):
        return base_level.draw_screen(window, controller, active_player_player_two_mode)
