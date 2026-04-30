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
            self.text_font = pygame.font.Font(self.font_path, 25)
        except:
            self.text_font = pygame.font.SysFont("Arial", 25, True)
        try:
            self.image_path = os.path.join("./image/menu", "story_background.png")
            self.background = pygame.image.load(self.image_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((50, 50, 50))


        powerup_time_image_path = os.path.join("./image/bubble", "ExtraTimeIcon.png")
        self.powerup_time_image = pygame.image.load(powerup_time_image_path).convert_alpha()
        self.powerup_time_image = pygame.transform.scale( self.powerup_time_image, (70, 70))

        powerup_velocity_path = os.path.join("./image/bubble", "ReducedVelocityIcon.png")
        self.powerup_velocity_image = pygame.image.load(powerup_velocity_path).convert_alpha()
        self.powerup_velocity_image = pygame.transform.scale(self.powerup_velocity_image, (70, 70))

        powerup_shield_path = os.path.join("./image/bubble", "ShieldBubbleIcon.png")
        self.powerup_shield_image = pygame.image.load(powerup_shield_path).convert_alpha()
        self.powerup_shield_image = pygame.transform.scale(self.powerup_shield_image, (70,70))

        # Create Buttons
        self.go_back_button = Button("Back", 200, 60, (self.width_int // 2) - 100, self.height_int - 130)

        self.powerups = [self.powerup_time_image, self.powerup_velocity_image, self.powerup_shield_image]
    def draw_rules_screen(self, screen):
        logging.info("Enter in rules screen")

        split_text = self.rules_text.splitlines()
        pos_x = 100
        pos_y = 60
        heading = True
        color_timer = (0, 0, 0)

        screen.blit(self.background, (0, 0))

        for ns in split_text:

            if ns.startswith ("PU"):
                line = ns[2:]
                img = self.text_font.render(line, True, color_timer)
                rect = img.get_rect()
                rect.midleft = (200, pos_y)
            else:
                img = self.text_font.render(ns, True, color_timer)
                rect = img.get_rect()
                rect.midleft = (pos_x, pos_y)
            screen.blit(img, rect)

            if heading == True:
                pos_y += 50
                heading = False
            elif ns.startswith ("PU"):
                pos_y += 90
            else:
                pos_y += 25

        left_margine = 100
        y_pos = 360
        gap = 85

        for y, powerup in enumerate(self.powerups):
            image_y_pos = y_pos + y * gap
            screen.blit(powerup, (left_margine, image_y_pos))

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
