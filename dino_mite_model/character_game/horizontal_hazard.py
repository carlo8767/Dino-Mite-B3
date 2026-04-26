import os.path
import random

import pygame

from dino_mite_utility.utilities_names import WIDTH


class HorizontalHazard(pygame.sprite.Sprite):
    """
    Base class for hazards that move horizontally across the screen.

    Subclasses must define as class attributes:
        image_path (str): path to the hazard image
        name       (str): identifier used by the collision system
        _move_x    (int): horizontal speed magnitude in pixels per frame
        size       (tuple): (width, height) to scale the image to
        _start_x   (int): starting x (off-screen left or right)
        _start_y   (int): center y (vertical position on screen)

    move_x is an instance copy of _move_x so the slowdown powerup can halve
    it per-instance without corrupting the class default.  
    Subclasses that travel right-to-left keep move_x positive and negate it internally.
    """

    image_path: str    = None
    name:       str    = "HorizontalHazard"
    _move_x:    int    = 2
    size:       tuple  = (60, 60)
    _start_x:   int    = -300
    _start_y:   int    = 600

    def __init__(self):
        super().__init__()
        self.move_x      = self._move_x
        self.position_x  = self._start_x
        self.position_y  = self._start_y
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(), self.size
        )
        self.rect        = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask        = pygame.mask.from_surface(self.image_loaded)
        self.is_active   = True

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x

    def update_position_collision(self):
        self.rect.x = self.position_x

    def get_current_position(self):
        return self.rect.x, self.rect.y


# ──────────────────────────────────────────────────────────────────────────────
# Bidirectional extension
# ──────────────────────────────────────────────────────────────────────────────

class BidirectionalHazard(HorizontalHazard):
    """
    Extension of HorizontalHazard for hazards that randomly alternate between
    left-to-right and right-to-left after each full screen pass.

    Subclasses get movement, direction-switching, and image-flipping for free
    — they only need to declare class attributes (image_path, name, _move_x,
    size, _start_x, _start_y).  No update_position or reset override needed
    unless the subclass adds extra per-frame logic (e.g. rotation).
    """

    def __init__(self):
        super().__init__()
        self._direction = 1                               # start LTR
        self._img_ltr   = self.image_loaded               # original orientation
        self._img_rtl   = pygame.transform.flip(self.image_loaded, True, False)

    def update_position(self):
        self.rect.x += self.move_x * self._direction

        exited = (
            (self._direction ==  1 and self.rect.left  > WIDTH) or
            (self._direction == -1 and self.rect.right < 0)
        )
        if exited:
            self._random_reset()

    def _random_reset(self):
        """Pick a random new direction and enter from the matching edge.

        Entry offsets are fixed constants, not self.rect.width, so subclasses
        that rebuild self.rect on every frame (e.g. RollingRock with rotation)
        get a consistent, rotation-proof spawn point every time.
        """
        self._direction = random.choice([1, -1])
        if self._direction == 1:                          # LTR: enter from left
            self.rect.x       = -200
            self.image_loaded = self._img_ltr
        else:                                             # RTL: enter from right
            self.rect.x       = WIDTH + 100
            self.image_loaded = self._img_rtl
        self.rect.centery = self.position_y
        self.mask         = pygame.mask.from_surface(self.image_loaded)

    def update_position_collision(self):
        """Shield deflect — immediately re-enter from a random edge."""
        self._random_reset()


# ──────────────────────────────────────────────────────────────────────────────
# Level 1
# ──────────────────────────────────────────────────────────────────────────────

