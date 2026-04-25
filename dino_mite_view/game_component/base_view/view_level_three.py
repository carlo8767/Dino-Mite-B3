import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelThree(BaseLevelView):
    """
    Level Three view.
    Extends BaseLevelView — only Level 3 specific rendering lives here.
    Waiting on Person A to deliver ControllerLevelThree and LevelThree model.
    """

    time_duration_level = 60  # Level 3 is 60 seconds, adjust when confirmed

    def __init__(self):
        super().__init__()

    def draw_screen_level_three(self, window, controller):
        """Entry point called by GameStateInteractor."""
        return self.draw_screen(window, controller)

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_model.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw(self, window, controller, background):
        window.blit(background, (0, 0))
        self._draw_hud(window, controller)
        controller.level_model.character.draw(window)

        # TODO: add Level 3 hazard drawing here when Person A delivers LevelThree model
        if controller.level_model.hazard_meteor.is_active:
            window.blit(
                controller.level_model.hazard_meteor.image_loaded,
                controller.level_model.hazard_meteor.rect,
            )
        window.blit(
            controller.level_model.hazard_rollingRock.image_loaded,
            controller.level_model.hazard_rollingRock.rect,
        )

    def _win_sequence(self, window, controller, background, clock):
        controller.stop_music()
        pygame.mixer.stop()
        # TODO: add Level 3 win animation when assets are ready
        return "GAME OVER"  # Level 3 is the final level

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over level three")
        controller.stop_music()
        return "GAME OVER"