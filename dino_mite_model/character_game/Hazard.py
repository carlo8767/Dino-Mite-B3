import os.path

import pygame
import random

from dino_mite_utility.utilities_names import WIDTH, HEIGHT
class Meteor(pygame.sprite.Sprite):
    """The meteor spawns with the random X position at the very top of the screen and falls down\n"
    "vertically with the set speed"""

    def __init__(self):
        super().__init__()
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.position_x = random.randint(50, self.screen_width - 50)
        self.position_y = -60
        self.speed = 4
        self.is_active = True
        self.image_path = os.path.join("./image", "meteor.png")
        self.image_loaded = pygame.image.load(self.image_path).convert_alpha()
        self.image_loaded = pygame.transform.scale(self.image_loaded, (60, 60))
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.name = "Hazard"

    """ Moves the meteor from top os the screen to the bottom"""
    def update_positions(self, meteor):
        meteor.rect.y += meteor.speed

    """
        # CHANGE WITH REALISTIC VALUES
        def _init_(self, screen_width):
        super()._init_()
        self.image = pygame.Surface((10, 10))  # replace with avatar later
        self.image.fill((0, 0, 0))

        x = random.randint(50, screen_width - 50)
        self.rect = self.image.get_rect(topleft=(x, 0))

        self.speed = 3 #can be also randomised. Will be adjusted later on
        def move(self):
            self.rect.y += self.speed
    """
 
class RollingRock(pygame.sprite.Sprite):
    """
    HOW A ROLLING ROCK MOVES:
    The rock rolls from left to right across the bottom of the screen.
    When it exits the right side, it resets back to the left side.
    This creates a looping hazard the player must avoid.

    HOW TO USE THIS:
    # In the controller or game component:
    from dino_mite_model.level_model.rolling_rock import RollingRock

    rock = RollingRock()

    # Game loop:
    rock.update_position()                          # moves it
    window.blit(rock.image_loaded, rock.rectangle)  # draws it
    # Collision dev uses: rock.rectangle
    """
    def __init__(self):
        super().__init__()
        self.move_x = 4
        self.move_y = 0
        self.position_x = -80
        self.position_y = 680
        self.screen_width = WIDTH
        self.is_active = True  # ADD THIS
        self.name = "RollingRock"  # ADD THIS

        self.image_rock_path = os.path.join("./image", "rolling_rock.png")
        self.image_loaded = pygame.image.load(self.image_rock_path).convert_alpha()
        self.image_loaded = pygame.transform.scale(self.image_loaded, (80, 80))
        self.rectangle = self.image_loaded.get_rect()
        self.rectangle.center = (self.position_x, self.position_y)

    def update_position(self):
        self.rectangle.x += self.move_x
        if self.rectangle.left > self.screen_width:
            self.is_active = False  # CHANGED from kill() to match Meteor pattern

