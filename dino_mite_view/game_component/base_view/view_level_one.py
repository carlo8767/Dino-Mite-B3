import pygame
import logging

from dino_mite_view.game_component.base_view.base_level_view import BaseLevelView
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelOne(BaseLevelView):
    """Level One view, only level-specific logic lives here."""

    time_duration_level = 120  # 2 minutes

    def __init__(self):
        super().__init__()

    def draw_screen_level_one(self, window, controller):
        """Entry point kept for backwards compatibility with GameStateInteractor."""
        return self.draw_screen(window, controller)

    # ==================== LEVEL ONE SPECIFIC ====================

    def _load_background(self, controller):
        img = pygame.image.load(controller.level_model.image).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))

    def _draw(self, window, controller, background):
        # Background
        window.blit(background, (0, 0))

        # Shared HUD (powerup, shield, timer)
        self._draw_hud(window, controller)

        # Character
        controller.level_model.character.draw(window)

        # Hazards
        if controller.level_model.hazard_meteor.is_active:
            window.blit(
                controller.level_model.hazard_meteor.image_loaded,
                controller.level_model.hazard_meteor.rect,
            )
        if controller.level_model.hazard_meteorOne.is_active:
            window.blit(
                controller.level_model.hazard_meteorOne.image_loaded,
                controller.level_model.hazard_meteorOne.rect,
            )
        if controller.level_model.hazard_meteorTwo.is_active:
            window.blit(
                controller.level_model.hazard_meteorTwo.image_loaded,
                controller.level_model.hazard_meteorTwo.rect,
            )
        window.blit(
            controller.level_model.hazard_rollingRock.image_loaded,
            controller.level_model.hazard_rollingRock.rect,
        )

    def _win_sequence(self, window, controller, background, clock):
        pygame.time.delay(500)
        controller.stop_music()
        pygame.mixer.music.load(controller.level_model.sound_complete_level)
        pygame.mixer.music.play(-1, 25.0)
        controller.level_model.character.draw_status(window, "happy")
        self._draw(window, controller, background)
        self.draw_text_end_level(window)
        pygame.time.delay(500)
        pygame.display.update()
        clock.tick(60)
        self.draw_elements_pass_level(window, controller, background, clock)
        controller.stop_music()
        pygame.mixer.stop()
        return "STORY_L1_TO_L2"

    def _lose_sequence(self, window, controller, clock):
        controller.init_music_end_level()
        self.faded_screen(window, controller, clock)
        logging.info("game over")
        controller.stop_music()
        return "STORY_FAILURE"

    # ==================== LEVEL ONE ANIMATIONS ====================

    def draw_elements_pass_level(self, window, controller, background, clock):
        img_loop = controller.level_model.image_loaded
        y = 510
        x = 370
        controller.level_model.character.set_current_position(x, y)
        while y > 200:
            y -= 5
            controller.level_model.character.set_current_position(x, y)
            window.blit(background, (0, 0))
            self.draw_text_end_level(window)
            img_loop.set_alpha(255)
            window.blit(img_loop, controller.level_model.rect)
            controller.level_model.character.draw(window)
            pygame.display.update()
            clock.tick(40)
            window.blit(background, (0, 0))
            self.draw_text_end_level(window)
            img_loop.set_alpha(0)
            window.blit(img_loop, controller.level_model.rect)
            controller.level_model.character.draw(window)
            pygame.display.update()
            clock.tick(40)
        screen_copy = window
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 255, 1):
            fade.set_alpha(alpha)
            window.blit(screen_copy, (0, 0))
            window.blit(fade, (0, 0))
            pygame.display.update()
            clock.tick(50)

    def draw_text_end_level(self, window):
        split_text = ["LEVEL PASSED!", "READY TO JUMP?"]
        pos_x = 400
        font_type = pygame.font.Font(self.font_path, 60)
        color_text = (255, 255, 0)
        img = font_type.render(split_text[0], True, color_text)
        rect = img.get_rect()
        rect.center = (pos_x, 500)
        window.blit(img, rect)
        img = font_type.render(split_text[1], True, color_text)
        rect = img.get_rect()
        rect.center = (pos_x, 60)
        window.blit(img, rect)

    def _next_level(self):
        return "STORY_L1_TO_L2"