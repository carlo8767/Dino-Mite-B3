import pygame
import logging
from dino_mite_model.level_model.levelone import LevelOne
from dino_mite_utility.utilities_names import WIDTH, HEIGHT



class ControllerLevelOne:

    def __init__(self):
        self.level_one = LevelOne()
        self.rolling_rocks = []
        self.is_paused = False
        self.models_collision = dict()
        self.add_models_collision()

    def init_music(self):
        pygame.mixer.music.load(self.level_one.sound)
        pygame.mixer.music.play(-1, 0.0) # Forever Loop

    def init_music_end_level_one(self):
        pygame.mixer.music.load(self.level_one.sound_end_game)
        pygame.mixer.music.play(-1, 0.0)  # Forever Loop


    def stop_music(self):
        pygame.mixer.music.stop()

    def toggle_pause_menu(self):
        self.is_paused = not self.is_paused

    def update_movement_level_one(self):
        self.level_one.hazard_meteor.update_position()
        self.level_one.hazard_meteorOne.update_position()
        self.level_one.hazard_meteorTwo.update_position()
        self.level_one.hazard_rollingRock.update_position()

    # ==================== PLAYER INPUT (forwarded to model) ====================

    def handle_player_input(self, keys, events):
        """Forward keyboard input to the player_movement model."""
        self.level_one.character.handle_key_input(keys, events)

    def apply_player_gravity(self):
        """Forward gravity call to the player_movement model."""
        self.level_one.character.gravity()


    # ==================== COLLISION ====================
    def detection_collision_character(self, sprite) -> tuple[bool, str]:
        for playM, collM in self.models_collision.items():
            # Skip the sprite we are testing (the character itself)
            if playM == sprite:
                continue
            sprites_group = pygame.sprite.Group()
            sprites_group.add(playM)
            # spritecollide returns a list of colliding sprites and remove from the group
            if pygame.sprite.spritecollide(sprite, sprites_group, False, pygame.sprite.collide_mask):
                logging.info({f'collude occurs between {sprite} and {collM}'})
                return True, collM
        return False, ""

    def update_collision_position(self, name):
        [k.update_position_collision() for k, v in self.models_collision.items() if v == name]

    # ==================== SPLIT SCREEN COLLISION (hazards) ====================
    # Meteor and RollingRock have different behave when they leave
    # the screen, so they are handled separately.
    def screen_collision_meteor(self):
        """
        Meteor falls top to bottom.
        When it goes past the bottom of the screen, reset it back to
        the top with a new random x position (handled by update_position_collision).
        """
        x, y = self.level_one.hazard_meteor.get_current_position()
        if y > HEIGHT:
            self.update_collision_position(self.level_one.hazard_meteor.name)

    def screen_collision_rolling_rock(self):
        """
        Rolling rock moves left to right along the ground.
        When it exits the right side of the screen, reset it back to
        the left side so it loops around.
        """
        x, y = self.level_one.hazard_rollingRock.get_current_position()
        if x > WIDTH:
            # Reset to just off the left edge, keep same y (ground level)
            self.level_one.hazard_rollingRock.rect.x = -60
            self.level_one.hazard_rollingRock.rect.y = self.level_one.hazard_rollingRock.position_y

    # ==================== ADD MODEL COMPONENT LEVEL ONE (hazards) ====================
    def add_models_collision(self):
        """Register all level-one sprites for collision checking."""
        self.models_collision[self.level_one.character] = self.level_one.character.name
        self.models_collision[self.level_one.hazard_meteor] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorOne] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_meteorTwo] = self.level_one.hazard_meteor.name
        self.models_collision[self.level_one.hazard_rollingRock] = self.level_one.hazard_rollingRock.name