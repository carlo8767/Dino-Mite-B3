import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT, STORY_FAILURE, STORY_L2_TO_L3


class ViewLevelTwo(BaseLevelView):
    """
    Level Two view, only Level 2 specific rendering lives here.
    """

    time_duration_level = 120  # Level 2 is 90 seconds, adjust when confirmed
    level_number        = 2

    def __init__(self):
        super().__init__()
        self._ch_arm = pygame.mixer.Channel(2)

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

        m = controller.level_model

        # Fireballs (vertical — only draw when active)
        if m.hazard_fireball.is_active:
            window.blit(m.hazard_fireball.image_loaded, m.hazard_fireball.rect)
        if m.hazard_fireballOne.is_active:
            window.blit(m.hazard_fireballOne.image_loaded, m.hazard_fireballOne.rect)
        if m.hazard_fireballTwo.is_active:
            window.blit(m.hazard_fireballTwo.image_loaded, m.hazard_fireballTwo.rect)

        # BigArm (always on screen — hangs, slams, retracts)
        arm = m.hazard_bigArm
        window.blit(arm.image_loaded, arm.rect)
        # Play stomp sound during slam and hold phases
        if arm._phase in (arm._SLAM, arm._HOLD):
            controller.sound_manager.play_looping("BigArm", self.level_number, self._ch_arm)

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over level two")
        controller.stop_music()
        return STORY_FAILURE

    def _next_level(self):
        return STORY_L2_TO_L3
