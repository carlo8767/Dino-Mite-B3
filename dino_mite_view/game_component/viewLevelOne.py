import pygame
import time
from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_view.game_component.game_over import GameOverMenu
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelOne:

    def __init__(self):
        self.pause_time_resume = 0
        self.start_ticks = pygame.time.get_ticks()
        self.pause_time_total = 0
        self.pause_start = 0
        self.eventually_time = ""
    """
    View component for Level One.
    """


    def draw_screen_level_one(self, window, ctr_levelOne):
        total_seconds = 2 * 60
        ctr_levelOne.init_music()
        """
        Main game loop for Level One.
        Handles events, updates game state via controller, and draws everything.

        :param window: The main pygame display surface.
        :param ctr_levelOne: The ControllerLevelOne instance that manages game logic.
        """
        print(">> Enter in View Level One")
        clock = pygame.time.Clock()
        pygame.display.set_caption(utilities_names.LEVEL_ONE)

        # Load and scale the background image to fill the window
        sprite_image_background = pygame.image.load(
            ctr_levelOne.level_one.image
        ).convert()
        sprite_image_background = pygame.transform.scale(
            sprite_image_background, (WIDTH, HEIGHT)
        )

        # Initialise the pause menu overlay
        pause_menu = PauseMenu(window)
        # initialise game over menu and game_over flag
        game_over_menu = GameOverMenu(window)
        game_over = False

        frame_count = 0
        running = True

        # Register all sprites for collision detection in the controller
        # REMOVE CARLO NOT NECESSARY ALREADY IN THE CONSTRCUTOR
        # ctr_levelOne.add_models_collision()
        while running:
            # Collect events once per frame
            events = pygame.event.get()
            # ==================== EVENT HANDLING ====================
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                # Toggle pause with Escape key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and  not ctr_levelOne.is_paused:
                        self.pause_time_start = pygame.time.get_ticks()
                        ctr_levelOne.toggle_pause()

                    # ADD FOR TIME LOGIC FOR KEEPING THE SAME WHEN RESET
                    elif event.key == pygame.K_ESCAPE and ctr_levelOne.is_paused:
                        # WHEN IT PRESSED
                        pause_duration = pygame.time.get_ticks() - self.pause_time_start
                        self.pause_time_total += pause_duration
                        ctr_levelOne.toggle_pause()

                # Handle clicks on the pause menu buttons (only when paused)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ctr_levelOne.is_paused:
                        # CARLO MOVE IS ANOTHER VIEW ?
                        result = pause_menu.handle_click(pygame.mouse.get_pos())
                        if result == "CONTINUE":
                            ctr_levelOne.toggle_pause()
                            pause_duration = pygame.time.get_ticks() - self.pause_time_start
                            self.pause_time_total += pause_duration
            
              # handle game over menu button clicks
                if game_over:
                    result = game_over_menu.handle_event(event)
                    if result == "RETRY":
                        # reset game state instead of returning, restarts the level
                        ctr_levelOne.init_music()
                        game_over = False
                        time_begins = time.time()         # reset the timer
                        ctr_levelOne.reset_level()        # reset hazards and character position
                    elif result == "RETURNTOMENU":
                        return "MAIN_MENU"

            # ==================== UPDATE (skip when paused) ====================
            # added "and not game_over" so game freezes on game over screen
            if not ctr_levelOne.is_paused and not game_over:
                # Pass raw inputs to the controller, it decides what to do
                keys = pygame.key.get_pressed()
                ctr_levelOne.handle_player_input(keys,events)

                # Controller handles gravity
                # CARLO
                ctr_levelOne.apply_player_gravity()

                # Update hazard positions via the controller # I CAN JUST MOVE THE UPDATE
                ctr_levelOne.update_movement_level_one()

                # Check if the character collides with any hazard
                # NOTE: collision only checks models_collision (Carlo's system).
                # The 5 meteors in ctr_levelOne.meteors are NOT registered there
                collided, name = ctr_levelOne.detection_collision_character(
                    ctr_levelOne.level_one.character
                )
                if collided:
                    # set game_over to True to trigger game over screen
                    print(f"Collision detected with {name} — game over")
                    ctr_levelOne.update_collision_position(name)
                    ctr_levelOne.stop_music()
                    game_over = True

                    # running = False THINK ABOUT ANOHTER LOGIC

                # Reset hazards that have left the screen bounds
                # ctr_levelOne.screen_collision_hazard()

                # CARLO DELETE WHY FRAM COUNT
                # frame_count += 1

            self.calculate_timer(total_seconds, ctr_levelOne.is_paused)
            self.draw_elements(window, ctr_levelOne, sprite_image_background, )

            if ctr_levelOne.is_paused:
                pause_menu.draw()

            # draw game over menu on top of everything when triggered
            if game_over:
                game_over_menu.draw()

            pygame.display.update()
            clock.tick(60)

    def calculate_timer(self, total_seconds, is_paused):
        if not is_paused:
            elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.pause_time_total
            remaining_seconds = max(0, total_seconds - elapsed_ms // 1000)
            mins, secs = divmod(remaining_seconds, 60)
            timer_text = f"Time to jump: {mins:02d}:{secs:02d}"
            self.eventually_time = timer_text

    def draw_elements(self, window, ctr_levelOne,sprite_image_background ):
            # ==================== DRAW ====================
            # Background
            window.blit(sprite_image_background, (0, 0))

            # Character draw various images  CARLO
            ctr_levelOne.level_one.character.draw(window)

            # Draw the original single hazard instances from the LevelOne model
            window.blit(
                ctr_levelOne.level_one.hazard_meteor.image_loaded,
                ctr_levelOne.level_one.hazard_meteor.rect,
            )
            window.blit(
                ctr_levelOne.level_one.hazard_meteorOne.image_loaded,
                ctr_levelOne.level_one.hazard_meteorOne.rect,
            )
            window.blit(
                ctr_levelOne.level_one.hazard_meteorTwo.image_loaded,
                ctr_levelOne.level_one.hazard_meteorTwo.rect,
            )

            window.blit(
                ctr_levelOne.level_one.hazard_rollingRock.image_loaded,
                ctr_levelOne.level_one.hazard_rollingRock.rect,
            )
            # ==================== DRAW  TIMER ====================
            FONT_TYPE = pygame.font.SysFont("Comic Sans MS", 40)
            color_timer = (0, 0, 0)
            img = FONT_TYPE.render(self.eventually_time, True, color_timer)
            rect = img.get_rect()
            rect.center = (400, 20)
            pygame.draw.rect(window, (0, 0, 0), rect, 2)
            window.blit(img, rect)

            # Draw all 5 meteors from the controller's meteor list.
            # These are separate from hazard_meteor above.
            # Collision for these is NOT wired up yet — that is for
            # Carlo to add to models_collision when ready.
            # MOVE IN CONTROLLER VIEW DOES NOT INTERACT WITH THTE CARLO VIEW!

            #  CARLO
           # self.draw_multiple_rock(ctr_levelOne,window)
            # Pause overlay drawn last so it sits on top of everything

    # ELIMINATE CARLO NOT NECESSARY
    def draw_multiple_rock (self, ctr_levelOne, window):
            for meteor in ctr_levelOne.meteors:
              window.blit(meteor.image_loaded, meteor.rect)

                # Draw any active rolling rocks from the controller's list
            #for rock in ctr_levelOne.rolling_rocks:
             #   window.blit(rock.image_loaded, rock.rect)