class RollingRock(BidirectionalHazard):
    """
    Rolls across the ground in a random direction after each pass. 
    Rotation tracks direction of travel 
    - clockwise for LTR,
    - counter-clockwise for RTL 
    """

    image_path = os.path.join("./image/hazard", "rolling_rock.png")
    name       = "RollingRock"
    _move_x    = 2
    size       = (60, 60)

    def __init__(self):
        super().__init__()
        self._original_image = self.image_loaded.copy()
        self._angle = 0

    def update_position(self):
        # Let BidirectionalHazard handle movement and direction switching
        super().update_position()

        # Rotate clockwise for LTR (+direction=1 → angle decreases),
        # counter-clockwise for RTL (+direction=-1 → angle increases)
        self._angle   = (self._angle - 4 * self._direction) % 360
        center        = self.rect.center
        self.image_loaded = pygame.transform.rotate(self._original_image, self._angle)
        self.rect     = self.image_loaded.get_rect(center=center)
        self.mask     = pygame.mask.from_surface(self.image_loaded)


# ──────────────────────────────────────────────────────────────────────────────
# Level 3 — Helicopter (LTR)
# ──────────────────────────────────────────────────────────────────────────────

class Helicopter(HorizontalHazard):
    """
    Flies left-to-right near the top of the screen and
    drops Bomb instances.

    Every _drop_interval frames should_drop() returns True and the controller
    activates the next idle Bomb at this helicopter's current centre x.

    !Adjust! _move_x to tune flight speed.
    !Adjust! _drop_interval (currently 120 frames ≈ 2 s at 60 fps).
    !Adjust! size to match the final asset dimensions.
    !Adjust! sound once a rotor sound is available.
    """

    image_path     = os.path.join("./image/hazard", "HelicopterT.png")
    name           = "Helicopter"
    _move_x        = 3
    size           = (120, 60)
    _start_x       = -200
    _start_y       = 80
    _drop_interval = 120

    def __init__(self):
        super().__init__()
        self._drop_timer = 0

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x
        self._drop_timer += 1

    def should_drop(self) -> bool:
        if self._drop_timer >= self._drop_interval:
            self._drop_timer = 0
            return True
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Level 3 — Helicopter (RTL, lower altitude)
# ──────────────────────────────────────────────────────────────────────────────

class HelicopterTwo(HorizontalHazard):
    """
    A second helicopter flying right-to-left at a slightly
    lower altitude than Helicopter.

    Image is flipped horizontally on load so it faces left (direction of travel).

    !Adjust! _move_x, _drop_interval, _start_y as needed.
    !Adjust! sound once a rotor sound is available.
    """

    image_path     = os.path.join("./image/hazard", "HelicopterT.png")
    name           = "HelicopterTwo"
    _move_x        = 4
    size           = (120, 60)
    _start_x       = WIDTH + 200   # starts off right edge, flies left
    _start_y       = 155           # lower than Helicopter (80) — visual depth
    _drop_interval = 150

    def __init__(self):
        super().__init__()
        self._drop_timer  = 0
        self.image_loaded = pygame.transform.flip(self.image_loaded, True, False)
        self.mask         = pygame.mask.from_surface(self.image_loaded)

    def update_position(self):
        self.rect.x -= self.move_x                   # RTL
        if self.rect.right < 0:
            self.rect.x = self.position_x            # reset to right side
        self._drop_timer += 1

    def update_position_collision(self):
        self.rect.x = self.position_x

    def should_drop(self) -> bool:
        if self._drop_timer >= self._drop_interval:
            self._drop_timer = 0
            return True
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Level 3 — Drone (bidirectional, unpredictable)
# ──────────────────────────────────────────────────────────────────────────────

class Drone(BidirectionalHazard):
    """
    Flies at mid-height - the player must duck under it.

    After each full pass the drone randomly picks LTR or RTL for the next
    entry.

    !Adjust! _start_y if the character hitbox changes.
    !Adjust! _move_x to tune speed.
    !Adjust! size to match the final DroneT asset dimensions.
    !Adjust! sound once a buzzing sound is available.
    """

    image_path = os.path.join("./image/hazard", "DroneT.png")
    name       = "Drone"
    _move_x    = 5
    size       = (80, 50)
    _start_x   = -300
    _start_y   = 520    
