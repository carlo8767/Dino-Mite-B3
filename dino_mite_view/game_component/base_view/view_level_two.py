import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelTwo(BaseLevelView):
    """
    Level Two view, only Level 2 specific rendering lives here.
    """

    time_duration_level = 9  # Level 2 is 90 seconds, adjust when confirmed
    level_number        = 2

    def __init__(self):
        super().__init__()
        self._ch_arm = pygame.mixer.Channel(2)

    def draw_screen_level_two(self, window, controller):
        """Entry point called by GameStateInteractor."""
        return self.draw_screen(window, controller)

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_model.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw(self, window, controller, background):
        window.blit(background, (0, 0))
        self._draw_hud(window, controller)

        if self.active_player_one:
            controller.level_model.character.draw(window)
        if self.active_two_player:
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
            self.sound_manager.play_looping("BigArm", self.level_number, self._ch_arm)

    def _win_sequence(self, window, controller, background, clock):
        controller.stop_music()
        pygame.mixer.stop()
        # TODO: add Level 2 win animation when assets are ready
        return "STORY_L2_TO_L3"

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over level two")
        controller.stop_music()
        return "STORY_FAILURE"

    def _next_level(self):
        return "STORY_L2_TO_L3"
