import os
import pygame
import logging
import random

from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility.utilities_names import WIDTH, HEIGHT
from dino_mite_utility.sound_manager import SoundManager


class BaseLevelView:
    """
    Base class for all level views.
    Contains all shared logic - event handling, timer, pause, powerup drawing,
    shield drawing, death animation, HUD, and all sound effects.
    Subclasses override only what is level-specific.

    Subclass contract
    -----------------
    Set level_number as a class attribute so hazard sounds are routed correctly:
        class ViewLevelTwo(BaseLevelView):
            level_number = 2
    """

    # Subclasses override these two values
    time_duration_level = 120
    level_number        = 0

    def __init__(self):
        self.pause_time_total = 0
        self.pause_start = 0
        self.eventually_time = ""
        self.remaining_time = ""
        self.remaining_seconds = 0
        self.time_reduction_ms = 0
        self.start_ticks = 0
        self.font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        self.shield_bubble_image = pygame.transform.scale(
            pygame.image.load("./image/bubble/ShieldBubbleforChar.png").convert_alpha(),
            (150, 150)
        )
        self.active_two_player = False
        self.active_player_one = False
        self.portal_active = False
        self.portal_rect = None
        self.portal_start_ticks = 0
        self.portal_image = pygame.image.load("./image/portal_2.png").convert_alpha()
        self.portal_image = pygame.transform.scale(self.portal_image, (90, 130))

        # Sound effects (powerup pickups, shield, hazard resets)
        self.sound_manager = SoundManager()

    def draw_screen(self, window, controller):
        """
        Main game loop - identical structure for all levels.
        Subclasses do not override this - they override the draw/sequence methods.
        """
        controller.init_music()
        clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        background = self._load_background(controller)
        pause_menu = PauseMenu(window)
        game_over = False
        delta_time = 0
        collided_player_two = False
        collided_player_one = False

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
            if not controller.is_paused and not game_over:
                # ANOTHER MAGIC
                keys = pygame.key.get_pressed()
                if self.active_two_player:
                    controller.handle_player_input_two(keys, events)
                    controller.apply_player_gravity_two()

                controller.handle_player_input(keys, events)
                controller.apply_player_gravity()
                # MAGIC
                if not self.portal_active:
                    controller.update_movement()

                # Tick shield / slowdown timers; snapshot shield state before
                shield_before_tick = controller.level_model.character.shield_active
                shield_before_tickPlayerTwo = controller.level_model.characterTwo.shield_active
                # TA MAGIC
                controller.update_powerup(delta_time, controller.level_model.character)

                controller.update_powerup(delta_time, controller.level_model.characterTwo)
                # Shield expired naturally
                if shield_before_tick and not controller.level_model.character.shield_active:
                    self.sound_manager.play_shield_pop()
                if shield_before_tickPlayerTwo and  not controller.level_model.characterTwo.shield_active:
                    self.sound_manager.play_shield_pop()

                # Powerup collectior FIX TAMAGIC POWER UP LOGIC
                if self.active_player_one:
                    collected_player_one_power_up = controller.detection_collision_powerup(controller.level_model.character)
                    if collected_player_one_power_up == "TimeReduction":
                        self.time_reduction_ms += 5000
                    if collected_player_one_power_up:
                        # TAMAGIC
                        self.sound_manager.play_powerup_pickup(collected_player_one_power_up)
                # MAGIC DANGEROUS
                if self.active_two_player:
                    collected_player_two_power_up = controller.detection_collision_powerup(controller.level_model.characterTwo)
                    if collected_player_two_power_up == "TimeReduction":
                        self.time_reduction_ms += 5000
                    if collected_player_two_power_up:
                        # TAMAGIC
                        self.sound_manager.play_powerup_pickup(collected_player_two_power_up)
                # MAGIC DANGEROUS
                if self.active_two_player and not self.portal_active:
                    collided_player_two, name = controller.detection_collision_character(
                        controller.level_model.characterTwo
                    )
                # Hazard collision — snapshot shield before to detect deflect
                if self.active_player_one and not self.portal_active:
                    shield_before_hit = controller.level_model.character.shield_active
                    collided_player_one, name = controller.detection_collision_character(
                        controller.level_model.character
                    )
                # Shield deflected the hit
                if not collided_player_one and shield_before_hit and not controller.level_model.character.shield_active:
                    self.sound_manager.play_shield_pop()
                    # Shield deflected the hit
                # ANOTHER MAGIC
                if collided_player_one and not  self.active_two_player :
                    logging.info(f"Collision detected with {name} — game over")
                    controller.update_collision_position(name)
                    controller.stop_music()
                    pygame.mixer.stop()
                    game_over = True

                if collided_player_one and self.active_two_player:
                    logging.info(f"Collision detected with {name} — game over")
                    controller.update_collision_position(name)
                    controller.stop_music()
                    pygame.mixer.stop()
                    self.active_player_one = False


                if  collided_player_two:
                    logging.info(f"Collision detected with {name} — game over")
                    controller.update_collision_position(name)
                    controller.stop_music()
                    self.active_two_player = False


                if not collided_player_two and shield_before_hit and not controller.level_model.characterTwo.shield_active:
                    self.sound_manager.play_shield_pop()

                if collided_player_two and collided_player_one:
                    logging.info(f"Collision detected with {name} — game over")
                    controller.update_collision_position(name)
                    controller.stop_music()
                    pygame.mixer.stop()
                    game_over = True

            self.calculate_timer(self.time_duration_level, controller.is_paused)

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

            # Portal collision + countdown — checked AFTER draw so player always sees the phase
            if self.portal_active and self.portal_rect is not None and not controller.is_paused:
                self.portal_countdown_ms = max(0, 5000 - (pygame.time.get_ticks() - self.portal_start_ticks))
                if self.active_player_one and controller.level_model.character.rect.colliderect(self.portal_rect):
                    return self._loading_transition(window, clock, self._next_level())
                if self.active_two_player and controller.level_model.characterTwo.rect.colliderect(self.portal_rect):
                    return self._loading_transition(window, clock, self._next_level())
                if self.portal_countdown_ms <= 0:
                    return self._loading_transition(window, clock, self._next_level())

            if game_over:
                # WHAT DO YOU RETURN EMPTY YOU CAN DELETE
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
            self.remaining_seconds = max(0, total_seconds - elapsed_ms // 1000)
            mins, secs = divmod(self.remaining_seconds, 60)
            self.remaining_time = f"{mins:02d}:{secs:02d}"
            self.eventually_time = self.remaining_time

    # ==================== SHARED DRAW HELPERS ====================
    def _draw_hud(self, window, controller):
        """Draws timer, powerup, shield bubble - identical for all levels."""
        # Falling powerup
        if controller.current_powerup and controller.current_powerup.is_active:
            controller.current_powerup.draw(window)

        # Shield bubble around character
        if controller.level_model.character.shield_active:
            shield_rect = self.shield_bubble_image.get_rect()
            shield_rect.center = controller.level_model.character.rect.center
            window.blit(self.shield_bubble_image, shield_rect)
        # MAGIC TA
        if controller.level_model.characterTwo.shield_active:
            shield_rect = self.shield_bubble_image.get_rect()
            shield_rect.center = controller.level_model.characterTwo.rect.center
            window.blit(self.shield_bubble_image, shield_rect)

        # Timer - dark oval backdrop then text on top
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
        """Death fade animation — identical for all levels. No text overlay."""
        # SEE HOW TO ADJUST MAGIC
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
                # VERIFY IF MODIFY
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
        if self.active_player_one:
            controller.level_model.character.draw(window)
        if self.active_two_player:
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
        t = pygame.time.get_ticks() % 800      # 0 -> 799 ms cycle
        pulse = t / 400.0 if t < 400 else (800 - t) / 400.0  # triangle wave 0 -> 1 -> 0
        b = int(255 * pulse)                   # (255,255,0) yellow <-> (255,255,255) white
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


