import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelThree(BaseLevelView):
    """
    Level Three view, only Level 3 specific rendering lives here.
    """

    time_duration_level = 60  # 60 seconds

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

        m = controller.level_model

        # Helicopters (always on screen — fly continuously in opposite directions)
        window.blit(m.hazard_helicopter.image_loaded,    m.hazard_helicopter.rect)
        window.blit(m.hazard_helicopterTwo.image_loaded, m.hazard_helicopterTwo.rect)

        # Bombs (only draw when active — inactive bombs are parked off-screen)
        for bomb in (m.hazard_bomb, m.hazard_bombOne, m.hazard_bombTwo):
            if bomb.is_active:
                window.blit(bomb.image_loaded, bomb.rect)

        # Drone (always on screen — flies at mid-height, direction randomised)
        window.blit(m.hazard_drone.image_loaded, m.hazard_drone.rect)

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

    def _next_level(self):
        return "GAME OVER"
