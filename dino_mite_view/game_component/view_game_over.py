import logging
import pygame
import os
from dino_mite_view.game_component.button import Button

class ViewGameOverMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        try:
            self.font = pygame.font.Font(font_path, 42)
        except OSError:
            self.font = pygame.font.SysFont("Arial", 42, bold=True)
        self.panel_w, self.panel_h = 400, 280
        self.panel_x = self.screen_w // 2 - self.panel_w // 2
        self.panel_y = self.screen_h // 2 - self.panel_h // 2

        #Buttons
        button_w = 220
        button_x = self.screen_w // 2 - button_w // 2

         #Lable
        title_path = os.path.join("./image/menu", "game_over_lable.png")
        self.title_image = pygame.image.load(title_path).convert_alpha()
        title_w, title_h = 320, 100
        self.title_image = pygame.transform.scale(self.title_image, (title_w, title_h))

        self.title_x = self.panel_x + (self.panel_w // 2 - title_w //2)
        self.title_y = self.panel_y + 20


        self.play_again_button = Button(
            "Play Again", button_w, 50, button_x, self.panel_y + 110, button_type= "restart"
        )

        self.exit_button = Button(
            "Return", button_w, 50, button_x, self.panel_y + 190, button_type= "return"
        )
        self.running = True


    def init_game_over(self, active_player_player_two):
        logging.info(f'init game over ')
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.play_again_button.is_clicked(event) and not active_player_player_two:
                            pygame.mixer.music.stop()
                            return "LEVEL_ONE"
                        if self.play_again_button.is_clicked(event) and active_player_player_two:
                            pygame.mixer.music.stop()
                            return "TWO PLAYERS"
                        if self.exit_button.is_clicked(event):
                            pygame.mixer.music.stop()
                            return "MAIN_MENU"
            self.draw_game_over(events)
            pygame.display.update()
            clock.tick(60)

    def draw_game_over(self, events):
        logging.info("Draw game over")
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_w, self.panel_h)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (90, 90, 90), panel_rect, width=2, border_radius=12)

          #lable
        self.screen.blit(self.title_image, (self.title_x, self.title_y))

        self.play_again_button.update_image(self.screen, events)
        self.exit_button.update_image(self.screen, events)


