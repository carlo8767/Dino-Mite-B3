import logging

import pygame
from dino_mite_view.game_component.button import Button
import os

class View_MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        self.font_title = pygame.font.Font(font_path, 60)
        # Load background
        try:
            self.image_path = os.path.join("./image", "menu", "story_background.png")
            self.background = pygame.image.load(self.image_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 50))

        # Create Buttons
        self.one_player_button = Button("One Player", 200, 60, (self.screen_width // 2) - 100, 340)
        self.two_players_button = Button("Two Players", 200, 60, (self.screen_width // 2) - 100, 410)
        self.rules_button = Button("Game Rules", 200, 60, (self.screen_width // 2) - 100, 480)
        self.exit_button = Button("Exit", 200, 60, (self.screen_width // 2) - 100, 550)

        # --- TEMP TEST BUTTONS (remove before release) ---
        self.test_level2_button = Button("Test Level 2", 180, 45, (self.screen_width // 2) - 195, 650)
        self.test_level3_button = Button("Test Level 3", 180, 45, (self.screen_width // 2) + 15,  650)
        # --------------------------------------------------

    def draw_start_menu(self):
        logging.info("Enter in view start menu")
        fps = pygame.time.Clock()
        self.screen.blit(self.background, (0, 0))

        #title = self.font_title.render("Welcome to Dino-Mite!", True, (0, 0, 0))
        #self.screen.blit(title, (150, 100))

        logo_path = os.path.join("./image", "menu", "Dino-Mite_logo.png")
        logo_image = pygame.image.load(logo_path).convert_alpha()
        logo_image = pygame.transform.scale(logo_image, (350, 350))
        self.screen.blit(logo_image, (self.screen_width//2 - logo_image.get_width() //2, 10))

        while True:
            events = pygame.event.get()
            self.one_player_button.update_image(self.screen, events)
            self.two_players_button.update_image(self.screen, events)
            self.exit_button.update_image(self.screen, events)
            self.rules_button.update_image(self.screen, events)
            # --- TEMP TEST BUTTONS (remove before release) ---
            self.test_level2_button.update_image(self.screen, events)
            self.test_level3_button.update_image(self.screen, events)

            for event in events:
                if self.one_player_button.is_clicked(event):
                    return "LEVEL_ONE"
                if self.exit_button.is_clicked(event):
                    return "EXIT"
                if self.rules_button.is_clicked(event):
                    return "RULES"
                # --- TEMP TEST BUTTONS (remove before release) ---
                if self.test_level2_button.is_clicked(event):
                    return "LEVEL_TWO"
                if self.test_level3_button.is_clicked(event):
                    return "LEVEL_THREE"
                if self.two_players_button.is_clicked(event):
                    return "TWO PLAYERS"
            # --------------------------------------------------
            pygame.display.update()
            fps.tick(60)



