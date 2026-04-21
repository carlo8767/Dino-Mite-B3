import random
from curses.ascii import ctrl
import os
import pygame
import logging
import os
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

        self.pause_time_total = 0
        self.pause_start = 0
        self.eventually_time = ""
        self.remaining_time = ""
        self.time_duration_level = 120
        self.font_path_level_one = os.path.join("./fonts", "Jersey10-Regular.ttf")
        # self.store_text_end = self.upload_file()
        self.shield_bubble_image = pygame.transform.scale(
            pygame.image.load("./image/bubble/ShieldBubbleforChar.png").convert_alpha(), (150, 150)
        )
        self.is_active_bubble_chair = False
        self.count_down_bubble_chair = -1
        self.count_down_bubble_chair_active = False
        self.power_up_time_countdown = 0
        self.power_up_time_reduce_velocity = 0
        self.time_reduction  = 0
        self.active_count_down_slower = -1
        self.start_ticks = 0
        self.powerup_spawned = False
        self.count_down_second_reduction = 0
        self.time_reduction_applied = True


    def draw_screen_level_one(self, window, ctr_level_one):
        logging.info("Enter in view level one")
        ctr_level_one.init_music()
        clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        pygame.display.set_caption(utilities_names.LEVEL_ONE)
        sprite_image_background = pygame.image.load(
            ctr_level_one.level_one.image
        ).convert()
        sprite_image_background = pygame.transform.scale(
            sprite_image_background, (WIDTH, HEIGHT)
        )
        pause_menu = PauseMenu(window)
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
            # ==================== UPDATE (skip when paused) ====================
            # added "and not game_over" so game freezes on game over screen
            if not ctr_level_one.is_paused and not game_over:
                # Pass raw inputs to the controller, it decides what to do
                keys = pygame.key.get_pressed()
                ctr_level_one.handle_player_input(keys,events)
                # Controller handles gravity
                ctr_level_one.apply_player_gravity()
                ctr_level_one.update_movement_level_one()
                # update powerup position and spawn timer every 10 second
                if self.power_up_time_countdown  in [55, 45, 30, 20, 10] and  not self.powerup_spawned :
                    # INSTANTIATE  POWER UP
                    ctr_level_one.update_powerup()
                    self.powerup_spawned = True



                # Check if the character collides with any hazard
                # collision only checks models_collision
                collided, name = ctr_level_one.detection_collision_character(
                    ctr_level_one.level_one.character, self.is_active_bubble_chair
                )
                if collided and name == "TimeReduction" and  self.time_reduction_applied:
                    # self.time_reduction = 5 # shift timer reference back --> removes 5s remaining
                    logging.info(f"Collision detected with {name} ")
                    self.powerup_spawned = False
                    self.start_ticks -= 5000
                    ctr_level_one.level_one.pw_up_time_reduction.is_active_time_reduction = False
                    ctr_level_one.level_one.pw_up_time_reduction.update_position_collision()

                elif collided and name == "SlowerHazards":
                    # TARGET IN SECOND
                    self.active_count_down_slower = (self.power_up_time_countdown-5)
                    logging.info(f"Collision detected with {name} ")
                    ctr_level_one.apply_slow_hazards()
                    self.powerup_spawned = False
                    ctr_level_one.level_one.pw_up_slower_hazard.is_active_slower_hazard = False
                    ctr_level_one.level_one.pw_up_slower_hazard.update_position_collision()

                elif collided and name == "ShieldBubble":
                    ctr_level_one.level_one.pw_up_shield_bubble.active_power_up_icon_bubble = False
                    self.count_down_bubble_chair_active =  True
                    self.is_active_bubble_chair = True
                    self.powerup_spawned = False

                elif collided and name == "RollingRock" or name == "Meteor":
                    ctr_level_one.restore_hazard_speeds()
                    self.powerup_spawned = False

                    # set game_over to True to trigger game over screen
                    logging.info(f"Collision detected with {name} — game over")
                    ctr_level_one.update_collision_position(name)
                    ctr_level_one.stop_music()
                    game_over = True

                # WORKAROUND SLOWER TIME :
                if  self.power_up_time_countdown == self.active_count_down_slower:
                    self.active_count_down_slower = -1
                    ctr_level_one.restore_hazard_speeds()
                    self.powerup_spawned = False
                # BEGIN COUNT DOWN

                if self.count_down_bubble_chair_active:
                    # BEGINS COUNTDOWN
                    self.count_down_bubble_chair = self.power_up_time_countdown-5
                    self.count_down_bubble_chair_active = False
                if self.count_down_bubble_chair == self.power_up_time_countdown:
                    self.count_down_bubble_chair = -1
                    self.is_active_bubble_chair = False

            self.calculate_timer(self.time_duration_level, ctr_level_one.is_paused)
            # DRAW ALL THE ELEMENT
            self.draw_elements(window, ctr_level_one, sprite_image_background )

            if ctr_level_one.is_paused:
                pause_menu.draw()
                # ========= END CONDITION =========#
            if "00:00" == self.remaining_time:
                pygame.time.delay(500)
                ctr_level_one.stop_music()
                pygame.mixer.music.load(ctr_level_one.level_one.sound_complete_level)
                pygame.mixer.music.play(-1, 25.0)  # Forever Loop
                # VERIFY
                ctr_level_one.level_one.character.draw_status(window, "happy")
                self.draw_elements(window, ctr_level_one, sprite_image_background)
                self.draw_text_end_level(window)
                pygame.time.delay(500)
                pygame.display.update()
                clock.tick(60)
                self.draw_elements_pass_level(window, ctr_level_one, sprite_image_background, clock)
                ctr_level_one.stop_music()
                pygame.mixer.stop()
                # CHANGE WHEN  INTRODUCING LEVEL TWO
                return "GAME OVER"
            # GAME OVER
            elif game_over:
                # ADD HERE CHANGE IMAGE CHARACTER
                ctr_level_one.init_music_end_level_one()
                self.faded_screen(window, ctr_level_one, clock)
                logging.info(f'game over')
                ctr_level_one.stop_music()

                # HERE TRANSITION
                # pygame.time.delay(2500)
                return "GAME OVER"
            pygame.display.update()
            clock.tick(60)

    # ==================== TIMER ====================
    def calculate_timer(self, total_seconds, is_paused):
        if not is_paused:
            # if self.time_reduction_applied == False:

                elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.pause_time_total
                remaining_seconds = max(0, total_seconds - elapsed_ms // 1000)
                mins, secs = divmod(remaining_seconds, 60)
                # secs -= self.time_reduction
                self.power_up_time_countdown = secs
                timer_text = f"Time to jump: {mins:02d}:{secs:02d}"
                self.remaining_time = f'{mins:02d}:{secs:02d}'
                self.eventually_time = timer_text

    # ==================== DRAW ELEMENTS ====================
    def draw_elements(self, window, ctr_level_one,sprite_image_background ):

            # Background
            window.blit(sprite_image_background, (0, 0))

            if ctr_level_one.level_one.pw_up_shield_bubble.active_power_up_icon_bubble:
                ctr_level_one.level_one.pw_up_shield_bubble.draw_bubble(window)

            if self.is_active_bubble_chair == True:
                shield_rect = self.shield_bubble_image.get_rect()
                shield_rect.center = ctr_level_one.level_one.character.rect.center
                window.blit(self.shield_bubble_image, shield_rect)


            if ctr_level_one.level_one.pw_up_slower_hazard.is_active_slower_hazard:
                # ctr_level_one.level_one.pw_up_slower_hazard.draw_slower_hazard(window)
                window.blit(
                    ctr_level_one.level_one.pw_up_slower_hazard.image_loaded_slow_hazard,
                    ctr_level_one.level_one.pw_up_slower_hazard.rect,
                )

            if ctr_level_one.level_one.pw_up_time_reduction.is_active_time_reduction:
                # ctr_level_one.level_one.pw_up_time_reduction.draw_time_reduction(window)
                window.blit(
                    ctr_level_one.level_one.pw_up_time_reduction.image_loaded_time_reduction,
                    ctr_level_one.level_one.pw_up_time_reduction.rect,
                )
                # self.time_reduction = 0
                # self.count_down_second_reduction = 0



            # Character draw various images  CARLO
            ctr_level_one.level_one.character.draw(window)
            # Draw the original single hazard instances from the LevelOne model
            if ctr_level_one.level_one.hazard_meteor.is_active:
                window.blit(
                    ctr_level_one.level_one.hazard_meteor.image_loaded,
                    ctr_level_one.level_one.hazard_meteor.rect,
                )
            if ctr_level_one.level_one.hazard_meteorOne.is_active:
                window.blit(
                    ctr_level_one.level_one.hazard_meteorOne.image_loaded,
                    ctr_level_one.level_one.hazard_meteorOne.rect,
                )
            if ctr_level_one.level_one.hazard_meteorTwo.is_active:
                window.blit(
                    ctr_level_one.level_one.hazard_meteorTwo.image_loaded,
                    ctr_level_one.level_one.hazard_meteorTwo.rect,
                )
            window.blit(
                ctr_level_one.level_one.hazard_rollingRock.image_loaded,
                ctr_level_one.level_one.hazard_rollingRock.rect,
            )


            # ==================== DRAW  TIMER ====================
            font_type = pygame.font.Font(self.font_path_level_one, 60)
            color_timer = (255, 255, 0)
            img = font_type.render(self.eventually_time, True, color_timer)
            rect = img.get_rect()
            rect.center = (400, 20)
            # pygame.draw.rect(window, (0, 250, 0), rect, 2)
            window.blit(img, rect)



    # ==================== DRAW ELEMENTS PASS LEVEL====================
    def draw_elements_pass_level(self, window, ctr_level_one, sprite_image_background, clock):
        img_loop = ctr_level_one.level_one.image_loaded
        y = 510
        x = 370
        ctr_level_one.level_one.character.set_current_position(x, y)
        while y > 200:
            y -= 5
            ctr_level_one.level_one.character.set_current_position(x, y)
            # ON
            window.blit(sprite_image_background, (0, 0))
            self.draw_text_end_level(window)
            img_loop.set_alpha(255)
            window.blit(img_loop, ctr_level_one.level_one.rect)
            ctr_level_one.level_one.character.draw(window)
            pygame.display.update()
            clock.tick(40)
            # OFF
            window.blit(sprite_image_background, (0, 0))
            self.draw_text_end_level(window)
            img_loop.set_alpha(0)
            window.blit(img_loop, ctr_level_one.level_one.rect)
            ctr_level_one.level_one.character.draw(window)
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
        pos_y = 500
        font_type  =  pygame.font.Font(self.font_path_level_one, 60)
        color_text = (255, 255, 0)
        img = font_type.render(split_text[0], True, color_text)
        rect = img.get_rect()
        rect.center = (pos_x, pos_y)
        window.blit(img, rect)
        pos_y = 60
        img = font_type.render(split_text[1], True, color_text)
        rect = img.get_rect()
        rect.center = (pos_x, pos_y)
        window.blit(img, rect)



    def draw_text_end(self, window, ctr_level_one):

        split_text = ctr_level_one.level_one.store_text_end.split("\n")
        pos_x = 400
        pos_y = 100
        font_type = pygame.font.Font(self.font_path_level_one, 60)
        color_text = (255, 255, 0)
        img = font_type.render(split_text[0], True, color_text)
        rect = img.get_rect()
        rect.center = (pos_x, pos_y)
        window.blit(img, rect)
        pos_y += 60
        img = font_type.render(split_text[1], True, color_text)
        rect = img.get_rect()
        rect.center = (pos_x, pos_y)
        window.blit(img, rect)

    def faded_screen(self, window,ctr_level_one,clock ):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        self.draw_text_end(window ,ctr_level_one)
        pygame.time.delay(500)
        screen_copy = window.copy()
        countdown = 500
        while countdown > 0:
            for alpha in range(0, 255, 20):
                fade.set_alpha(alpha)
                window.blit(screen_copy, (0, 0))
                window.blit(fade, (0, 0))
                ctr_level_one.apply_change_player_status(window, "dead")
                pygame.display.update()
                clock.tick(60)
            for alpha in range(255, 0, 20):
                fade.set_alpha(alpha)
                window.blit(screen_copy, (0, 0))
                window.blit(fade, (0, 0))
                ctr_level_one.apply_change_player_status(window, "dead")
                pygame.display.update()
                clock.tick(60)
            countdown -= 300
        for alpha in range(0, 255, 1):
            fade.set_alpha(alpha)
            window.blit(screen_copy, (0, 0))
            window.blit(fade, (0, 0))
            ctr_level_one.apply_change_player_status(window, "dead")
            pygame.display.update()
            pygame.time.delay(10)
            clock.tick(60)