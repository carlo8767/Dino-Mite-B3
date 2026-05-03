import os
import pygame
import random
from abc import ABC, abstractmethod

from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class BaseLevelView(ABC):
    """
    Base class for all level views.
    Responsible only for rendering: timer display, shield bubble, portal phase,
    death animation, and HUD. All game logic lives in the controller.

    Subclass contract
    -----------------
    Set level_number as a class attribute so hazard sounds are routed correctly:
        class ViewLevelTwo(BaseLevelView):
            level_number = 2

    Subclasses must implement:
        _load_background(controller)
        _draw(window, controller, background)
        _lose_sequence(window, controller, clock)
        _next_level()
    """

    time_duration_level = 120
    level_number        = 0

    def __init__(self):
        self.pause_time_total = 0
        self.pause_start = 0
        self.eventually_time = ""
        self.remaining_time = ""
        self.remaining_seconds = 0
        self.start_ticks = 0
        self.font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        self.shield_bubble_image = pygame.transform.scale(
            pygame.image.load("./image/bubble/ShieldBubbleforChar.png").convert_alpha(),
            (150, 150)
        )
        self.portal_active = False
        self.portal_rect = None
        self.portal_start_ticks = 0
        self.portal_countdown_ms = 0
        self.portal_image = pygame.image.load("./image/portal_2.png").convert_alpha()
        self.portal_image = pygame.transform.scale(self.portal_image, (90, 130))

    def draw_screen(self, window, controller):
        """
        Main game loop — identical structure for all levels.
        Subclasses do not override this; they override the draw/sequence methods.
        """
        controller.init_music()
        clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        background = self._load_background(controller)
        pause_menu = PauseMenu(window)
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

                if event.type == pygame.MOUSEBUTTONUP:
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
            if not controller.is_paused and not controller.game_over:
                keys = pygame.key.get_pressed()
                controller.update(delta_time, keys, events, self.portal_active)

            self.calculate_timer(self.time_duration_level, controller.is_paused, controller.time_reduction_ms)

            # ==================== DRAW ====================
            if self.portal_active and self.portal_rect is not None:
                self._draw_portal_phase(window, controller, background)
            else:
                self._draw(window, controller, background)

            if controller.is_paused:
                pause_menu.draw(events)

            # ==================== END CONDITIONS ====================
            if self.remaining_time == "00:00" and not self.portal_active:
                self.portal_active = True
                self.portal_start_ticks = pygame.time.get_ticks()
                self._spawn_portal(controller)

            if self.portal_active and self.portal_rect is not None and not controller.is_paused:
                self.portal_countdown_ms = max(0, 5000 - (pygame.time.get_ticks() - self.portal_start_ticks))
                if controller.player_one_active and controller.level_model.character.rect.colliderect(self.portal_rect):
                    return self._loading_transition(window, clock, self._next_level())
                if controller.player_two_active and controller.level_model.characterTwo.rect.colliderect(self.portal_rect):
                    return self._loading_transition(window, clock, self._next_level())
                if self.portal_countdown_ms <= 0:
                    return self._loading_transition(window, clock, self._next_level())

            if controller.game_over:
                return self._lose_sequence(window, controller, clock)

            pygame.display.update()
            delta_time = clock.tick(60)

    # ==================== TIMER ====================

    def calculate_timer(self, total_seconds, is_paused, time_reduction_ms):
        if not is_paused:
            elapsed_ms = (
                pygame.time.get_ticks()
                - self.start_ticks
                - self.pause_time_total
                + time_reduction_ms
            )
            self.remaining_seconds = max(0, total_seconds - elapsed_ms // 1000)
            mins, secs = divmod(self.remaining_seconds, 60)
            self.remaining_time = f"{mins:02d}:{secs:02d}"
            self.eventually_time = self.remaining_time

    # ==================== SHARED DRAW HELPERS ====================

    def _draw_hud(self, window, controller):
        """Draws timer, powerup, shield bubbles - identical for all levels."""
        if controller.current_powerup and controller.current_powerup.is_active:
            controller.current_powerup.draw(window)

        if controller.level_model.character.shield_active:
            shield_rect = self.shield_bubble_image.get_rect()
            shield_rect.center = controller.level_model.character.rect.center
            window.blit(self.shield_bubble_image, shield_rect)
        if controller.level_model.characterTwo.shield_active:
            shield_rect = self.shield_bubble_image.get_rect()
            shield_rect.center = controller.level_model.characterTwo.rect.center
            window.blit(self.shield_bubble_image, shield_rect)

        # Timer — dark oval backdrop then text on top
        font_type = pygame.font.Font(self.font_path, 36)
        if self.remaining_seconds <= 10:
            t = pygame.time.get_ticks() % 600
            pulse = t / 300.0 if t < 300 else (600 - t) / 300.0
            color_timer = (255, int(255 * (1 - pulse)), 0)
        else:
            color_timer = (255, 255, 0)
        img = font_type.render(self.eventually_time, True, color_timer)
        text_rect = img.get_rect(center=(WIDTH // 2, 22))
        pad_x, pad_y = 22, 10
        oval_surf = pygame.Surface((text_rect.width + pad_x * 2, text_rect.height + pad_y * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(oval_surf, (0, 0, 0, 140), oval_surf.get_rect())
        oval_rect = oval_surf.get_rect(center=text_rect.center)
        window.blit(oval_surf, oval_rect)
        window.blit(img, text_rect)

        if controller.show_time_reduction_hud > 0:
            font_hud = pygame.font.Font(self.font_path, 44)
            hud_img = font_hud.render("-5", True, (255, 80, 0))
            window.blit(hud_img, hud_img.get_rect(center=(WIDTH // 2, 58)))

    def draw_text_end(self, window, controller):
        """Death message text - reads from level model."""
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
        """Death fade animation - identical for all levels."""
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
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

    def _draw_portal(self, window):
        portal_draw_rect = self.portal_image.get_rect(center=self.portal_rect.center)
        window.blit(self.portal_image, portal_draw_rect)

    def _draw_portal_phase(self, window, controller, background):
        window.blit(background, (0, 0))
        if controller.player_one_active:
            controller.level_model.character.draw(window)
        if controller.player_two_active:
            controller.level_model.characterTwo.draw(window)
        self._draw_portal(window)
        self._draw_portal_prompt(window)
        self._draw_portal_countdown(window)

    def _draw_portal_countdown(self, window):
        seconds_left = max(0, (self.portal_countdown_ms + 999) // 1000)
        font = pygame.font.Font(self.font_path, 72)
        text = font.render(str(seconds_left), True, (255, 255, 0))
        shadow = font.render(str(seconds_left), True, (0, 0, 0))
        rect = text.get_rect(center=(WIDTH // 2, 110))
        window.blit(shadow, rect.move(4, 4))
        window.blit(text, rect)

    def _draw_portal_prompt(self, window):
        t = pygame.time.get_ticks() % 800
        pulse = t / 400.0 if t < 400 else (800 - t) / 400.0
        b = int(255 * pulse)
        color = (255, 255, b)
        font = pygame.font.Font(self.font_path, 42)
        text = font.render("GO TO THE PORTAL!", True, color)
        shadow = font.render("GO TO THE PORTAL!", True, (0, 0, 0))
        rect = text.get_rect(center=(WIDTH // 2, 55))
        window.blit(shadow, rect.move(3, 3))
        window.blit(text, rect)

    def _spawn_portal(self, controller):
        portal_width = 90
        portal_height = 130
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

    # ==================== ABSTRACT METHODS ====================

    @abstractmethod
    def _load_background(self, controller):
        ...

    @abstractmethod
    def _draw(self, window, controller, background):
        ...

    @abstractmethod
    def _lose_sequence(self, window, controller, clock):
        ...

    @abstractmethod
    def _next_level(self):
        ...

    def _loading_transition(self, window, clock, next_state):
        pygame.mixer.music.stop()
        pygame.mixer.stop()
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
