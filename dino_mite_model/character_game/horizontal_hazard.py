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
        _start_x   (int): x position to reset to (off-screen left or right)
        _start_y   (int): y position (center y)

    move_x is an instance copy of _move_x so the slowdown powerup can modify
    it per-instance without corrupting the class default.  For right-to-left
    hazards (HelicopterTwo, Drone in RTL pass) move_x stays positive and the
    subclass applies the sign internally — this keeps the base controller's
    slowdown arithmetic correct.
    """

    image_path: str   = None
    name:        str  = "HorizontalHazard"
    _move_x:     int  = 2
    size:        tuple = (60, 60)
    _start_x:    int  = -300
    _start_y:    int  = 600

    def __init__(self):
        super().__init__()
        self.move_x      = self._move_x
        self.position_x  = self._start_x
        self.position_y  = self._start_y
        self.image_loaded = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(), self.size
        )
        self.rect         = self.image_loaded.get_rect()
        self.rect.center  = (self.position_x, self.position_y)
        self.mask         = pygame.mask.from_surface(self.image_loaded)
        self.is_active    = True

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x

    def update_position_collision(self):
        self.rect.x = self.position_x

    def get_current_position(self):
        return self.rect.x, self.rect.y


# ──────────────────────────────────────────────────────────────────────────────
# Level 1
# ──────────────────────────────────────────────────────────────────────────────

class RollingRock(HorizontalHazard):
    """Level 1 hazard. Rolls left-to-right across the ground with clockwise rotation."""

    image_path = os.path.join("./image/hazard", "rolling_rock.png")
    name       = "RollingRock"
    _move_x    = 2
    size       = (60, 60)

    def __init__(self):
        super().__init__()
        self._original_image = self.image_loaded.copy()
        self._angle = 0

    def update_position(self):
        self.rect.x += self.move_x
        if self.rect.left > WIDTH:
            self.rect.x = self.position_x

        # Clockwise rotation to match rightward movement
        self._angle      = (self._angle - 4) % 360
        center           = self.rect.center
        self.image_loaded = pygame.transform.rotate(self._original_image, self._angle)
        self.rect         = self.image_loaded.get_rect(center=center)
        self.mask         = pygame.mask.from_surface(self.image_loaded)


# ──────────────────────────────────────────────────────────────────────────────
# Level 3 — Helicopter (left-to-right)
# ──────────────────────────────────────────────────────────────────────────────

class Helicopter(HorizontalHazard):
    """
    Level 3 hazard. Flies left-to-right near the top of the screen and
    periodically drops Bomb instances.

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
    _start_y       = 80           # near the top of the screen
    _drop_interval = 120          # frames between bomb drops

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
# Level 3 — Helicopter (right-to-left, lower altitude)
# ──────────────────────────────────────────────────────────────────────────────

class HelicopterTwo(HorizontalHazard):
    """
    Level 3 hazard. A second helicopter flying right-to-left at a slightly
    lower altitude than Helicopter, creating a crossing pattern.

    move_x is stored as a positive value; update_position subtracts it so the
    helicopter travels right-to-left.  This keeps the base controller's slow-
    down arithmetic (which uses max(1, ...)) correct — it always operates on a
    positive magnitude and direction is handled here.

    The image is flipped horizontally on load so it faces left (direction of travel).

    !Adjust! _move_x, _drop_interval, and _start_y as needed.
    !Adjust! sound once a rotor sound is available.
    """

    image_path     = os.path.join("./image/hazard", "HelicopterT.png")
    name           = "HelicopterTwo"
    _move_x        = 4
    size           = (120, 60)
    _start_x       = WIDTH + 200   # starts off right edge, flies left
    _start_y       = 155           # slightly lower than Helicopter (80) — visual depth
    _drop_interval = 150           # slightly different rhythm from Helicopter

    def __init__(self):
        super().__init__()
        self._drop_timer = 0
        # Flip image so the helicopter faces left (direction of travel)
        self.image_loaded = pygame.transform.flip(self.image_loaded, True, False)
        self.mask         = pygame.mask.from_surface(self.image_loaded)

    def update_position(self):
        self.rect.x -= self.move_x                  # right-to-left
        if self.rect.right < 0:                      # exited left edge
            self.rect.x = self.position_x            # reset to right side
        self._drop_timer += 1

    def update_position_collision(self):
        self.rect.x = self.position_x               # reset to right side

    def should_drop(self) -> bool:
        if self._drop_timer >= self._drop_interval:
            self._drop_timer = 0
            return True
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Level 3 — Drone (bidirectional, unpredictable)
# ──────────────────────────────────────────────────────────────────────────────

class Drone(HorizontalHazard):
    """
    Level 3 hazard. Flies at mid-height — the player must duck under it.

    After each full pass the drone randomly picks left-to-right or right-to-
    left for its next pass, keeping the player guessing which side to watch.
    The image is flipped to face the direction of travel on each pass.

    move_x is always a positive magnitude; _direction (±1) is applied inside
    update_position so the slowdown powerup works without sign errors.

    _start_y is tuned so the drone's bottom edge sits just above the standing
    character's head top (~y 510), requiring a duck to pass safely.

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
    _start_y   = 490    # center y; bottom = 515, just above char standing top (510)

    def __init__(self):
        super().__init__()
        self._direction  = 1                         # 1 = LTR, -1 = RTL
        # Cache both orientations — swap on direction change, no per-frame cost
        self._img_ltr    = self.image_loaded
        self._img_rtl    = pygame.transform.flip(self.image_loaded, True, False)

    def update_position(self):
        self.rect.x += self.move_x * self._direction

        exited = (
            (self._direction ==  1 and self.rect.left  > WIDTH) or
            (self._direction == -1 and self.rect.right < 0)
        )
        if exited:
            self._random_reset()

    def _random_reset(self):
        """Pick a random new direction and enter from the matching edge."""
        self._direction = random.choice([1, -1])
        if self._direction == 1:                     # LTR: enter from left
            self.rect.x       = -self.rect.width - 10
            self.image_loaded = self._img_ltr
        else:                                        # RTL: enter from right
            self.rect.x       = WIDTH + 10
            self.image_loaded = self._img_rtl
        self.rect.centery = self.position_y
        self.mask         = pygame.mask.from_surface(self.image_loaded)

    def update_position_collision(self):
        self._random_reset()
