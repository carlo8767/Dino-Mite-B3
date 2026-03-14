import pygame

from dino_mite_view.event_game_notifications.event_controller import EventsController
from dino_mite_view.game_component.viewLevelOne import ViewLevelOne
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT
from dino_mite_view.game_component.start_menu import MainMenu
from dino_mite_view.game_component.start_story_screen import Start_Story_Screen


class FrameGameComponent:
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

    def __init__(self):
        self.init_game()

    def init_game(self):
        pygame.init()
        window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption(utilities_names.INIT_GAME)
        fps = pygame.time.Clock()

        init_event = EventsController()
        view_level_one = ViewLevelOne()
        main_menu = MainMenu(window)
        story_screen = Start_Story_Screen(window)

        self.GAME_STATE = "STORY"
        controller_level_one = None

        while self.RUN_GAME:

            # ==================== GLOBAL EVENTS ====================
            # Handle window close from any state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUN_GAME = False
                if self.GAME_STATE == "STORY":
                    action = story_screen.handle_event(event)
                    if action == "SKIP":
                        self.GAME_STATE = "MAIN_MENU"
                # Forward events to main menu when active
                elif self.GAME_STATE == "MAIN_MENU":
                    action = main_menu.handle_event(event)
                    if action == "START":
                        self.GAME_STATE = utilities_names.LEVEL_ONE
                    elif action == "EXIT":
                        self.RUN_GAME = False

            # ==================== STATE: MAIN MENU ====================
            if self.GAME_STATE == "STORY":
                story_screen.draw()
            elif self.GAME_STATE == "MAIN_MENU":
                main_menu.draw()

            # ==================== STATE: LEVEL ONE INIT ====================
            # Create the controller once, then move to the draw state
            elif self.GAME_STATE == utilities_names.LEVEL_ONE:
                controller_level_one = init_event.event_level_one_notification()
                self.GAME_STATE = "DrawLevelOne"

            # ==================== STATE: LEVEL ONE RUNNING ====================
            # The level view runs its own game loop internally.
            # When it returns, we check the result:
            #  "MAIN_MENU" - player paused and chose "Return to Menu"
            #   None        - player closed the window
            if self.GAME_STATE == "DrawLevelOne":
                result = view_level_one.draw_screen_level_one(window, controller_level_one)
                if result == "MAIN_MENU":
                    self.GAME_STATE = "MAIN_MENU"
                else:
                    self.RUN_GAME = False

            pygame.display.update()
            fps.tick(60)

        pygame.quit()