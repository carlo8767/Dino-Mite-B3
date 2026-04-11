import pygame
import os

"""To create a button you give the following parameters: 
    1. text on the button
    2. width of the button
    3. height of the button
    4. X position on the screen
    5. Y position on the screen

    Then the following parameters are OPTIONAL: color, text_color, font_size, "green"/"red" (if using texture) font_path/name (name of the font)
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
            red_green = "green",
            font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
            
    ):
        if red_green == "green":
            self.button_fone = os.path.join("./image", "button_green.png")
        else:
            self.button_fone = os.path.join("./image", "button_red.png")

        self.text = text
        self.color = color
        self.text_color = text_color

        self.font = pygame.font.Font(font_path, font_size)
        self.rect = pygame.Rect(x_pos, y_pos, width, height)

        self.text_rendered = self.font.render(self.text, True, self.text_color)

        image_button = pygame.image.load(self.button_fone).convert_alpha()
        self.fone = pygame.transform.scale(image_button, (width, height))

    def draw_function(self, surface):
        if self.fone:
            surface.blit(self.fone, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_rect = self.text_rendered.get_rect(center=self.rect.center)
        surface.blit(self.text_rendered, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


