import pygame
import os


class CharacterDesign:
    # A reusable class for loading visual states and drawing them.
    def __init__(self, x=0, y=0, scale=1.0, fallback_color=(0, 255, 0), fallback_size=(40, 60)):
        self.x = x
        self.y = y
        self.scale = scale
        self.sprites = {}

        self.current_state = "idle"
        self.facing_right = True

        # Fallback surface if a sprite is missing
        self.fallback_surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
        self.fallback_surface.fill(fallback_color)

    def load_sprites(self, state_to_filepath_map):
        # Maps a state string to an image file path
        # Uses the file's current directory as a base to support Git repositories
        base_dir = os.path.dirname(os.path.abspath(__file__))

        for state, rel_filepath in state_to_filepath_map.items():
            # Create an absolute path from the relative path provided
            abs_filepath = os.path.join(base_dir, rel_filepath)

            if os.path.exists(abs_filepath):
                try:
                    img = pygame.image.load(abs_filepath).convert_alpha()
                    if self.scale != 1.0:
                        new_width = int(img.get_width() * self.scale)
                        new_height = int(img.get_height() * self.scale)
                        img = pygame.transform.scale(img, (new_width, new_height))
                    self.sprites[state] = img
                except pygame.error:
                    pass

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def set_state(self, new_state, facing_right=True):
        self.current_state = new_state
        self.facing_right = facing_right

    def draw(self, surface):
        img = self.sprites.get(self.current_state, self.fallback_surface)

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        rect = img.get_rect()
        rect.midbottom = (self.x, self.y)
        surface.blit(img, rect)


