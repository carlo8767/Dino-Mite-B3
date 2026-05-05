import pygame
import random

from dino_mite_utility.utilities_names import HEIGHT, WIDTH


class CharacterDinoTwo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            "idle":       pygame.transform.scale(pygame.image.load("./image/character/2ndPlayerIdleT.png").convert_alpha(), (140, 140)),
            "walk_right": pygame.transform.scale(pygame.image.load("./image/character/2ndPlayerRunningT.png").convert_alpha(), (140, 140)),
            "walk_left":  pygame.transform.flip(pygame.transform.scale(pygame.image.load("./image/character/2ndPlayerRunningT.png").convert_alpha(), (140, 140)), True, False),
            "duck":       pygame.transform.scale(pygame.image.load("./image/character/2ndPlayerCrouchT.png").convert_alpha(), (140, 65)),
            "jump":       pygame.transform.scale(pygame.image.load("./image/character/2ndPlayerJumpT.png").convert_alpha(), (140, 140)),
            "dead":       pygame.transform.scale(pygame.image.load("./image/character/2ndPlayerDeadT.png").convert_alpha(), (140, 140)),
            "happy":      pygame.transform.scale(pygame.image.load("./image/character/levelpass.png").convert_alpha(), (140, 140)),
        }
        self.position_x = 460
        self.constant_ground = 500

        self.game_state = "idle"
        self.rect = self.images[self.game_state].get_rect()
        self.mask = pygame.mask.from_surface(self.images[self.game_state])
        self.speed_y = 0
        self.png_on_ground = True
        self.standing_height = 150
        self.rect.center = (self.position_x, self.constant_ground)
        self.duck_height = 75

        self.name = "Dina"
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.move_x = 2
        self.move_y = 2

        self.shield_active = False
        self.shield_timer = 0
        self.duck_start_ticks = 0

    # ==================== ACTIONS (called by controller) ====================

    def start_jump(self):
        self.speed_y = -15
        self.game_state = "jump"

    def start_duck(self):
        self.game_state = "duck"
        self.rect.height = self.duck_height
        self.rect.y = self.constant_ground + (self.standing_height - self.duck_height)
        self.duck_start_ticks = pygame.time.get_ticks()

    def stop_duck(self):
        self.game_state = "idle"
        self.rect.height = self.standing_height
        self.rect.y = self.constant_ground

    def walk_left(self):
        self.rect.x -= 5
        if self.rect.left < 0:
            self.rect.x += 5
        if self.game_state not in ("jump", "duck"):
            self.game_state = "walk_left"

    def walk_right(self):
        self.rect.x += 5
        if self.rect.right > self.screen_width:
            self.rect.x -= 5
        if self.game_state not in ("jump", "duck"):
            self.game_state = "walk_right"

    def set_idle(self):
        if self.png_on_ground and self.game_state not in ("duck", "jump"):
            self.game_state = "idle"

    # ==================== PHYSICS ====================

    def gravity(self):
        if self.game_state == "duck":
            return

        constant_gravity = 0.9
        self.speed_y += constant_gravity
        self.rect.y += self.speed_y

        if self.rect.y >= self.constant_ground:
            self.rect.y = self.constant_ground
            self.speed_y = 0
            self.png_on_ground = True
            if self.game_state == "jump":
                self.game_state = "idle"
        else:
            self.png_on_ground = False

    # ==================== DRAWING / POSITION ====================

    def draw(self, screen):
        screen.blit(self.images[self.game_state], self.rect)

    def movement_character_left(self):
        self.rect.x -= self.move_x

    def movement_character_right(self):
        self.rect.x += self.move_x

    def set_position_rectangle(self, position_x, position_y):
        self.rect.center = (position_x, position_y)

    def get_current_position(self):
        return self.rect.x, self.rect.y

    def set_current_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_position_collision(self):
        self.rect.y = self.constant_ground
        self.rect.x = random.randint(50, self.screen_width - 50)

    def draw_status(self, screen, state):
        self.game_state = state
        screen.blit(self.images[self.game_state], self.rect)
