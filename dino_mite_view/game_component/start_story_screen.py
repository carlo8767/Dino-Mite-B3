import pygame
from dino_mite_view.game_component.button import Button
import os


class Start_Story_Screen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font_title = pygame.font.SysFont("Arial", 20, bold=True)

        # Load background
        try:
            self.image_path = os.path.join("./image", "menu_background.jpeg")
            self.background = pygame.image.load(self.image_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((50, 50, 50))

        try:
            story_file =  "start_story.txt"
            with open (story_file, 'r', encoding='utf-8') as f:
                self.story_text = f.read()
        except FileNotFoundError:
            self.story_text = "file is missing"
        # Create Buttons
        self.skip_story_button = Button("Skip", 200, 60, (self.screen_width // 2) - 100, self.screen_height - 150, (0, 150, 0),
                                        (255, 255, 255), 20)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        line_spacing = 5
        max_width = self.screen_width - 80
        y_pos = 80

        paragraphs = self.story_text.split('\n')
        for paragrap in paragraphs:
            if paragrap.strip() =='':
                y_pos += self.font_title.get_linesize() + line_spacing
                continue

            words = paragrap.split(' ')
            current_line = []

            for word in words:
                line = ' '. join(current_line + [word])
                x, y = self.font_title.size(line)

                if x < max_width:
                    current_line.append(word)
                else:
                    line_surface = self.font_title.render(' '.join(current_line), True, (255, 255, 255))
                    x_pos = (self.screen_width - line_surface.get_width()) // 2
                    self.screen.blit(line_surface, (x_pos, y_pos))

                    y_pos += y + line_spacing
                    current_line = [word]

            if current_line:
                line_surface = self.font_title.render(' '.join(current_line), True, (255, 255, 255))
                x_pos = (self.screen_width - line_surface.get_width()) // 2
                self.screen.blit(line_surface, (x_pos, y_pos))
                y_pos += self.font_title.get_linesize()+line_spacing+10


        self.skip_story_button.draw_function(self.screen)

    def handle_event(self, event):
        if self.skip_story_button.is_clicked(event):
            return "SKIP"
        return None

