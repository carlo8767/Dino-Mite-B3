import random
import pygame
from dino_mite_view.game_component.pause_menu import PauseMenu
from dino_mite_utility import utilities_names

class ViewLevelOne:

    dict_elements_view = dict()

    def draw_screen_level_one(self, window, ctr_levelOne):
        print(">> Enter in View Level One")
        clock = pygame.time.Clock()
        pygame.display.set_caption(utilities_names.LEVEL_ONE)

        sprite_image_background = pygame.image.load(
            ctr_levelOne.level_one.image
        ).convert()

        pause_menu = PauseMenu(window)
        frame_count = 0
        running = True

        while running:
            # --- EVENTS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        ctr_levelOne.toggle_pause()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ctr_levelOne.is_paused:
                        result = pause_menu.handle_click(pygame.mouse.get_pos())
                        if result == "CONTINUE":
                            ctr_levelOne.toggle_pause()
                        if result == "EXIT":
                            running = False  # back to main menu

            # --- UPDATE (only when not paused) ---
            if not ctr_levelOne.is_paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    ctr_levelOne.movement_character_left()
                elif keys[pygame.K_RIGHT]:
                    ctr_levelOne.movement_character_right()

                # Spawn rolling rock every 1-2 minutes (randomly between 3600-7200 frames)
                if not hasattr(self, 'next_rock_spawn'):
                    self.next_rock_spawn = random.randint(3600, 7200)

                if frame_count == self.next_rock_spawn:
                    ctr_levelOne.spawn_rolling_rock()
                    self.next_rock_spawn = frame_count + random.randint(3600, 7200)

                # No meteor spawning needed - 5 are pre-spawned and loop forever

                # Update all hazards
                ctr_levelOne.update_level_one()

                # Collision detection
                for hazard in ctr_levelOne.meteors + ctr_levelOne.rolling_rocks:
                    if ctr_levelOne.detection_collision_character(
                        ctr_levelOne.level_one.character, hazard
                    ):
                        print("collision - game over")
                        running = False

                # Screen collision for hazards
                ctr_levelOne.screen_collision_hazard()

                frame_count += 1

            # --- DRAW ---
            window.blit(sprite_image_background, (0, 0))

            # Draw character
            window.blit(
                ctr_levelOne.level_one.character.image_loaded,
                ctr_levelOne.level_one.character.rect
            )

            # Draw all meteors
            for meteor in ctr_levelOne.meteors:
                window.blit(meteor.image_loaded, meteor.rect)

            # Draw all rolling rocks
            for rock in ctr_levelOne.rolling_rocks:
                window.blit(rock.image_loaded, rock.rectangle)

            # Draw pause menu on top if paused
            if ctr_levelOne.is_paused:
                pause_menu.draw()

            pygame.display.update()
            clock.tick(60)