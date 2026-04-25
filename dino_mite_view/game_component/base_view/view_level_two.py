import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelTwo(BaseLevelView):
    """
    Level Two view.
    Extends BaseLevelView — only Level 2 specific rendering lives here.
    Waiting on Person A to deliver ControllerLevelTwo and LevelTwo model.
    """

    time_duration_level = 10  # Level 2 is 90 seconds, adjust when confirmed

    def __init__(self):
        super().__init__()

    def draw_screen_level_two(self, window, controller):
        """Entry point called by GameStateInteractor."""
        return self.draw_screen(window, controller)

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_model.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw(self, window, controller, background):
        window.blit(background, (0, 0))
        self._draw_hud(window, controller)
        controller.level_model.character.draw(window)
        # TODO: add Level 2 hazard drawing here once hazards are defined in LevelTwo model

    def _win_sequence(self, window, controller, background, clock):
        controller.stop_music()
        pygame.mixer.stop()
        # TODO: add Level 2 win animation when assets are ready
        return "LEVEL_THREE"

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over level two")
        controller.stop_music()
        return "GAME OVER"
    
    def _next_level(self):
        return "LEVEL_THREE"