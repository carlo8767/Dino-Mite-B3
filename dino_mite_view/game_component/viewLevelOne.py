import pygame
import logging
from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT
from dino_mite_view.game_component.view_game_over import ViewGameOverMenu

""" Main game loop for Level One"""
""" :param window: The main pygame display surface."""
""" :param ctr_levelOne: The ControllerLevelOne instance that manages game logic. """

class ViewLevelOne:

    def __init__(self):
        self.pause_time_resume = 0
        self.start_ticks = pygame.time.get_ticks()
        self.pause_time_total = 0
        self.pause_start = 0
        self.eventually_time = ""
        self.time_duration_level = 120


    def draw_screen_level_one(self, window, ctr_level_one):
        logging.info("Enter in view level one")
        ctr_level_one.init_music()
        clock = pygame.time.Clock()
        pygame.display.set_caption(utilities_names.LEVEL_ONE)
        sprite_image_background = pygame.image.load(
            ctr_level_one.level_one.image
        ).convert()
        sprite_image_background = pygame.transform.scale(
            sprite_image_background, (WIDTH, HEIGHT)
        )
        pause_menu = PauseMenu(window)
        game_over_menu = ViewGameOverMenu(window)
        game_over = False
        running = True
        while running:
            # ==================== EVENT HANDLING ====================
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                # Toggle pause with Escape key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and  not ctr_level_one.is_paused:
                        self.pause_start = pygame.time.get_ticks()
                        ctr_level_one.toggle_pause_menu()
                    # Detection pause and calculate time
                    elif event.key == pygame.K_ESCAPE and ctr_level_one.is_paused:
                        pause_duration = pygame.time.get_ticks() - self.pause_start
                        self.pause_time_total += pause_duration
                        ctr_level_one.toggle_pause_menu()
                # Handle clicks on the pause menu buttons (only when paused)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ctr_level_one.is_paused:
                        result = pause_menu.handle_click(event) #pass event instead of coordinates 
                        if result == "CONTINUE":
                            ctr_level_one.toggle_pause_menu()
                            pause_duration = pygame.time.get_ticks() - self.pause_start
                            self.pause_time_total += pause_duration
                        elif result == "RETURN_TO_MENU":
                             ctr_level_one.toggle_pause_menu()
                             ctr_level_one.stop_music()
                             return "MAIN_MENU"
                    elif game_over:
                        result = game_over_menu.handle_click(event)
                        if result == "RESTART":
                            return "DRAW_LEVEL_ONE"
                        if result == "MAIN_MENU":
                            return "MAIN_MENU"
            # ==================== UPDATE (skip when paused) ====================
            # added "and not game_over" so game freezes on game over screen
            if not ctr_level_one.is_paused and not game_over:
                # Pass raw inputs to the controller, it decides what to do
                keys = pygame.key.get_pressed()
                ctr_level_one.handle_player_input(keys,events)
                # Controller handles gravity
                ctr_level_one.apply_player_gravity()
                ctr_level_one.update_movement_level_one()

                # Check if the character collides with any hazard
                # collision only checks models_collision
                collided, name = ctr_level_one.detection_collision_character(
                    ctr_level_one.level_one.character
                )
                if collided:
                    # set game_over to True to trigger game over screen
                    logging.info(f"Collision detected with {name} — game over")
                    ctr_level_one.update_collision_position(name)
                    ctr_level_one.stop_music()
                    game_over = True

            self.calculate_timer(self.time_duration_level, ctr_level_one.is_paused)
            self.draw_elements(window, ctr_level_one, sprite_image_background, )

            if ctr_level_one.is_paused:
                pause_menu.draw()
            # GAME OVER
            if game_over:
                logging.info(f'game over')
                # pygame.time.delay(2500)
                game_over_menu.draw()
            pygame.display.update()
            clock.tick(60)

    # ==================== TIMER ====================
    def calculate_timer(self, total_seconds, is_paused):
        if not is_paused:
            elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.pause_time_total
            remaining_seconds = max(0, total_seconds - elapsed_ms // 1000)
            mins, secs = divmod(remaining_seconds, 60)
            timer_text = f"Time to jump: {mins:02d}:{secs:02d}"
            self.eventually_time = timer_text

    # ==================== DRAW ELEMENTS ====================
    def draw_elements(self, window, ctr_level_one,sprite_image_background ):

            # Background
            window.blit(sprite_image_background, (0, 0))
            # Character draw various images  CARLO
            ctr_level_one.level_one.character.draw(window)
            # Draw the original single hazard instances from the LevelOne model
            window.blit(
                ctr_level_one.level_one.hazard_meteor.image_loaded,
                ctr_level_one.level_one.hazard_meteor.rect,
            )
            window.blit(
                ctr_level_one.level_one.hazard_meteorOne.image_loaded,
                ctr_level_one.level_one.hazard_meteorOne.rect,
            )
            window.blit(
                ctr_level_one.level_one.hazard_meteorTwo.image_loaded,
                ctr_level_one.level_one.hazard_meteorTwo.rect,
            )
            window.blit(
                ctr_level_one.level_one.hazard_rollingRock.image_loaded,
                ctr_level_one.level_one.hazard_rollingRock.rect,
            )
            # ==================== DRAW  TIMER ====================
            font_type = pygame.font.SysFont("Comic Sans MS", 40)
            color_timer = (0, 0, 0)
            img = font_type.render(self.eventually_time, True, color_timer)
            rect = img.get_rect()
            rect.center = (400, 20)
            pygame.draw.rect(window, (0, 0, 0), rect, 2)
            window.blit(img, rect)
