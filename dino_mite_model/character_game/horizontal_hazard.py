import os.path

import pygame

from dino_mite_utility.utilities_names import WIDTH


class HorizontalHazard(pygame.sprite.Sprite):
    """
    Base class for hazards that roll/walk horizontally across the ground.

    Subclasses must define as class attributes:
        image_path (str): path to the hazard image
        name       (str): identifier used by the collision system
        _move_x    (int): horizontal speed in pixels per frame
        size       (tuple): (width, height) to scale the image to
        _start_x   (int): x position to reset to (off-screen left)
        _start_y   (int): y position (ground level)
    """

    image_path: str = None
    name: str = "HorizontalHazard"
    _move_x: int = 2
    size: tuple = (60, 60)
    _start_x: int = -300
    _start_y: int = 600

    def __init__(self):
        super().__init__()
        self.move_x = self._move_x  # instance copy so slowdown powerup can modify it
        self.position_x = self._start_x
        self.position_y = self._start_y
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(), self.size
        )
        self.rect = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image_loaded)
        self.is_active = True

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x

    def update_position_collision(self):
        self.rect.x = self.position_x

    def get_current_position(self):
        return self.rect.x, self.rect.y


class RollingRock(HorizontalHazard):
    """Level 1 hazard. Rolls left-to-right across the ground."""

    image_path = os.path.join("./image/hazard", "rolling_rock.png")
    name = "RollingRock"
    _move_x = 2
    size = (60, 60)


class Mammoth(HorizontalHazard):
    """
    Level 2 hazard. Stomps left-to-right across the ground, faster than the rolling rock.

    !Adjust! image_path once a mammoth asset is available.
    !Adjust! size once the mammoth image dimensions are known.
    !Adjust! sound once a mammoth stomp sound is available.
    """

    image_path = os.path.join("./image/hazard", "rolling_rock.png")  # placeholder
    name = "Mammoth"
    _move_x = 3
    size = (80, 80)
