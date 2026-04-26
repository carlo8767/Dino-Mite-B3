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

# ──────────────────────────────────────────────────────────────────────────────
# Level 1
# ──────────────────────────────────────────────────────────────────────────────
class Meteor(VerticalHazard):
    """Falls with slight random horizontal drift."""

    image_path = os.path.join("./image/hazard", "meteor.png")
    name = "Meteor"
    _speed = 6

    def update_position(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-2, 2)
        if self.rect.top > HEIGHT:
            self._reset()


# ──────────────────────────────────────────────────────────────────────────────
# Level 2
# ──────────────────────────────────────────────────────────────────────────────

class Fireball(VerticalHazard):
    """
    Faster than a meteor with more horizontal drift.

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

class MammothLeg(VerticalHazard):
    """
    A giant mammoth leg that descends from the top of the screen
    in three phases, giving the player time to dodge by running left or right.

    Phases
    ------
    WARN  – the bottom of the leg hangs just inside the top edge, shaking
            slightly so the player knows exactly where it will stomp.
    SLAM  – leg drops at self.speed px/frame.
    HOLD  – leg rests at ground level for _HOLD_FRAMES; collision active.
    RISE  – leg retracts off-screen, then resets to a new random x.

    !Adjust! size to match the final MammothLegT asset dimensions.
    !Adjust! _WARN_FRAMES / _speed / _HOLD_FRAMES to tune difficulty.
    !Adjust! sound once a stomp sound is available.
    """

    image_path    = os.path.join("./image/hazard", "MammothLegT.png")
    name          = "MammothLeg"
    _speed        = 22          # slam speed (px/frame); slowed by powerup
    size          = (80, 200)

    _WARN_FRAMES  = 90          # frames to hang at top (~1.5 s at 60 fps)
    _HOLD_FRAMES  = 18          # frames to rest at ground after slam
    _RISE_SPEED   = 14          # retract speed - not affected by slow powerup
    _GROUND_BOTTOM = 625        # rect.bottom at full stomp (ground level)
    _HANG_BOTTOM   = 50         # rect.bottom during WARN (50 px visible as warning)

    _WARN = "warn"
    _SLAM = "slam"
    _HOLD = "hold"
    _RISE = "rise"

    def __init__(self):
        super().__init__()
        self._phase       = self._WARN
        self._phase_timer = 0
        # Position leg so only the bottom _HANG_BOTTOM pixels are visible
        self.position_x   = random.randint(100, WIDTH - 100)
        self.rect.centerx = self.position_x
        self.rect.bottom  = self._HANG_BOTTOM

    def update_position(self):
        if self._phase == self._WARN:
            self.rect.x  += random.randint(-2, 2)   # slight shake as warning
            self._phase_timer += 1
            if self._phase_timer >= self._WARN_FRAMES:
                self._phase       = self._SLAM
                self._phase_timer = 0

        elif self._phase == self._SLAM:
            self.rect.y += self.speed
            if self.rect.bottom >= self._GROUND_BOTTOM:
                self.rect.bottom  = self._GROUND_BOTTOM
                self._phase       = self._HOLD
                self._phase_timer = 0

        elif self._phase == self._HOLD:
            self._phase_timer += 1
            if self._phase_timer >= self._HOLD_FRAMES:
                self._phase       = self._RISE
                self._phase_timer = 0

        elif self._phase == self._RISE:
            self.rect.y -= self._RISE_SPEED
            if self.rect.bottom <= 0:
                self._reset()

    def update_position_collision(self):
        """Shield deflect - immediately retract without resetting to a new position."""
        self._phase       = self._RISE
        self._phase_timer = 0

    def _reset(self):
        self.position_x   = random.randint(100, WIDTH - 100)
        self.rect.centerx = self.position_x
        self.rect.bottom  = self._HANG_BOTTOM
        self._phase       = self._WARN
        self._phase_timer = 0
        self.is_active    = True


# ──────────────────────────────────────────────────────────────────────────────
# Level 3
# ──────────────────────────────────────────────────────────────────────────────
class Bomb(VerticalHazard):
    """
    Dropped by the Helicopter - spawns at the helicopter's
    x position and falls straight down with no drift.

    Bombs are inactive by default.

    !Adjust! _speed to tune difficulty.
    !Adjust! size to match the final asset dimensions.
    !Adjust! sound once a bomb/explosion sound is available.
    """

    image_path = os.path.join("./image/hazard", "BombT.png")
    name = "Bomb"
    _speed = 10
    size = (55, 80)

    def __init__(self):
        super().__init__()
        self.is_active = False          # inactive until the helicopter drops it
        self.rect.center = (-500, -500) # parked off-screen

    def activate_at(self, x: int, y: int = -60):
        """
        Drop this bomb from the given position.
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
        """Park off-screen and go inactive - helicopter will re-drop later."""
        self.is_active = False
        self.rect.center = (-500, -500)


