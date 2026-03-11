import pygame
import sys
from dino_mite_view.game_component.button import Button

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Load background
        try:
            self.background = pygame.image.load("background.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 50))

        # Create Buttons
        self.start_button = Button("Start", 200, 60, (self.screen_width // 2) - 100, 250)
        self.exit_button = Button("Exit", 200, 60, (self.screen_width // 2) - 100, 350)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.start_button.draw_function(self.screen)
        self.exit_button.draw_function(self.screen)

    def handle_event(self, event):
        if self.start_button.is_clicked(event):
            return "START"
        if self.exit_button.is_clicked(event):
            return "EXIT"
        return None

