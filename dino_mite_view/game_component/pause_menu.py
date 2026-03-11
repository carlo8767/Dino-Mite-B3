import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 24)

    def draw(self):
        screen_w, screen_h = self.screen.get_size()

        # Dark Transparent Background
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Central Panel 
        panel_w, panel_h = 260, 220
        panel_x = screen_w // 2 - panel_w // 2
        panel_y = screen_h // 2 - panel_h // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (30, 30, 30, 200), panel_rect, border_radius=12) 
        pygame.draw.rect(self.screen, (80, 80, 80), panel_rect, width=2, border_radius=12)

        # Title centered in panel
        title = self.font_title.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, (
            panel_x + (panel_w - title.get_width()) // 2,
            panel_y + 20
        ))

        # Buttons
        btn_w, btn_h = 180, 45
        btn_x = panel_x + (panel_w - btn_w) // 2
        self.continue_rect = pygame.Rect(btn_x, panel_y + 85, btn_w, btn_h)
        self.exit_rect = pygame.Rect(btn_x, panel_y + 145, btn_w, btn_h)

        pygame.draw.rect(self.screen, (40, 160, 40), self.continue_rect, border_radius=8)
        self._draw_centered_text("Continue", self.continue_rect)

        pygame.draw.rect(self.screen, (190, 45, 45), self.exit_rect, border_radius=8)
        self._draw_centered_text("Exit", self.exit_rect)

    def _draw_centered_text(self, text, rect):
        surface = self.font_button.render(text, True, (255, 255, 255))
        x = rect.x + (rect.width - surface.get_width()) // 2
        y = rect.y + (rect.height - surface.get_height()) // 2
        self.screen.blit(surface, (x, y))

    def handle_click(self, mouse_pos):
        if self.continue_rect.collidepoint(mouse_pos):
            return "CONTINUE"
        if self.exit_rect.collidepoint(mouse_pos):
            return "EXIT"
        return None