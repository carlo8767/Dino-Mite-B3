import os.path

import pygame
import random

from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class VerticalHazard(pygame.sprite.Sprite):
    """
    Base class for hazards that fall vertically from the top of the screen.

    Subclasses must define as class attributes:
        image_path (str): path to the hazard image
        name       (str): identifier used by the collision system
        _speed     (int): fall speed in pixels per frame

    Subclasses may override update_position() to add horizontal drift.
    """

    image_path: str = None
    name: str = "VerticalHazard"
    _speed: int = 6
    size: tuple = (120, 120)

    def __init__(self):
        super().__init__()
        self.speed = self._speed  # instance copy so slowdown powerup can modify it
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(), self.size
        )
        self.rect = self.image_loaded.get_rect()
        self.mask = pygame.mask.from_surface(self.image_loaded)
        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60
        self.rect.center = (self.position_x, self.position_y)
        self.is_active = True

    def update_position(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self._reset()

    def _reset(self):
        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60
        self.rect.center = (self.position_x, self.position_y)
        self.is_active = True

    def update_position_collision(self):
        self._reset()

    def get_current_position(self):
        return self.rect.x, self.rect.y


class Meteor(VerticalHazard):
    """Level 1 hazard. Falls with slight random horizontal drift."""

    image_path = os.path.join("./image/hazard", "meteor.png")
    name = "Meteor"
    _speed = 6

    def update_position(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-2, 2)
        if self.rect.top > HEIGHT:
            self._reset()


class Fireball(VerticalHazard):
    """
    Level 2 hazard. Faster than a meteor with more horizontal drift.

    !Adjust! image_path once a fireball asset is available.
    !Adjust! sound once a fireball sound is available.
    """

    image_path = os.path.join("./image/hazard", "meteor.png")  # placeholder
    name = "Fireball"
    _speed = 8

    def update_position(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-3, 3)
        if self.rect.top > HEIGHT:
            self._reset()


class Bomb(VerticalHazard):
    """
    Level 3 hazard. Dropped by the Helicopter — spawns at the helicopter's
    x position and falls straight down with no drift.

    Bombs are inactive by default. The controller calls activate_at(x) each
    time the helicopter fires, positioning the bomb directly below it.
    When a bomb exits the bottom of the screen or collides, it goes back to
    inactive and waits for the next drop — it does NOT respawn randomly.

    !Adjust! image_path once a bomb asset is available.
    !Adjust! _speed to tune difficulty (currently placeholder value).
    !Adjust! size to match the final asset dimensions.
    !Adjust! sound once a bomb/explosion sound is available.
    !Adjust! consider drawing a shadow/warning indicator on the ground
             at self.rect.centerx while the bomb is falling so the player
             can see the incoming drop zone.
    """

    image_path = os.path.join("./image/hazard", "meteor.png")  # placeholder
    name = "Bomb"
    _speed = 10
    size = (40, 60)

    def __init__(self):
        super().__init__()
        self.is_active = False          # inactive until the helicopter drops it
        self.rect.center = (-500, -500) # parked off-screen

    def activate_at(self, x: int, y: int = -60):
        """
        Drop this bomb from the given position.
        Pass the helicopter's rect.bottom as y so the bomb appears to
        fall from the helicopter rather than from the top of the screen.
        """
        self.rect.center = (x, y)
        self.is_active = True

    def update_position(self):
        if not self.is_active:
            return
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self._reset()

    def _reset(self):
        """Park off-screen and go inactive — helicopter will re-drop later."""
        self.is_active = False
        self.rect.center = (-500, -500)
