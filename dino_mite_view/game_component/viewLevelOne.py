import pygame
from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility import utilities_names
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewLevelOne:
    """
    View component for Level One.
    """

    dict_elements_view = dict()

    def draw_screen_level_one(self, window, ctr_levelOne):
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
        ctr_levelOne.add_models_collision()

        while running:
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
                ctr_levelOne.apply_player_gravity()

                # Update hazard positions via the controller
                ctr_levelOne.update_level_one()

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
                    running = False

                # Reset hazards that have left the screen bounds
                ctr_levelOne.screen_collision_hazard()

                frame_count += 1

            # ==================== DRAW ====================
            # Background
            window.blit(sprite_image_background, (0, 0))

            # Character
            ctr_levelOne.level_one.character.player_movement.draw(window)

            # Draw the original single hazard instances from the LevelOne model
            window.blit(
                ctr_levelOne.level_one.hazard_meteor.image_loaded,
                ctr_levelOne.level_one.hazard_meteor.rect,
            )
            window.blit(
                ctr_levelOne.level_one.hazard_rollingRock.image_loaded,
                ctr_levelOne.level_one.hazard_rollingRock.rect,
            )

            # Draw all 5 meteors from the controller's meteor list.
            # These are separate from hazard_meteor above.
            # Collision for these is NOT wired up yet — that is for
            # Carlo to add to models_collision when ready.
            for meteor in ctr_levelOne.meteors:
                window.blit(meteor.image_loaded, meteor.rect)

            # Draw any active rolling rocks from the controller's list
            for rock in ctr_levelOne.rolling_rocks:
                window.blit(rock.image_loaded, rock.rect)

            # Pause overlay drawn last so it sits on top of everything
            if ctr_levelOne.is_paused:
                pause_menu.draw()

            pygame.display.update()
            clock.tick(60)
