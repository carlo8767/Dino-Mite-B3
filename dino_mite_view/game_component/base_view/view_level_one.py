import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT, STORY_FAILURE, STORY_L1_TO_L2


class ViewLevelOne(BaseLevelView):
    """Level One view, only level-specific logic lives here."""

    time_duration_level = 120  # 2 minutes
    level_number        = 1

    def __init__(self):
        super().__init__()
        self._ch_meteor = pygame.mixer.Channel(0)
        self._ch_rock   = pygame.mixer.Channel(1)

    # ==================== LEVEL ONE SPECIFIC ====================

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_model.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw_elements_view(self, window, controller, background):
        # Background
        window.blit(background, (0, 0))

        # Shared HUD (powerup, shield, timer)
        self._draw_hud(window, controller)

        # Character
        if controller.player_one_active:
            controller.level_model.character.draw(window)

        if controller.player_two_active:
            controller.level_model.characterTwo.draw(window)

        m = controller.level_model

        # Hazards
        if m.hazard_meteor.is_active:
            window.blit(m.hazard_meteor.image_loaded, m.hazard_meteor.rect)
        if m.hazard_meteorOne.is_active:
            window.blit(m.hazard_meteorOne.image_loaded, m.hazard_meteorOne.rect)
        if m.hazard_meteorTwo.is_active:
            window.blit(m.hazard_meteorTwo.image_loaded, m.hazard_meteorTwo.rect)
        window.blit(m.hazard_rollingRock.image_loaded, m.hazard_rollingRock.rect)

        # Ambient hazard sounds
        any_meteor = m.hazard_meteor.is_active or m.hazard_meteorOne.is_active or m.hazard_meteorTwo.is_active
        if any_meteor:
            controller.sound_manager.play_looping("Meteor", self.level_number, self._ch_meteor)
        else:
            self._ch_meteor.stop()
        controller.sound_manager.play_looping("RollingRock", self.level_number, self._ch_rock)


    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over")
        controller.stop_music()
        return STORY_FAILURE


    def _next_level(self):
        return STORY_L1_TO_L2
