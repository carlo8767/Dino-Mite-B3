import pygame

"""To create a button you give the following parameters: 
    1. text on the button
    2. width of the button
    3. height of the button
    4. X position on the screen
    5. Y position on the screen

    Then the following parameters are OPTIONAL: color, text_color, font_size, font_type (name of the font)
"""


class Button:
    def __init__(
            self,
            text,
            width,
            height,
            x_pos,
            y_pos,
            color=(100, 100, 100),
            text_color=(255, 255, 255),
            font_size=40,
            font_type="Verdana",
    ):

        self.text = text
        self.color = color
        self.text_color = text_color

        self.font = pygame.font.SysFont(font_type, font_size)
        self.rect = pygame.Rect(x_pos, y_pos, width, height)

        self.text_rendered = self.font.render(self.text, True, self.color)

    def draw_function(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_rendered.get_rect(center=self.rect.center)
        surface.blit(self.text_rendered, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


