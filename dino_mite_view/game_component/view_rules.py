import logging

import pygame
from dino_mite_view.game_component.button import Button
import os
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class ViewRules:
    def __init__(self):
        self.rules_text = self.upload_file()
        self.width_int = WIDTH
        self.height_int = HEIGHT
        self.font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        try:
            self.text_font = pygame.font.Font(self.font_path, 30)
        except:
            self.text_font = pygame.font.SysFont("Arial", 30, True)
        try:
            self.image_path = os.path.join("./image/menu", "story_background.png")
            self.background = pygame.image.load(self.image_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((50, 50, 50))

        # Create Buttons
        self.go_back_button = Button("Back", 200, 60, (self.width_int // 2) - 100, self.height_int - 130, (0, 150, 0),
                                        (255, 255, 255), 30, "green")

    def draw_rules_screen(self, screen):
        logging.info("Enter in rules screen")

        split_text = self.rules_text.splitlines()
        pos_x = 400
        pos_y = 100
        heading = True
        color_timer = (0, 0, 0)

        screen.blit(self.background, (0, 0))

        for ns in split_text:
            img = self.text_font.render(ns, True, color_timer)
            rect = img.get_rect()
            rect.center = (pos_x, pos_y)
            screen.blit(img, rect)

            if heading == True:
                pos_y += 80
                heading = False
            else:
                pos_y += 40

        self.go_back_button.draw_function(screen)


    def handle_click(self,event):
   
        if self.go_back_button.is_clicked(event):
            return "MAIN_MENU"
        return "RULES"
    
    def upload_file(self):
        try:
            content = ""
            os_path = os.path.join("./text_files", "rules.txt")
            with open(os_path, 'r', encoding='utf-8') as f:
                content += f.read()
        except FileNotFoundError:
            content = "file is missing"
        return content
