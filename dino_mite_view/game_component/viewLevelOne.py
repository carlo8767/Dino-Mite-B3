import pygame
import time
from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelOne:
    """
    View component for Level One.
    """


    def draw_screen_level_one(self, window, ctr_levelOne):

        FONT_TYPE = pygame.font.SysFont("Comic Sans MS", 40)
        color_timer = (0, 0, 0)
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
        frame_count = 0
        running = True

        # Register all sprites for collision detection in the controller
        # REMOVE CARLO NOT NECESSARY ALREADY IN THE CONSTRCUTOR
        # ctr_levelOne.add_models_collision()
        # TIME
        time_begins = time.time()
        duration = 200
        while running:
            # TIME
            remaining = int(duration - (time.time() - time_begins))
            print(remaining)
            if remaining <=0:
                print("NEXT LEVEL")
            # Collect events once per frame
            events = pygame.event.get()
            # ==================== EVENT HANDLING ====================
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                # Toggle pause with Escape key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        ctr_levelOne.toggle_pause()

                # Handle clicks on the pause menu buttons (only when paused)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ctr_levelOne.is_paused:
                        # CARLO MOVE IS ANOTHER VIEW ?
                        result = pause_menu.handle_click(pygame.mouse.get_pos())
                        if result == "CONTINUE":
                            ctr_levelOne.toggle_pause()
                        elif result == "EXIT":
                            running = False

            # ==================== UPDATE (skip when paused) ====================
            if not ctr_levelOne.is_paused:
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
                    # HERE THE ISSUE !!!
                    print(f"Collision detected with {name} — game over")
                    ctr_levelOne.update_collision_position(name)
                    # running = False THINK ABOUT ANOHTER LOGIC

                # Reset hazards that have left the screen bounds
                # ctr_levelOne.screen_collision_hazard()

                # CARLO DELETE WHY FRAM COUNT
                # frame_count += 1
            self.draw_elements(window, ctr_levelOne,sprite_image_background)

            if ctr_levelOne.is_paused:
                pause_menu.draw()


            time_left = "TIME LEFT "+str(remaining)
            self.draw_timer(time_left,FONT_TYPE, color_timer, 400, 50, window)
            pygame.display.update()
            clock.tick(60)

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


    def draw_timer(self, text, font, text_color, x_pos, y_pos, window):
        img = font.render(text, True, text_color)
        rect = img.get_rect()
        rect.center = (x_pos, y_pos)
        pygame.draw.rect(window, (0, 0, 0), rect, 2)
        window.blit(img, rect)






















    def handle_key_input(self, keys, events):
        # Check key press for JUMP
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.png_on_ground:
                    self.speed_y = -15  # Launch upward
                    self.game_state = "jump"

        # Check which keys are pressed
        # Move the png accordingly
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.game_state = "walk_left"   # A = Walk left

        elif keys[pygame.K_d]:
            self.rect.x += 5
            self.game_state = "walk_right"  # D = Walk right

        elif keys[pygame.K_s]:
            self.game_state = "duck"        # S = Duck
            self.rect.height = self.duck_height
            self.rect.y = self.constant_ground - self.duck_height  # Crouch at ground level

        elif self.png_on_ground and self.game_state != "jump":
            self.game_state = "idle"        # Nothing pressed, stay idle
            self.rect.height = self.standing_height # Restore when standing


