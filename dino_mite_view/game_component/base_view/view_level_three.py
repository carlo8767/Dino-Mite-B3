import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelThree(BaseLevelView):
    """
    Level Three view, only Level 3 specific rendering lives here.
    """

    time_duration_level = 60  # 60 seconds
    level_number        = 3

    def __init__(self):
        super().__init__()
        self._ch_heli  = pygame.mixer.Channel(3)
        self._ch_drone = pygame.mixer.Channel(4)
        self._ch_bomb  = pygame.mixer.Channel(5)

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_model.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw_elements_view(self, window, controller, background):
        window.blit(background, (0, 0))
        self._draw_hud(window, controller)
        if controller.player_one_active:
            controller.level_model.character.draw(window)
        if controller.player_two_active:
            controller.level_model.characterTwo.draw(window)
        # WHAT THA M LIME
        m = controller.level_model

        # Helicopters (always on screen — fly continuously in opposite directions)
        window.blit(m.hazard_helicopter.image_loaded,    m.hazard_helicopter.rect)
        window.blit(m.hazard_helicopterTwo.image_loaded, m.hazard_helicopterTwo.rect)
        controller.sound_manager.play_looping("Helicopter", self.level_number, self._ch_heli)

        # Bombs (only draw when active — inactive bombs are parked off-screen)
        any_bomb = False
        for bomb in (m.hazard_bomb, m.hazard_bombOne, m.hazard_bombTwo):
            if bomb.is_active:
                window.blit(bomb.image_loaded, bomb.rect)
                any_bomb = True
        if any_bomb:
            controller.sound_manager.play_looping("Bomb", self.level_number, self._ch_bomb)

        # Drone (always on screen — flies at mid-height, direction randomised)
        window.blit(m.hazard_drone.image_loaded, m.hazard_drone.rect)
        controller.sound_manager.play_looping("Drone", self.level_number, self._ch_drone)

    # def _win_sequence(self, window, controller, background, clock):
    #     controller.stop_music()
    #     pygame.mixer.stop()
    #     # TODO: add Level 3 win animation when assets are ready
    #     return "STORY_SUCCESS"  # Level 3 is the final level

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over level three")
        controller.stop_music()
        return "STORY_FAILURE"

    def _next_level(self):
        return "STORY_SUCCESS"
