import pygame
from IPython.utils.timing import clock

from dino_mite_utility.utilities_names import LEVEL_ONE


class ViewGameOverMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 24)
        self.running = True


    def init_game_over(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.play_again_rect.collidepoint(pygame.mouse.get_pos()):
                            return "DRAW_LEVEL_ONE"
                        if self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                            return "MAIN_MENU"
            self.draw_game_over()
            pygame.display.update()
            clock.tick(60)


    def draw_game_over(self):
        screen_w, screen_h = self.screen.get_size()

        # Dark transparent overlay
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Central panel
        panel_w, panel_h = 400, 260
        panel_x = screen_w // 2 - panel_w // 2
        panel_y = screen_h // 2 - panel_h // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, (80, 80, 80), panel_rect, width=2, border_radius=12)

        # Title centered in panel
        title = self.font_title.render("GAME OVER", True, (220, 40, 40))
        self.screen.blit(title, (
            panel_x + (panel_w - title.get_width()) // 2,
            panel_y + 20
        ))

        # Buttons positioned relative to panel_y just like pause_menu.py
        btn_w, btn_h = 220, 45
        btn_x = panel_x + (panel_w - btn_w) // 2
        self.play_again_rect = pygame.Rect(btn_x, panel_y + 120, btn_w, btn_h)
        self.menu_rect = pygame.Rect(btn_x, panel_y + 185, btn_w, btn_h)

        pygame.draw.rect(self.screen, (40, 160, 40), self.play_again_rect, border_radius=8)
        self._draw_centered_text("Play Again", self.play_again_rect)

        pygame.draw.rect(self.screen, (190, 45, 45), self.menu_rect, border_radius=8)
        self._draw_centered_text("Return to Menu", self.menu_rect)

    def _draw_centered_text(self, text, rect):
        surface = self.font_button.render(text, True, (255, 255, 255))
        x = rect.x + (rect.width - surface.get_width()) // 2
        y = rect.y + (rect.height - surface.get_height()) // 2
        self.screen.blit(surface, (x, y))

