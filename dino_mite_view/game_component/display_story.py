import logging

import pygame
from dino_mite_view.game_component.button import Button
import os
from dino_mite_utility.utilities_names import WIDTH, HEIGHT

class ViewDisplayStory:

    STORY_FILES = {
        1: "start_story.txt",
        2: "transition_level1_to_2.txt",
        3: "transition_level2_to_3.txt",
        4: "story_success.txt",
        5: "story_failure.txt",
    }

    def __init__(self, story_part=1, next_state="MAIN_MENU"):
        self.story_part = story_part
        self.next_state = next_state
        self.store_text = self.upload_file()
        self.width_int =  WIDTH
        self.height_int = HEIGHT
        self.story_text  = self.store_text
        # Load background
        try:
            self.image_path = os.path.join("./image/menu", "story_background.png")
            self.background = pygame.image.load(self.image_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except OSError:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((50, 50, 50))

        # Create Buttons — "Play Again" for the final success story, "Go" otherwise
        button_text = "Play Again" if self.story_part == 4 else "Go"
        self.skip_story_button = Button(button_text, 200, 60, (self.width_int // 2) - 100, self.height_int - 130)

    def draw_story_screen(self, screen):
        logging.info("Enter in view story screen")
        fps = pygame.time.Clock()
        split_text = self.story_text.split("\n")
        pos_x = 400
        pos_y = 50
        font_path = os.path.join("./fonts", "Jersey10-Regular.ttf")
        try:
            text_font = pygame.font.Font(font_path, 30)
        except FileNotFoundError:
            text_font = pygame.font.SysFont("Comic Sans MS", 30)

        color_timer = (0, 0, 0)
        screen.blit(self.background, (0, 0))
        self.skip_story_button.draw_function(screen)
        pygame.display.update()
        index = 0
        prev_line_time = pygame.time.get_ticks()

        while True:
            events = pygame.event.get()

            for event in events:
                if self.skip_story_button.is_clicked(event):
                    return self.next_state

            current_time = pygame.time.get_ticks()
            if index < len(split_text) and (current_time - prev_line_time) >= 1500:
                ns = split_text[index]
                img = text_font.render(ns, True, color_timer)
                rect = img.get_rect()
                rect.center = (pos_x, pos_y)
                screen.blit(img, rect)
                pos_y += 40
                index += 1
                prev_line_time = current_time

            self.skip_story_button.update_image(screen, events)
            
            pygame.display.update()
            fps.tick(60)

    def upload_file(self):
        try:
            content  = ""
            filename = self.STORY_FILES.get(self.story_part, "start_story.txt")
            os_path  = os.path.join("./text_files", filename)
            with open(os_path, 'r', encoding='utf-8') as f:
                content+= f.read()
        except FileNotFoundError:
            content = "file is missing"
        return content





