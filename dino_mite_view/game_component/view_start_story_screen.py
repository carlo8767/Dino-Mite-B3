import pygame
from dino_mite_view.game_component.button import Button
import os
from dino_mite_utility.utilities_names import WIDTH, HEIGHT

class ViewStartStoryScreen:

    def __init__(self):
        self.store_text = self.upload_file()
        self.width_int =  WIDTH
        self.height_int = HEIGHT
        self.font_title = pygame.font.SysFont("Arial", 20, bold=True)
        self.story_text  = self.store_text
        # Load background
        self.image_path = os.path.join("./image", "menu_background.jpeg")
        self.background = pygame.image.load(self.image_path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((50, 50, 50))

        # Create Buttons
        self.skip_story_button = Button("Skip", 200, 60, (self.width_int // 2) - 100, self.height_int - 150, (0, 150, 0),
                                        (255, 255, 255), 20)

    def draw_story_screen(self, screen):

        fps = pygame.time.Clock()
        split_text = self.story_text.split("\n")
        pos_x = 400
        pos_y = 30
        text_font = pygame.font.SysFont("Comic Sans MS", 30)
        color_timer = (0, 0, 0)
        screen.blit(self.background, (0, 0))
        while True:
            for event in pygame.event.get():
                    if self.skip_story_button.is_clicked(event):
                        return "MAIN_MENU"
            for ns in split_text:
                # SEE HOW TO WAIT TO RENDER THE TEXT
                img = text_font.render(ns, True, color_timer)
                rect = img.get_rect()
                rect.center = (pos_x, pos_y)
                screen.blit(img, rect)
                pos_y += 40
                split_text.pop(0)
                pygame.time.delay(2500)
                break
            self.skip_story_button.draw_function(screen)
            pygame.display.update()
            fps.tick(60)

    def upload_file(self):
        try:
            content  = ""
            os_path  = os.path.join("./text_files", "start_story.txt")
            with open(os_path, 'r', encoding='utf-8') as f:
                content+= f.read()
        except FileNotFoundError:
            content = "file is missing"
        return content





