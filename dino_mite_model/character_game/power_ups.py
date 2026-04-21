import pygame
import random
from dino_mite_utility.utilities_names import WIDTH, HEIGHT


class PowerUp(pygame.sprite.Sprite):
    """
    Base class for all powerups
    Mirrors the Hazard class structure-falls from the sky
    Disappears when it hits the ground or is collected
    Subclasses override apply_effect to define what happens on collection
    """
    def __init__(self, image_path, speed=3, placeholder_color=(255, 0, 0)):
        super().__init__()

        # Load and scale image, or draw a colored placeholder if no path given
        if image_path is not None:
            self.image_loaded = pygame.transform.scale(
                pygame.image.load(image_path).convert_alpha(), (60, 60)
            )
        else:
            self.image_loaded = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.image_loaded.fill(placeholder_color)
        self.image = self.image_loaded

        # Random x position, spawn above screen
        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60  # start above screen

        self.rect = self.image_loaded.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image_loaded)

        self.speed = speed
        self.is_active = True
        self.name = "PowerUp"

    def update_position(self):
        # Falls downward every frame 
        self.rect.y += self.speed

        # If it hits the ground it disappears
        if self.rect.y >= HEIGHT:
            self.is_active = False

    def get_current_position(self):
        return self.rect.x, self.rect.y

    def update_position_collision(self):
        # Reset to top with new random x when collected or expired
        self.position_x = random.randint(50, WIDTH - 50)
        self.rect.center = (self.position_x, -60)
        self.is_active = True

    def apply_effect(self, character):
        # Subclasses override this
        pass

    def draw(self, screen):
        screen.blit(self.image_loaded, self.rect)

class ShieldBubble(PowerUp):
    """
    ShieldBubble powerup - gives the player a shield for 5 seconds
    """
    def __init__(self):
        super().__init__("./image/bubble/Shield Bubble Icon.png", speed=3)
        self.name = "ShieldBubble"

    def apply_effect(self, character):
        character.shield_active = True
        character.shield_timer = 5000  # 5 seconds in milliseconds
        print("Shield activated!")


class TimeReduction(PowerUp):
    """
    TimeReduction powerup - removes 5 seconds from the remaining timer
    """
    def __init__(self):
        super().__init__("./image/bubble/Extra Time Icon.png", speed=4)
        self.name = "TimeReduction"

    def apply_effect(self, _character):
        print("Time reduced by 5 seconds!")


class SlowerHazards(PowerUp):
    """
    SlowerHazards powerup - makes incoming hazards speed decrease for 5 seconds
    """
    def __init__(self):
        super().__init__("./image/bubble/Reduced Velocity Icon.png", speed=3)
        self.name = "SlowerHazards"

    def apply_effect(self, character):
        print("Hazards slowed down for 5 seconds!")