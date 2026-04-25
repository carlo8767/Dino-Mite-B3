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

    time_duration_level = 90  # Level 2 is 90 seconds, adjust when confirmed

    def __init__(self):
        super().__init__()

    def draw_screen_level_two(self, window, controller):
        """Entry point called by GameStateInteractor."""
        return self.draw_screen(window, controller)

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_one.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw(self, window, controller, background):
        window.blit(background, (0, 0))
        self._draw_hud(window, controller)
        controller.level_one.character.draw(window)

        # TODO: add Level 2 hazard drawing here when Person A delivers LevelTwo model
        if controller.level_one.hazard_meteor.is_active:
            window.blit(
                controller.level_one.hazard_meteor.image_loaded,
                controller.level_one.hazard_meteor.rect,
            )
        if controller.level_one.hazard_meteorOne.is_active:
            window.blit(
                controller.level_one.hazard_meteorOne.image_loaded,
                controller.level_one.hazard_meteorOne.rect,
            )
        if controller.level_one.hazard_meteorTwo.is_active:
            window.blit(
                controller.level_one.hazard_meteorTwo.image_loaded,
                controller.level_one.hazard_meteorTwo.rect,
            )
        window.blit(
            controller.level_one.hazard_rollingRock.image_loaded,
            controller.level_one.hazard_rollingRock.rect,
        )

    def _win_sequence(self, window, controller, background, clock):
        controller.stop_music()
        pygame.mixer.stop()
        # TODO: add Level 2 win animation when assets are ready
        return "LEVEL_THREE"

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level_one()
        self.faded_screen(window, controller, clock)
        logging.info("game over level two")
        controller.stop_music()
        return "GAME OVER"