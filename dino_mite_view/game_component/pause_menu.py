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
        self.panel_w, self.panel_h = 400, 280
        self.panel_x = self.screen_w // 2 - self.panel_w // 2
        self.panel_y = self.screen_h // 2 - self.panel_h // 2

        #Lable
        title_path = os.path.join("./image/menu", "paused_lable.png")
        self.title_image = pygame.image.load(title_path).convert_alpha()
        title_w, title_h = 320, 100
        self.title_image = pygame.transform.scale(self.title_image, (title_w, title_h))

        self.title_x = self.panel_x + (self.panel_w // 2 - title_w //2)
        self.title_y = self.panel_y + 20


        button_w = 250
        button_x = self.screen_w //2 - button_w //2

        self.continue_button = Button("Continue", button_w, 60, button_x, self.panel_y + 110, button_type="continue")
        self.exit_button = Button("Return", button_w, 50, button_x, self.panel_y + 190, button_type="return")

    def draw(self, events):
        logging.info("Doing pause menu")

        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        self.screen.blit(overlay,(0,0))
        #Central panel
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_w, self.panel_h)
        pygame.draw.rect(self.screen, (30,30,30), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (90, 90, 90), panel_rect, width=2, border_radius=12)
       
        #lable
        self.screen.blit(self.title_image, (self.title_x, self.title_y))

        #Buttons
        self.continue_button.update_image(self.screen, events)
        self.exit_button.update_image(self.screen, events)
       
    def handle_click(self, event):
        if self.continue_button.is_clicked(event):
            return "CONTINUE"
        if self.exit_button.is_clicked(event):
            return "RETURN_TO_MENU"
        return None
        


