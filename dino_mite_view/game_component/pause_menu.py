import pygame
from dino_mite_view.game_component.button import Button
import os
import logging

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        self.font = pygame.font.Font(font_path, 42)

        #Central Panel
        self.panel_w, self.panel_h = 280, 240
        self.panel_x = self.screen_w // 2 - self.panel_w // 2
        self.panel_y = self.screen_h // 2 - self.panel_h // 2

        button_w = 220
        button_x = self.panel_x + (self.panel_w - button_w) // 2

        self.continue_button = Button("Continue", button_w, 50, button_x, self.panel_y + 80, (0, 0, 0), (255, 255,255), 35, "green")
        self.exit_button = Button("Return", button_w, 50, button_x, self.panel_y + 150, (0, 0, 0), (255, 255, 255),
                                      35, "red")
    def draw(self):
        logging.info("Doing pause menu")

        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        self.screen.blit(overlay,(0,0))
        #Central panel
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_w, self.panel_h)
        pygame.draw.rect(self.screen, (30,30,30), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (90, 90, 90), panel_rect, width=2, border_radius=12)
        #Title
        title = self.font.render("PAUSED", True, (255,255,255))
        self.screen.blit(title, (self.panel_x + (self.panel_w - title.get_width()) // 2, self.panel_y+20))
        #Buttons
        self.continue_button.draw_function(self.screen)
        self.exit_button.draw_function(self.screen)

    def handle_click(self, event):
        if self.continue_button.is_clicked(event):
            return "CONTINUE"
        if self.exit_button.is_clicked(event):
            return "RETURN_TO_MENU"
        return None

