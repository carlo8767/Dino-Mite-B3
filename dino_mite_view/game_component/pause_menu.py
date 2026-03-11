import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 36)

        # Button rectangles
        self.continue_rect = pygame.Rect(362, 300, 300, 60)
        self.exit_rect = pygame.Rect(362, 400, 300, 60)

    def draw(self):
        # Dark transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Title
        title = self.font_title.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, (430, 200))

        # Continue button
        pygame.draw.rect(self.screen, (70, 130, 70), self.continue_rect, border_radius=8)
        continue_text = self.font_button.render("Continue", True, (255, 255, 255))
        self.screen.blit(continue_text, (430, 315))

        # Exit button
        pygame.draw.rect(self.screen, (130, 70, 70), self.exit_rect, border_radius=8)
        exit_text = self.font_button.render("Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, (410, 415))

    def handle_click(self, mouse_pos):
        if self.continue_rect.collidepoint(mouse_pos):
            return "CONTINUE"
        if self.exit_rect.collidepoint(mouse_pos):
            return "EXIT"
        return None