import pygame

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
        pygame.init()
        window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption(utilities_names.INIT_GAME)
        fps = pygame.time.Clock()

        init_event = EventsController()
        # REVIEW GAME STORY !!!!
        view_main_menu = View_MainMenu(window)
        view_story_screen = ViewStartStoryScreen()

        self.GAME_STATE = STORY
        controller_level_one = None

        while self.RUN_GAME:

            # ==================== GLOBAL EVENTS ====================
            # Handle window close from any state
            #for event in pygame.event.get():
             #   if event.type == pygame.QUIT:
              #      self.RUN_GAME = False
                # Forward events to main menu when active



            # ==================== STATE: MAIN MENU ====================
            if self.GAME_STATE == STORY:
                self.GAME_STATE = view_story_screen.draw_story_screen(window)
            if self.GAME_STATE == "MAIN_MENU":
                 self.GAME_STATE = view_main_menu.draw_start_menu()
            if self.GAME_STATE == "EXIT":
                self.RUN_GAME = False
            # ==================== STATE: LEVEL ONE INIT ====================
            # Create the controller once, then move to the draw state
            if self.GAME_STATE == utilities_names.LEVEL_ONE:
                controller_level_one = init_event.event_level_one_notification()
                self.GAME_STATE = "DrawLevelOne"

            if self.GAME_STATE == "GAME OVER":
                self.GAME_STATE = "DrawGameOver"

            # ==================== STATE: LEVEL ONE RUNNING ====================
            # The level view runs its own game loop internally.
            # When it returns, we check the result:
            #  "MAIN_MENU" - player paused and chose "Return to Menu"
            #   None        - player closed the window
            if self.GAME_STATE == "DrawLevelOne":
                view_level_one = ViewLevelOne()
                result = view_level_one.draw_screen_level_one(window, controller_level_one)
                self.GAME_STATE = result

            if self.GAME_STATE == "GAME OVER":
                view_level_game_over = ViewGameOverMenu(window)
                result = view_level_game_over.init_game_over()
                self.GAME_STATE = result
                #else:
                 #  self.RUN_GAME = False
        pygame.quit()