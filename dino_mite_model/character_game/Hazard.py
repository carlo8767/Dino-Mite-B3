import os.path

import pygame
import random


class Meteor():


    def __init__(self):
        self.position_x = 400
        self.position_y = 2
        self.speed = 3
        self.image_meteor = os.path.join("./image", "meteor.jpeg")
        self.image_loaded = pygame.image.load(self.image_meteor).convert()
        self.rectangle = self.image_loaded.get_rect()
        self.rectangle.center = (self.position_x, self.position_y)


    def update_positions(self, x, y):
        self.position = (x, y)

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

class RollingRock():
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

        # MOVEMENT VALUES
        self.move_x = 4   # rolls left to right
        self.move_y = 0   # does not move vertically

        # POSITION
        # Starts just off the left edge of the screen.
        self.position_x = -80
        self.position_y = 680

        # SCREEN WIDTH
        # When the rock passes this x value, it resets to the left.
        self.screen_width = 1024

        # IMAGE LOADING
        # convert_alpha() preserves the transparent PNG background
        # so there is no ugly box around the rock.
        self.image_rock_path = os.path.join("./image", "rolling_rock.png")

        self.image_loaded = pygame.image.load(
            self.image_rock_path
        ).convert_alpha()

        self.image_loaded = pygame.transform.scale(
            self.image_loaded,
            (80, 80)   # width, height in pixels 
        )

        # RECTANGLE
        self.rectangle = self.image_loaded.get_rect()

        self.rectangle.center = (
            self.position_x,
            self.position_y
        )

    def update_position(self):
        """
        Moves the rock right by move_x pixels every frame.
        When it exits the right edge, it resets to the left.
        """

        self.rectangle.x += self.move_x

        # Reset to left side when rock exits the right side
        if self.rectangle.left > self.screen_width:
            self.kill()

    def kill(self):
        self.is_active = False 


    

