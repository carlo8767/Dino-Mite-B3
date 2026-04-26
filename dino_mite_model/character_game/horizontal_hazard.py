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
    """Level 1 hazard. Rolls left-to-right across the ground with clockwise rotation."""

    image_path = os.path.join("./image/hazard", "rolling_rock.png")
    name = "RollingRock"
    _move_x = 2
    size = (60, 60)

    def __init__(self):
        super().__init__()
        self._original_image = self.image_loaded.copy()
        self._angle = 0

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x

        # Rotate clockwise to match rightward movement (~4 degrees per frame)
        self._angle = (self._angle - 4) % 360
        center = self.rect.center
        self.image_loaded = pygame.transform.rotate(self._original_image, self._angle)
        self.rect = self.image_loaded.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image_loaded)


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


class Helicopter(HorizontalHazard):
    """
    Level 3 hazard. Flies left-to-right across the top of the screen and
    periodically drops Bomb instances.

    The drop timer increments every frame inside update_position(). The
    controller calls should_drop() once per frame — when it returns True
    the controller activates one of the level's Bomb instances at this
    helicopter's current centre x.

    The helicopter itself is a collision hazard, but since it flies near
    the top of the screen the player can only be hit by it with unusual
    movement — its main role is as a bomb dropper.

    !Adjust! image_path once a helicopter asset is available.
    !Adjust! _move_x to tune flight speed.
    !Adjust! _drop_interval to tune how often bombs are dropped
             (currently 120 frames = 2 seconds at 60 fps).
    !Adjust! size to match the final asset dimensions.
    !Adjust! sound once a helicopter/rotor sound is available.
    """

    image_path = os.path.join("./image/hazard", "rolling_rock.png")  # placeholder
    name = "Helicopter"
    _move_x = 3
    size = (120, 60)    # wide and flat — helicopter silhouette
    _start_x = -200
    _start_y = 80       # near the top of the screen

    _drop_interval = 120  # frames between bomb drops (~2 s at 60 fps)

    def __init__(self):
        super().__init__()
        self._drop_timer = 0

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x
        self._drop_timer += 1

    def should_drop(self) -> bool:
        """
        Returns True once every _drop_interval frames and resets the timer.
        Call this from the controller's update_movement() to trigger a bomb drop.
        """
        if self._drop_timer >= self._drop_interval:
            self._drop_timer = 0
            return True
        return False


class Drone(HorizontalHazard):
    """
    Level 3 hazard. Flies left-to-right at mid-screen height — NOT at ground level.
    The player must duck under it rather than jump over it, introducing a new
    required input in Level 3.

    _start_y is set to mid-screen (~300 px). Adjust this to match the height
    that forces a duck without being unfair given the character's crouch hitbox.

    !Adjust! image_path once a drone asset is available.
    !Adjust! _start_y to the exact height that requires ducking (depends on character hitbox).
    !Adjust! _move_x to tune speed — drones should feel fast and mechanical.
    !Adjust! size to match the final asset dimensions.
    !Adjust! sound once a drone/buzzing sound is available.
    !Adjust! consider whether drones should also come from the right (negative move_x)
             for variety — if so, _start_x should be WIDTH + 300 and reset logic inverted.
    """

    image_path = os.path.join("./image/hazard", "rolling_rock.png")  # placeholder
    name = "Drone"
    _move_x = 5
    size = (80, 50)      # wide and flat — drone shape
    _start_x = -300
    _start_y = 520       # just above the character's head (head top = y 450, drone bottom = y 445)
