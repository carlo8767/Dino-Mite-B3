import pygame
import random  # used for spawn position in activate / update_position_collision

from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class PowerUp(pygame.sprite.Sprite):
    """
    Base class for all power-ups.

    Subclasses must define as class attributes:
        image_path (str): path to the powerup icon image
        name       (str): identifier used by the collision and game logic systems
        _speed     (int): fall speed in pixels per frame

    Subclasses must override:
        apply_effect(character): apply the powerup effect when collected
    """

    image_path: str = None
    name: str = "PowerUp"
    _speed: int = 3

    def __init__(self):
        super().__init__()
        self.is_active = False
        self.speed = self._speed
        self.image = pygame.transform.scale(
            pygame.image.load(self.image_path).convert_alpha(), (60, 60)
        )
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (random.randint(50, WIDTH - 50), -60)

    def activate(self):
        """Reset to a random top position and mark as actively falling."""
        self.rect.center = (random.randint(50, WIDTH - 50), -60)
        self.is_active = True

    def update_position(self):
        """Move downward each frame; deactivate if it exits the bottom."""
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.is_active = False
            self.rect.center = (random.randint(50, WIDTH - 50), -60)

    def update_position_collision(self):
        """Deactivate and reset off-screen after being collected."""
        self.is_active = False
        self.rect.center = (random.randint(50, WIDTH - 50), -60)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def apply_effect(self, _character):
        raise NotImplementedError(f"{self.__class__.__name__} must implement apply_effect")


class ShieldBubble(PowerUp):
    """Gives the player a shield for 5 seconds."""

    image_path = "./image/bubble/ShieldBubbleIcon.png"
    name = "ShieldBubble"
    _speed = 3

    def apply_effect(self, character):
        character.shield_active = True
        character.shield_timer = 5000


class TimeReduction(PowerUp):
    """Removes 5 seconds from the remaining level timer."""

    image_path = "./image/bubble/ExtraTimeIcon.png"
    name = "TimeReduction"
    _speed = 3

    def apply_effect(self, character):
        # The view adjusts start_ticks by -5000 ms on collection
        pass


class SlowerHazards(PowerUp):
    """Slows all hazards for 5 seconds."""

    image_path = "./image/bubble/ReducedVelocityIcon.png"
    name = "SlowerHazards"
    _speed = 3

    def apply_effect(self, character):
        # The controller applies and tracks the slowdown effect
        pass
