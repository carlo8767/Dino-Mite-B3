import pygame
import random


from dino_mite_utility.utilities_names import WIDTH, HEIGHT



class ShieldBubble(pygame.sprite.Sprite):
    """
    ShieldBubble powerup - gives the player a shield for 5 seconds
    """
    def __init__(self ,speed=3,  placeholder_color=(255, 0, 0)):
        super().__init__()
        self.name = "ShieldBubble"
        self.active_power_up_icon_bubble = False

        # Load and scale image, or draw a colored placeholder if no path given
        self.image_path_bubble_icon = "./image/bubble/ShieldBubbleIcon.png"
        if self.image_path_bubble_icon is not None:
            self.image_loaded_bubble_icon = pygame.transform.scale(
                pygame.image.load(self.image_path_bubble_icon).convert_alpha(), (60, 60)
            )
        else:
            self.image_loaded_bubble_icon = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.image_loaded_bubble_icon.fill(placeholder_color)
        self.image = self.image_loaded_bubble_icon

        # Random x position, spawn above screen
        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60  # start above screen
        self.rect = self.image_loaded_bubble_icon.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image_loaded_bubble_icon)
        self.speed = speed


    def apply_effect(self, character):
        character.shield_active = True
        character.shield_timer = 5000  # 5 seconds in milliseconds
        print("Shield activated!")


    def update_position_collision(self):
        # Reset to top with new random x when collected or expired
        self.rect.y = self.position_y = -60
        self.rect.x = random.randint(50, WIDTH - 50)
        self.active_power_up_icon_bubble = False

    def update_position(self):
        # Falls downward every frame
        self.rect.y += self.speed
        self.rect.x -= random.randint(-2, 2)

        # If it hits the ground it disappears
        if self.rect.top >= HEIGHT:
            self.active_power_up_icon_bubble = False
            self.rect.center = (random.randint(50, WIDTH - 50), -60)


    def draw_bubble(self, screen):
       screen.blit(self.image_loaded_bubble_icon, self.rect)


class TimeReduction(pygame.sprite.Sprite):
    """
    TimeReduction powerup - removes 5 seconds from the remaining timer
    """
    def __init__(self , speed=4,  placeholder_color=(255, 0, 0)):
        super().__init__()
        self.name = "TimeReduction"
        self.is_active_time_reduction = False
        self.image_path_time = "./image/bubble/ExtraTimeIcon.png"
        if self.image_path_time is not None:
            self.image_loaded_time_reduction = pygame.transform.scale(
                pygame.image.load(self.image_path_time).convert_alpha(), (60, 60)
            )
        else:
            self.image_loaded_time_reduction = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.image_loaded_time_reduction.fill(placeholder_color)
        self.image = self.image_loaded_time_reduction


        # Random x position, spawn above screen

        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60  # start above screen

        self.rect = self.image_loaded_time_reduction.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image_loaded_time_reduction)

        self.speed = speed

    def apply_effect(self, _character):
        print("Time reduced by 5 seconds!")

    def update_position(self):
        # Falls downward every frame
        self.rect.y += self.speed
        self.rect.x -= random.randint(-2, 2)

        # If it hits the ground it disappears
        if self.rect.top >= HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -60)

    def update_position_collision(self):
        # Reset to top with new random x when collected or expired
            self.rect.y = self.position_y = -60
            self.rect.x = random.randint(50, WIDTH- 50)

    def draw_time_reduction(self, screen):
        screen.blit(self.image_loaded_time_reduction, self.rect)


class SlowerHazards(pygame.sprite.Sprite):
    """
    SlowerHazards powerup - makes incoming hazards speed decrease for 5 seconds
    """
    def __init__(self, speed=3, placeholder_color=(255, 0, 0)):
        super().__init__()
        self.name = "SlowerHazards"
        self.is_active_slower_hazard = False

        self.image_path_slow_hazard = "./image/bubble/ReducedVelocityIcon.png"
        if self.image_path_slow_hazard is not None:
            self.image_loaded_slow_hazard = pygame.transform.scale(
                pygame.image.load(self.image_path_slow_hazard).convert_alpha(), (60, 60)
            )
        else:
            self.image_loaded_slow_hazard = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.image_loaded_slow_hazard.fill(placeholder_color)
        self.image = self.image_loaded_slow_hazard

        # Random x position, spawn above screen
        self.position_x = random.randint(50, WIDTH - 50)
        self.position_y = -60  # start above screen

        self.rect = self.image_loaded_slow_hazard.get_rect()
        self.rect.center = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image_loaded_slow_hazard)

        self.speed = speed


    def update_position(self):
        # Falls downward every frame
        self.rect.y += self.speed

        # If it hits the ground it disappears
        if self.rect.top  >= HEIGHT:
            self.is_active_slower_hazard = False
            self.rect.center = (random.randint(50, WIDTH - 50), -60)


    def update_position_collision(self):
        # Reset to top with new random x when collected or expired
        self.rect.y = self.position_y = -60
        self.rect.x = random.randint(50, WIDTH - 50)


