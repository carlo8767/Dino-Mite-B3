import pygame
import os

"""To create a button you give the following parameters: 
    1. text on the button
    2. width of the button
    3. height of the button
    4. X position on the screen
    5. Y position on the screen

    Then the following parameters are OPTIONAL: 
    button_type: "normal", "continue", "return", "restart"
"""


class Button:
    def __init__(
            self,
            text,
            width,
            height,
            x_pos,
            y_pos,
            text_color=(255, 255, 255),
            font_size=40,
            button_type = "normal",
            font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")

    ):

        self.text = text
        self.text_color = text_color
        self.button_type = button_type

        self.width = width
        self.height = height

        self.font = pygame.font.Font(font_path, font_size)
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.text_rendered = self.font.render(self.text, True, self.text_color)

        name_start = button_type if button_type in ("continue", "return", "restart") else "button"
        self.normal_image = self.load_image(os.path.join("./image/menu", f"{name_start}_normal.png"))
        self.halt_image = self.load_image(os.path.join("./image/menu", f"{name_start}_halt.png"))
        self.clicked_image = self.load_image(os.path.join("./image/menu", f"{name_start}_clicked.png"))


        self.is_halt = False
        self._is_clicked = False
        self._click_time = 0
        self._click_dur = 270

    def update_image(self, surface, events):
        mouse = pygame.mouse.get_pos()
        self.is_halt = self.rect.collidepoint(mouse)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_halt:
                    self._is_clicked = True
                    self._click_time = pygame.time.get_ticks()
        if self._is_clicked and pygame.time.get_ticks() - self._click_time >= self._click_dur:
            self._is_clicked = False
        self.draw_function(surface)

    def draw_function(self, surface):
        if self._is_clicked:
            button_image = self.clicked_image
        elif self.is_halt:
            button_image = self.halt_image
        else:
            button_image = self.normal_image

        surface.blit(button_image, self.rect)
        if self.button_type == "normal":
            text_rect = self.text_rendered.get_rect(center=self.rect.center)
            surface.blit(self.text_rendered, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


    def load_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))
        return image