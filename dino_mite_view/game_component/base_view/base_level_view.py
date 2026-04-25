import os
import pygame
import logging
import random

from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class BaseLevelView:
    """
    Base class for all level views.
    Contains all shared logic — event handling, timer, pause, powerup drawing,
    shield drawing, death animation, HUD.
    Subclasses override only what is level-specific.
    """

    # Subclasses override this number only
    time_duration_level = 120

    def __init__(self):
        self.pause_time_total = 0
        self.pause_start = 0
        self.eventually_time = ""
        self.remaining_time = ""
        self.time_reduction_ms = 0
        self.start_ticks = 0
        self.font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        self.shield_bubble_image = pygame.transform.scale(
            pygame.image.load("./image/bubble/ShieldBubbleforChar.png").convert_alpha(),
            (150, 150)
        )

        self.portal_active = False
        self.portal_rect = None

    def draw_screen(self, window, controller):
        """
        Main game loop — identical structure for all levels.
        Subclasses do not override this — they override the draw/sequence methods.
        """
        controller.init_music()
        clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        background = self._load_background(controller)
        pause_menu = PauseMenu(window)
        game_over = False
        delta_time = 0

        while True:
            events = pygame.event.get()

            # ==================== EVENT HANDLING ====================
            for event in events:
                if event.type == pygame.QUIT:
                    return "EXIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not controller.is_paused:
                        self.pause_start = pygame.time.get_ticks()
                        controller.toggle_pause_menu()
                    elif event.key == pygame.K_ESCAPE and controller.is_paused:
                        pause_duration = pygame.time.get_ticks() - self.pause_start
                        self.pause_time_total += pause_duration
                        controller.toggle_pause_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if controller.is_paused:
                        result = pause_menu.handle_click(event)
                        if result == "CONTINUE":
                            controller.toggle_pause_menu()
                            pause_duration = pygame.time.get_ticks() - self.pause_start
                            self.pause_time_total += pause_duration
                        elif result == "RETURN_TO_MENU":
                            controller.toggle_pause_menu()
                            controller.stop_music()
                            return "MAIN_MENU"

            # ==================== UPDATE ====================
            if not controller.is_paused and not game_over:
                keys = pygame.key.get_pressed()
                controller.handle_player_input(keys, events)
                controller.apply_player_gravity()
                controller.update_movement()

                controller.update_powerup(delta_time)

                collected = controller.detection_collision_powerup()
                if collected == "TimeReduction":
                    self.time_reduction_ms += 5000

                collided, name = controller.detection_collision_character(
                    controller.level_model.character
                )
                if collided and name in ("RollingRock", "Meteor"):
                    logging.info(f"Collision detected with {name} — game over")
                    controller.update_collision_position(name)
                    controller.stop_music()
                    game_over = True

                if self.portal_active and self.portal_rect is not None:
                    if controller.level_model.character.rect.colliderect(self.portal_rect):
                        return self._loading_transition(window, clock, self._next_level())

            self.calculate_timer(self.time_duration_level, controller.is_paused)
            self._draw(window, controller, background)

            if self.portal_active and self.portal_rect is not None:
                pygame.draw.rect(window, (0, 255, 0), self.portal_rect)

            if controller.is_paused:
                pause_menu.draw()

            # ==================== END CONDITIONS ====================
            if self.remaining_time == "00:00" and not self.portal_active:
                self.portal_active = True
                self._spawn_portal(controller)

            if game_over:
                return self._lose_sequence(window, controller, clock)

            pygame.display.update()
            delta_time = clock.tick(60)

    # ==================== TIMER ====================
    def calculate_timer(self, total_seconds, is_paused):
        if not is_paused:
            elapsed_ms = (
                pygame.time.get_ticks()
                - self.start_ticks
                - self.pause_time_total
                + self.time_reduction_ms
            )
            remaining_seconds = max(0, total_seconds - elapsed_ms // 1000)
            mins, secs = divmod(remaining_seconds, 60)
            self.remaining_time = f"{mins:02d}:{secs:02d}"
            self.eventually_time = f"Time to jump: {mins:02d}:{secs:02d}"

    # ==================== SHARED DRAW HELPERS ====================
    def _draw_hud(self, window, controller):
        """Draws timer, powerup, shield bubble — identical for all levels."""
        # Falling powerup
        if controller.current_powerup and controller.current_powerup.is_active:
            controller.current_powerup.draw(window)

        # Shield bubble around character
        if controller.level_model.character.shield_active:
            shield_rect = self.shield_bubble_image.get_rect()
            shield_rect.center = controller.level_model.character.rect.center
            window.blit(self.shield_bubble_image, shield_rect)

        # Timer text
        font_type = pygame.font.Font(self.font_path, 60)
        color_timer = (255, 255, 0)
        img = font_type.render(self.eventually_time, True, color_timer)
        rect = img.get_rect()
        rect.center = (400, 20)
        window.blit(img, rect)

    def draw_text_end(self, window, controller):
        """Death message text — reads from level model."""
        split_text = controller.level_model.store_text_end.split("\n")
        pos_x = 400
        font_type = pygame.font.Font(self.font_path, 60)
        color_text = (255, 255, 0)
        for i, line in enumerate(split_text):
            img = font_type.render(line, True, color_text)
            rect = img.get_rect()
            rect.center = (pos_x, 100 + i * 60)
            window.blit(img, rect)

    def faded_screen(self, window, controller, clock):
        """Death fade animation — identical for all levels."""
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        self.draw_text_end(window, controller)
        pygame.time.delay(500)
        screen_copy = window.copy()
        countdown = 500
        while countdown > 0:
            for alpha in range(0, 255, 20):
                fade.set_alpha(alpha)
                window.blit(screen_copy, (0, 0))
                window.blit(fade, (0, 0))
                controller.apply_change_player_status(window, "dead")
                pygame.display.update()
                clock.tick(60)
            for alpha in range(255, 0, 20):
                fade.set_alpha(alpha)
                window.blit(screen_copy, (0, 0))
                window.blit(fade, (0, 0))
                controller.apply_change_player_status(window, "dead")
                pygame.display.update()
                clock.tick(60)
            countdown -= 300
        for alpha in range(0, 255, 1):
            fade.set_alpha(alpha)
            window.blit(screen_copy, (0, 0))
            window.blit(fade, (0, 0))
            controller.apply_change_player_status(window, "dead")
            pygame.display.update()
            pygame.time.delay(10)   
            clock.tick(60)

    def _spawn_portal(self, controller):
        portal_width = 60
        portal_height = 80
        character = controller.level_model.character
        ground_y = character.constant_ground
        player_x = character.rect.x

        possible_x_positions = [
            x for x in range(80, WIDTH - portal_width - 80)
            if abs(x - player_x) > 180
        ]

        if not possible_x_positions:
            portal_x = WIDTH - portal_width - 80
        else:
            portal_x = random.choice(possible_x_positions)

        self.portal_rect = pygame.Rect(
            portal_x,
            ground_y + character.standing_height - portal_height,
            portal_width,
            portal_height
        )

    def _loading_transition(self, window, clock, next_state):
        font = pygame.font.Font(self.font_path, 70)

        for alpha in range(0, 255, 5):
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            window.blit(overlay, (0, 0))

            text = font.render("ENTERING PORTAL...", True, (255, 255, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            window.blit(text, rect)

            pygame.display.update()
            clock.tick(60)

        pygame.time.delay(700)
        return next_state

    # ==================== ABSTRACT METHODS ====================
    # Subclasses MUST implement these   

    def _load_background(self, controller):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _load_background")

    def _draw(self, window, controller, background):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _draw")

    def _win_sequence(self, window, controller, background, clock):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _win_sequence")

    def _lose_sequence(self, window, controller, clock):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _lose_sequence")
    
    def _next_level(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement _next_level")